from .microsoft_access import check_microsoft_access_drivers, check_microsoft_access_mdb_file


def odbc_checkers(file_path: str):
    check_microsoft_access_drivers()
    check_microsoft_access_mdb_file(file_path)
