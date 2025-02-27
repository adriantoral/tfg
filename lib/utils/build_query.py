from lib.utils.convert_to_type import convert_to_type


def build_query(query: list[str]):
    return ' '.join([line for line in query if line])


def build_query_colums(columns_value: dict[str, str], ignore: list[str]):
    return {
        column.upper(): convert_to_type(value)
        for column, value in columns_value.items()
        if column not in ignore and value
    }
