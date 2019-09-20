"""Logging Miror B.ot Module"""
from modules.asslib import disp
from modules.miror_module import MirorModule


class Log(MirorModule):
    """Logging Miror B.ot Module"""
    mb_mod = True  # Is this a module designed for use with Miror B.ot?
    mb_import = True  # Should this module and its actions be automatically loaded by Miror B.ot?
    mb_name = "Logging"

    mb_help = "Logging module, prints messages to the console, useful for debugging!"

    def __init__(self):
        self.mb_actions = {  # All actions must be named with a key.
            "on_message": {  # When a Discord message is received.
                "print_msg": self.print_msg
            },
            "init": {
                "init": self.init
            }
        }

    @staticmethod
    def print_msg(*_args, **kwargs):
        message = kwargs["message"]
        # Print a message to the console
        msg = f"{message.author}: {message.content}"
        disp(msg)

    @staticmethod
    def init(*_args, **_kwargs):
        disp("Logging module enabled!")
