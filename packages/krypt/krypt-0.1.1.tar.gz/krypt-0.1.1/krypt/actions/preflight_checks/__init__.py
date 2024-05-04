import os
from abc import abstractmethod, ABC

from krypt.util import meta_util


class ActionPreflightCheck(ABC):
    def __call__(self, args):
        self.run(args)

    @abstractmethod
    def run(self, args):
        raise RuntimeError("Not implemented")


def common_check(args):
    if not os.path.exists(meta_util.get_cluster_path(args.cluster_path)):
        raise ValueError("Cluster path does not exist")
    if not os.path.isdir(meta_util.get_cluster_path(args.cluster_path)):
        raise ValueError("Cluster path is not a directory")

    if not os.path.exists(meta_util.get_config_path(args.cluster_path)):
        raise ValueError("Cluster directory has not been initialized yet")
