import sys

from krypt import parser
from krypt import action_manager


def system_parser():
    builder = parser.new(
        "krypt",
        description="A helper tool for file encryption in Git repositories "
        "primarily aimed at encrypting Kubernetes secrets and "
        "other sensitive information to be later used in a "
        "CI/CD pipeline",
    )

    builder.with_subparsers(
        "action",
        group_description="Action",
        group_comment="The action to perform",
        parsers=action_manager.get_argument_parsers(),
    )

    return builder.build()


def launch():
    cmd_args = sys.argv[1:]

    args = system_parser().parse_args(cmd_args)

    action_manager.call_action(args.action, args)
