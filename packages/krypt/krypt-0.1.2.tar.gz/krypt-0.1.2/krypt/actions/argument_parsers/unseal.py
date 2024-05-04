from krypt import parser

from krypt.actions.argument_parsers import ActionArgumentParser


class UnsealArgumentParser(ActionArgumentParser):
    def create(self, name):
        builder = parser.new(name, "Unseal the cluster directory.")

        return (
            builder.with_argument(
                "cluster_path", comment="Path to the directory to unseal"
            )
            .with_argument(
                "-p",
                "--passphrase",
                comment="The passphrase used for private key encryption.",
                required=False,
            )
            .with_argument(
                "--no-passphrase",
                comment="Assume the private key is not encrypted. NOT RECOMMENDED!",
                action="store_true",
                required=False,
                default=False,
            )
            .with_argument(
                "--remove-sealed",
                comment="Remove sealed files after unsealing.",
                action="store_true",
                required=False,
                default=False,
            )
            .with_argument(
                "--overwrite-existing",
                comment="Overwrite files that already exist in the cluster directory.",
                action="store_true",
                required=False,
                default=False,
            )
            .build()
        )
