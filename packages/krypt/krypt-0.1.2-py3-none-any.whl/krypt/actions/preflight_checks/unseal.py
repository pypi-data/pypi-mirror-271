import os

from krypt.actions.preflight_checks import ActionPreflightCheck, common_check
from krypt.util import meta_util


class UnsealPreflightCheck(ActionPreflightCheck):
    def run(self, args):
        common_check(args)

        if not os.path.exists(meta_util.get_private_key_path(args.cluster_path)):
            raise ValueError("Cluster directory seems to be corrupted")
        if not os.path.exists(meta_util.get_data_path(args.cluster_path)):
            raise ValueError("Cluster directory does not seem to be sealed")

        if args.passphrase is None and not args.no_passphrase:
            raise ValueError("Passphrase is required for private key decryption")
