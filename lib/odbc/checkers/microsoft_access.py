import os.path

import pyodbc


def check_microsoft_access_drivers():
    if not any(driver.startswith('Microsoft Access Driver') for driver in pyodbc.drivers()):
        raise RuntimeError('Microsoft Access drivers not found')


def check_microsoft_access_mdb_file(file_path: str):
    if not file_path.endswith('.mdb'):
        raise RuntimeError('File is not a Microsoft Access database')

    if not os.path.exists(file_path):
        raise RuntimeError('File not found')

    return True
