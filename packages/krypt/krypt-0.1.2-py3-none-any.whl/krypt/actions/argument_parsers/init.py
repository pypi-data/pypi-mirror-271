from krypt import parser

from krypt.actions.argument_parsers import ActionArgumentParser


class InitArgumentParser(ActionArgumentParser):
    def create(self, name):
        builder = parser.new(
            name,
            "Initialize a cluster directory for encrypted files.",
            "This command will create a new directory and generate a new key pair for encryption.",
        )

        return (
            builder.with_argument(
                "cluster_path", comment="Path to the directory to initialize"
            )
            .with_argument(
                "-p",
                "--passphrase",
                comment="The passphrase to use for private key encryption.",
                required=False,
            )
            .with_argument(
                "--no-passphrase",
                comment="Do not encrypt the private key. NOT RECOMMENDED!",
                action="store_true",
                required=False,
                default=False,
            )
            .with_argument(
                "--force",
                comment="Overwrite the existing key pair and sealed data."
                "ONLY USE IF YOU KNOW WHAT YOU'RE DOING!",
                action="store_true",
                required=False,
                default=False,
            )
            .with_argument(
                "--enable-gitignore",
                comment="Automatically add original files to .gitignore.",
                action="store_true",
                required=False,
                default=True,
            )
            .build()
        )
