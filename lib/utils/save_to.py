from json import dump


def save_to_file(serializable: object, path: str) -> None:
    file = open(path, 'w', encoding='utf-8')
    dump(serializable, file, indent=4, ensure_ascii=False)
    file.close()
