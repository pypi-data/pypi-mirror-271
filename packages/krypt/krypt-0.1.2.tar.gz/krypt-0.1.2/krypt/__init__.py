from krypt.actions import ActionManager

from krypt.actions.init import InitAction
from krypt.actions.preflight_checks.init import InitPreflightCheck
from krypt.actions.argument_parsers.init import InitArgumentParser

from krypt.actions.seal import SealAction
from krypt.actions.preflight_checks.seal import SealPreflightCheck
from krypt.actions.argument_parsers.seal import SealArgumentParser

from krypt.actions.unseal import UnsealAction
from krypt.actions.preflight_checks.unseal import UnsealPreflightCheck
from krypt.actions.argument_parsers.unseal import UnsealArgumentParser

action_manager = ActionManager()

action_manager.register(InitAction(), InitPreflightCheck(), InitArgumentParser())
action_manager.register(SealAction(), SealPreflightCheck(), SealArgumentParser())
action_manager.register(UnsealAction(), UnsealPreflightCheck(), UnsealArgumentParser())
