import os

from krypt.actions.preflight_checks import ActionPreflightCheck, common_check
from krypt.util import meta_util


class SealPreflightCheck(ActionPreflightCheck):
    def run(self, args):
        common_check(args)

        if not os.path.exists(meta_util.get_public_key_path(args.cluster_path)):
            raise ValueError("Cluster directory seems to be corrupted")
