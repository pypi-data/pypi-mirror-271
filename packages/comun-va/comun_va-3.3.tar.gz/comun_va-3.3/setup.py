from setuptools import setup

setup(name='comun_va',
      version='3.3',
      py_modules=['comun_va', 'comun_mail'],
      install_requires=['comun_sqlsrv', 'opencv-python', 'tensorflow', 'numpy', 'pyzbar'])
