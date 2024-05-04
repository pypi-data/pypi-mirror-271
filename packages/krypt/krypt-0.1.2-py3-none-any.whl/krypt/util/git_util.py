import os

from krypt.util import meta_util


def get_gitignore_path(cluster_path: str) -> str:
    return os.path.join(meta_util.get_cluster_path(cluster_path), ".gitignore")


def has_gitignore_entry(cluster_path: str, entry: str):
    gitignore_path = get_gitignore_path(cluster_path)

    with open(gitignore_path, "r") as f:
        return any(x.strip() == entry for x in f.readlines())


def add_gitignore_entry(cluster_path: str, entry: str):
    gitignore_path = get_gitignore_path(cluster_path)

    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write(entry + "\n")
            return

    if not has_gitignore_entry(cluster_path, entry):
        with open(gitignore_path, "a") as f:
            f.write(entry + "\n")
