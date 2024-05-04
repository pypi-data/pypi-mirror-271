import os

from krypt.actions.preflight_checks import ActionPreflightCheck

from krypt.util import meta_util


class InitPreflightCheck(ActionPreflightCheck):
    def run(self, args):
        if not os.path.exists(meta_util.get_cluster_path(args.cluster_path)):
            raise ValueError("Cluster path does not exist")
        if not os.path.isdir(meta_util.get_cluster_path(args.cluster_path)):
            raise ValueError("Cluster path is not a directory")

        if not args.force and os.path.exists(
            meta_util.get_config_path(args.cluster_path)
        ):
            raise ValueError("Cluster directory has already been initialized")

        if args.no_passphrase:
            print(
                "WARNING: Private key will not be encrypted. This is not recommended!"
            )
            args.passphrase = None

        elif args.passphrase is None or args.passphrase == "":
            raise ValueError("Passphrase is required for private key encryption")
