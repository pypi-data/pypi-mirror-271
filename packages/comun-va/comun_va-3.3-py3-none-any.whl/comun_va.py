from datetime import datetime
from pyzbar.pyzbar import decode
import tensorflow as tf
import numpy as np
import cv2

import comun_sqlsrv
import comun_mail


class AILog:
    def __init__(self, endpoint_name: str, endpoint_data_received: str):
        self.date_time: datetime = datetime.now()
        self.endpoint_name: str = endpoint_name
        self.endpoint_data_received: str = endpoint_data_received
        self.result: str = "KO_199"
        self.prediction: str = ""
        self.match_score: float = 0.0
        self.img_path: str = ""
        self.img_name: str = ""
        self.img_frame = None
        self.error: str = ""
        self.bar_code: any = ""

    def __str__(self):
        return f"""
                LOG:
                Date: {self.date_time},
                Endpoint name: {self.endpoint_name},
                Endpoint received data: {self.endpoint_data_received},
                Result: {self.result},
                Prediction: {self.prediction},
                Match score: {self.match_score}
                """

    def save_log(self, mssql_srv: str, database: str, user: str, passwd: str, rescale_size: tuple = None):
        """
        Save the image in local path and the data into the DB
        :param mssql_srv: IP of the MSSQL server
        :param database: Name of the database
        :param user: User of the database
        :param passwd: Password of the user
        :param rescale_size: A tuple with the HxW (in px) to rescale the image, example: (512, 512)
        :return: doesn't return anything
        """
        # SAVE IMAGE:
        if self.img_frame is not None:
            if not self.img_name:
                self.img_name = f'{self.date_time.strftime("%Y_%m_%d_%H_%M_%S")}.png'
            if not self.img_path:
                self.img_path = f'img_save/{self.img_name}'
            if rescale_size:
                self.img_frame = cv2.resize(self.img_frame, rescale_size)
            cv2.imwrite(self.img_path, self.img_frame)

        # SAVE LOG IN DB:
        mssql = comun_sqlsrv.Sql(mssql_srv, database, user, passwd)
        query = f"""
                INSERT INTO T_VA_API_LOG
                (FECHA_HORA, ENDPOINT, RESULTADO, DATO_RECIBIDO, PREDICCION_VA, NOMBRE_IMAGEN, COD_BAR, ERROR, PORCENTAJE_ACIERTO)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        query_values = (self.date_time,
                        str(self.endpoint_name),
                        str(self.result),
                        str(self.endpoint_data_received),
                        str(self.prediction),
                        str(self.img_name),
                        str(self.bar_code),
                        str(self.error),
                        str(self.match_score))
        mssql.ejecutar(query, query_values)
        mssql.cerrar_conexion()

    def send_email_info(self, smtp_host: str, email_subject: str, receiver: list):
        """
        Send an email with VA information
        :param smtp_host: IP and port of the smtp server, example: "10.10.10.5:587"
        :param email_subject: String with the subject of the email
        :param receiver: list with email destinations, example: ["miki@gmail.es","adolfo@gmail.es"]
        :return: doesn't return anything
        """
        msg = f"""
            INFORME VISIÓN:
        
            Nombre del endpoint (URL llamada): {self.endpoint_name} \n
            Datos recibidos por el endpoint: {self.endpoint_data_received} \n
            Resultado (respuesta a la llamada): {self.result} \n
            Descripción: {self.error} \n"""
        if self.prediction:
            msg += f"""
            Predicción de la vision: {self.prediction} \n
            Porcentaje de acierto: {self.match_score} \n"""
        if self.bar_code:
            msg += f"""
            Código de barras leído: {str(self.bar_code)} \n"""
        if self.img_path:
            comun_mail.send_mail(smtp_host, msg, email_subject, receiver, self.img_path)
        else:
            comun_mail.send_mail(smtp_host, msg, email_subject, receiver)


def get_image_from_ip_camera(camera_url: str, frames_to_calibrate: int = 1):
    """
    Function that connect to an IP camera and return a frame
    :param camera_url: need to be the RTSP URL
    :param frames_to_calibrate: Sometimes the iris of the camera needs some frames to calibrate, otherwise the
    image cud be too brightness or too dark. This value has to be greater than 0
    :return: given frame from OpenCV when you read a video capture
    """
    try:
        cap = cv2.VideoCapture(camera_url)  # IP Camera
        if not cap.isOpened():
            raise Exception(f"No se ha podido conectar a la camara {camera_url}")
        for _ in range(frames_to_calibrate):
            success, frame = cap.read()
            if not success:
                raise Exception("No se ha podido obtener un frame (imagen) de la camara")
        cap.release()
        return frame

    except Exception as e:
        raise Exception(f"Error relacionado con la camara: {str(e)}")


def read_barcode_from_ip_camera(camera_url: str, frames_to_read: int = 10) -> set[str]:
    """
    Function that connect to an IP camera and return all the barcodes or QRs that can be read (without repeat)
    :param camera_url: need to be the RTSP URL
    :param frames_to_read: quantity of frames that you want to use for reading the barcodes, has to be greater than 0
    :return: list of all barcodes read without repeat
    """
    try:
        barcodes = set()
        cap = cv2.VideoCapture(camera_url)  # IP Camera
        for _ in range(frames_to_read):
            success, frame = cap.read()
            if not success:
                raise Exception
            detected_barcodes = decode(frame)
            if detected_barcodes:
                for barcode in detected_barcodes:
                    if barcode.data != "":
                        # Convert the byte string to a string
                        decoded_barcode = barcode.data.decode("utf-8")
                        # A set cannot have repeated elements, so we don't need to check if already exist.
                        barcodes.add(decoded_barcode)

        cap.release()
        return barcodes

    except Exception as e:
        raise Exception(f"Error durante el proceso de lectura de código de barras: {str(e)}")


def run_model_with_frame(img_frame, class_names: dict, model, output=False, limit_gpu=False,
                         rescaled_size=(256, 256)) -> tuple[str, float]:
    """
    Function that execute an IA model
    :param img_frame: given frame from OpenCV when you read a video capture
    :param class_names: the posibles results of the IA
    :param model: the loaded model
    :param output: set to True if you want to see all predictions
    :param limit_gpu: set the GPU memory usage only to what is needed
    :param rescaled_size: the size of the images which the model has been trained (img_height, img_width)
    :return: the maximum value predicted by the model from class_names dictionary and the match score
    """
    try:
        if limit_gpu:
            # Limit the GPU memory usage only to what is needed, without this TensorFlow would use all the GPU memory.
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                try:
                    for gpu in gpus:
                        tf.config.experimental.set_memory_growth(gpu, True)
                except RuntimeError as e:
                    print(str(e))

        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        image_resized = cv2.resize(img_frame, rescaled_size)
        # save the img as .jpg, load it and dete it. We do this because the neuronal network is trained with .jpg images
        # .jpg images are compressed and is different from the img_frame (the Pypi matrix is different)
        cv2.imwrite("img.jpg", image_resized)
        img_jpg = cv2.imread("img.jpg", cv2.IMREAD_UNCHANGED)
        image = np.expand_dims(img_jpg, axis=0)
        predictions = model.predict(image)
        index = np.argmax(predictions)
        class_name = str(class_names[index])
        match_score = float(str(predictions[0][index])[:4])

        if output:
            print("\nPREDICTION:", flush=True)
            print(f"Class name: {class_name}  Match Score: {predictions[0][index]}", flush=True)
            print(f"All predictions: {predictions}", flush=True)

        return class_name, match_score

    except Exception as e:
        raise Exception(f"Error, no se ha podido ejecutar la red neuronal: {str(e)}")
