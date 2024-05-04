import argparse


class ParserBuilder(object):
    def __init__(self, name, description, comment=None):
        self.parser = argparse.ArgumentParser(
            prog=name, description=description, epilog=comment
        )

    def with_argument(self, *names, comment, required=True, default=None, action=None):
        if names[0].startswith("-"):  # workaround for positional arguments
            self.parser.add_argument(
                *names, help=comment, required=required, default=default, action=action
            )
            return self

        if not required:
            raise ValueError("Positional arguments can not be optional")

        self.parser.add_argument(*names, help=comment, default=default, action=action)

        return self

    def with_subparsers(
        self, group_name, group_description, group_comment, parsers, group_required=True
    ):
        subparsers = self.parser.add_subparsers(
            title=group_description,
            dest=group_name,
            help=group_comment,
            required=group_required,
        )

        for parser in parsers:
            subparsers.add_parser(
                parser.prog,
                description=parser.description,
                epilog=parser.epilog,
                parents=[parser],
                add_help=False,
            )

        return self

    def build(self):
        return self.parser


def new(name, description, comment=None):
    return ParserBuilder(name, description, comment)
