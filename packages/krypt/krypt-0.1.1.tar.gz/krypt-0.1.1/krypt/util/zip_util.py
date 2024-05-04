import zipfile


def list_files(zip_path):
    if not zipfile.is_zipfile(zip_path):
        return []

    with zipfile.ZipFile(zip_path, "r") as f:
        return f.namelist()


def exists(zip_path, file_path):
    return file_path in list_files(zip_path)


def read_file(zip_path, file_path):
    with zipfile.ZipFile(zip_path, "r") as f:
        return f.read(file_path)


def append(zip_path, file_path, data):
    with zipfile.ZipFile(zip_path, "a") as f:
        f.writestr(file_path, data)
        f.close()


def merge(original, new):
    for x in list_files(original):
        if exists(new, x):
            continue

        append(new, x, read_file(original, x))
