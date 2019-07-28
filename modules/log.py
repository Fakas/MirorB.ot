from .asslib import disp


def print_msg(*_args, **kwargs):
    message = kwargs["message"]
    # Print a message to the console
    msg = f"{message.author}: {message.content}"
    disp(msg)


def init(*_args, **_kwargs):
    disp("Logging module enabled!")


mb_mod = True  # Is this a module designed for use with Miror B.ot?
mb_import = True  # Should this module and its actions be automatically loaded by Miror B.ot?
mb_actions = {  # All actions must be named with a key.
    "on_message": {  # When a Discord message is received.
        "print_msg": print_msg
    },
    "init": {
        "init": init
    }
}
