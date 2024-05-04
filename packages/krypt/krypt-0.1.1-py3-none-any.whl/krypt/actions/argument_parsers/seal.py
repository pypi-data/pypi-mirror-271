from krypt import parser

from krypt.actions.argument_parsers import ActionArgumentParser


class SealArgumentParser(ActionArgumentParser):
    def create(self, name):
        builder = parser.new(name, "Seal the cluster directory.")

        return (
            builder.with_argument(
                "cluster_path", comment="Path to the directory to seal"
            )
            .with_argument(
                "--append",
                comment="Append new files to the existing sealed data.",
                action="store_true",
                required=False,
                default=True,
            )
            .with_argument(
                "--remove-sealed",
                comment="Remove original files after sealing.",
                action="store_true",
                required=False,
                default=False,
            )
            .with_argument(
                "--overwrite-existing",
                comment="Overwrite files that already exist in the sealed archive.",
                action="store_true",
                required=False,
                default=False,
            )
            .build()
        )
