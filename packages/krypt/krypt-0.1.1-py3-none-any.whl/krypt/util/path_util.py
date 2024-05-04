import os


def absolute(path):
    return os.path.abspath(path)


def walk(path):
    res = []

    def on_error(error):
        raise error

    path = absolute(path)

    if not os.path.isdir(path):
        raise ValueError(f"Path {path} is not a directory")

    paths = os.walk(path, topdown=True, onerror=on_error, followlinks=False)

    for root, dirs, files in paths:
        for file in files:
            file_path = str(os.path.join(root, file))
            relative_path = os.path.relpath(file_path, path)

            res.append(relative_path)

    return res


def filter_contents(files):
    res = []

    for x in files:
        if not x.endswith(".kpt") and x.find(".kpt.") == -1:
            continue
        if os.path.split(x)[0] == ".krypt":
            continue

        res.append(x)

    return res
