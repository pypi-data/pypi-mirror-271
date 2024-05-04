import os


def init(cluster_path: str):
    config_path = get_config_path(cluster_path)

    if not os.path.exists(config_path):
        os.makedirs(config_path)


def get_cluster_path(cluster_path: str):
    return os.path.abspath(cluster_path)


def get_config_path(cluster_path: str):
    return os.path.join(get_cluster_path(cluster_path), ".krypt")


def get_private_key_path(cluster_path: str):
    return os.path.join(get_config_path(cluster_path), "private.key")


def get_public_key_path(cluster_path: str):
    return os.path.join(get_config_path(cluster_path), "public.key")


def get_data_path(cluster_path: str):
    return os.path.join(get_config_path(cluster_path), "data.zip")


def get_new_data_path(cluster_path: str):
    return os.path.join(get_config_path(cluster_path), "data_new.zip")


def read_private_key(cluster_path: str):
    with open(get_private_key_path(cluster_path), "rb") as f:
        return f.read()


def read_public_key(cluster_path: str):
    with open(get_public_key_path(cluster_path), "rb") as f:
        return f.read()


def store_private_key(cluster_path: str, private_key: bytes):
    with open(get_private_key_path(cluster_path), "wb") as f:
        f.write(private_key)


def store_public_key(cluster_path: str, public_key: bytes):
    with open(get_public_key_path(cluster_path), "wb") as f:
        f.write(public_key)
