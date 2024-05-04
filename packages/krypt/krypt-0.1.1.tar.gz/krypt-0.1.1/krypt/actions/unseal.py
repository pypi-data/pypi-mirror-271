import os

from krypt.actions import Action
from krypt.pki import keypair, decryptor
from krypt.util import meta_util, zip_util


class UnsealAction(Action):
    def __init__(self):
        super().__init__("unseal")

    def run(self, args):
        key_pair = keypair.load_private_key_pair(
            meta_util.read_private_key(args.cluster_path), args.passphrase
        )

        cluster_path = meta_util.get_cluster_path(args.cluster_path)

        for x in zip_util.list_files(meta_util.get_data_path(args.cluster_path)):
            if (
                os.path.exists(os.path.join(cluster_path, x))
                and not args.overwrite_existing
            ):
                print(
                    "Skipping existing file:",
                    x,
                    "(use --overwrite-existing to overwrite)",
                )
                continue

            print("Unsealing file:", x)

            encrypted_data = zip_util.read_file(
                meta_util.get_data_path(args.cluster_path), x
            )
            data = decryptor.decrypt(key_pair, encrypted_data)

            with open(os.path.join(cluster_path, x), "wb") as f:
                f.write(data)

        if args.remove_sealed:
            print("Removing sealed files")
            os.remove(meta_util.get_data_path(args.cluster_path))
