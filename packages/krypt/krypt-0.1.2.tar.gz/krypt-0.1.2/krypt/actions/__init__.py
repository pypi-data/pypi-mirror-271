from abc import abstractmethod, ABC


class Action(ABC):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __call__(self, args):
        self.run(args)

    @abstractmethod
    def run(self, args):
        raise RuntimeError("Not implemented")


class RegisteredAction(object):
    def __init__(self, action, preflight_check, argument_parser):
        self.action = action
        self.preflight_check = preflight_check
        self.argument_parser = argument_parser

    def get_action(self):
        return self.action

    def get_preflight_check(self):
        return self.preflight_check

    def get_argument_parser(self):
        return self.argument_parser


class ActionManager(object):
    def __init__(self):
        self.actions = {}

    def register(self, action, preflight_check, argument_parser):
        self.actions[action.name] = RegisteredAction(
            action, preflight_check, argument_parser
        )

    def unregister(self, name):
        self.actions.pop(name, None)

    def call_action(self, name, args):
        if name not in self.actions:
            raise ValueError("Action not found")

        action = self.actions[name].get_action()
        preflight_check = self.actions[name].get_preflight_check()

        preflight_check.run(args)
        action.run(args)

    def get_argument_parsers(self):
        return [
            x.get_argument_parser().create(name) for name, x in self.actions.items()
        ]
