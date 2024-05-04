import shutil

from krypt.actions import Action
from krypt.pki import keypair
from krypt.util import meta_util, git_util


def prompt_force(args):
    answer = input(
        "WARNING: This will overwrite the existing keypair and DESTROY the sealed data.\n"
        "Existing sealed data will be lost. THERE IS NO UNDO!\n"
        "Continue? [y/N]\n"
    )

    if answer.lower() in ["y", "yes"]:
        shutil.rmtree(meta_util.get_config_path(args.cluster_path))
        return True
    else:
        print("Aborted")
        return False


class InitAction(Action):
    def __init__(self):
        super().__init__("init")

    def run(self, args):
        if args.force and not prompt_force(args):
            return

        meta_util.init(args.cluster_path)

        key_pair = keypair.generate_key_pair(args.passphrase)

        meta_util.store_private_key(args.cluster_path, key_pair.get_private_bytes())
        meta_util.store_public_key(args.cluster_path, key_pair.get_public_bytes())

        if args.enable_gitignore:
            git_util.add_gitignore_entry(args.cluster_path, "**/*.kpt")
            git_util.add_gitignore_entry(args.cluster_path, "**/*.kpt.*")
