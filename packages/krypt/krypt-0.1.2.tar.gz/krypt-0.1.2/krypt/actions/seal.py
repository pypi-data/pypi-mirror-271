import os

from krypt.actions import Action

from krypt.pki import keypair, encryptor
from krypt.util import meta_util, path_util, zip_util


class SealAction(Action):
    def __init__(self):
        super().__init__("seal")

    def run(self, args):
        key_pair = keypair.load_public_key_pair(
            meta_util.read_public_key(args.cluster_path)
        )

        cluster_path = meta_util.get_cluster_path(args.cluster_path)

        for x in path_util.filter_contents(path_util.walk(cluster_path)):
            if (
                zip_util.exists(meta_util.get_data_path(args.cluster_path), x)
                and not args.overwrite_existing
            ):
                print(
                    "Skipping existing file:",
                    x,
                    "(use --overwrite-existing to overwrite)",
                )
                continue

            with open(os.path.join(cluster_path, x), "rb") as f:
                print("Sealing file:", x)

                data = f.read()
                encrypted_data = encryptor.encrypt(key_pair, data)

                zip_util.append(
                    meta_util.get_new_data_path(args.cluster_path), x, encrypted_data
                )

            if args.remove_sealed:
                print("Removing original file:", x)
                os.remove(os.path.join(cluster_path, x))

        if args.append:
            zip_util.merge(
                meta_util.get_data_path(args.cluster_path),
                meta_util.get_new_data_path(args.cluster_path),
            )

        if os.path.exists(meta_util.get_new_data_path(args.cluster_path)):
            os.rename(
                meta_util.get_new_data_path(args.cluster_path),
                meta_util.get_data_path(args.cluster_path),
            )
