"""Common Miror B.ot Module"""
import json
from os import path, getcwd, makedirs
from modules.asslib import frame_util, disp


class MirorModule(object):
    """Common Miror B.ot Module"""
    mb_mod = False  # Is this a module designed for use with Miror B.ot?
    mb_import = False  # Should this module and its actions be automatically loaded by Miror B.ot?
    mb_name = "__DefaultName__"
    mb_default_config = {}
    mb_help = None

    mb_actions = {  # All actions must be named with a key.
        "on_command": {  # "<Command key>": Command function, e.g. !echo = "echo": echo

        },
        "on_voice_join": {  # When a Member joins a voice channel

        },
        "on_voice_leave": {  # When a Member leaves a voice channel

        },
        "on_voice_state_update": {  # When a Member's voice state is updated

        },
        "on_voice_join_self": {  # When the bot joins a voice channel

        },
        "on_voice_leave_self": {  # When the bot leaves a voice channel

        },
        "on_guild_join": {  # When a new member joins the server

        },
        "on_guild_leave": {  # When a member leaves the server

        },
        "on_guild_update": {  # When a server is updated

        },
        "on_guild_available": {  # When a server becomes available to the bot

        },
        "on_guild_unavailable": {  # When a server becomes unavailable to the bot (usually due to Discord issues)

        },
        "on_guild_join_self": {  # When the bot joins a server

        },
        "on_guild_leave_self": {  # When the bot leaves a server

        },
        "on_connect": {  # When the bot successfully connects to Discord

        },
        "on_disconnect": {  # When the bot is disconnected from Discord (intended or otherwise)

        },
        "on_ready": {  # When the bot is ready to begin activities

        },
        "on_resumed": {  # When a suspended session is resumed

        },
        "on_error": {  # When an uncaught error occurs

        },
        "on_socket_raw_receive": {  # When any data is received through the Discord WebSocket, pre-processing.

        },
        "on_socket_raw_send": {  # When any data is sent through the Discord WebSocket, pre-processing.

        },
        "on_typing": {  # When a Member starts to type.

        },
        "on_message": {  # When a Discord message is received.

        },
        "on_message_self": {  # When the bot sends a Discord message.

        },
        "on_message_delete": {  # When an existing Discord message is deleted.

        },
        "on_bulk_message_delete": {  # When a bulk group of Discord messages are deleted.

        },
        "on_message_edit": {  # When a Discord message is edited.

        },
        "on_reaction_add": {  # When a reaction is added to a Discord message.

        },
        "on_reaction_remove": {  # When a reaction is removed from a Discord message.

        },
        "on_reaction_clear": {  # When all reactions are cleared from a Discord message.

        },
        "on_channel_create": {  # When a new Discord channel is created.

        },
        "on_channel_delete": {  # When an existing Discord channel is deleted.

        },
        "on_guild_channel_pins_update": {  # When the pins list of a Discord channel is updated.

        },
        "on_guild_integrations_update": {  # When a server's available integrations are updated.

        },
        "on_webhooks_update": {  # When a server's available webhooks are updated.

        },
        "on_member_update": {  # When a server Member is updated.

        },
        "on_user_update": {  # When a user's profile is updated.

        },
        "on_member_banned": {  # When an existing Member is banned from a server.

        },
        "on_member_unbanned": {  # When an existing Member is unbanned from a server.

        },
        "init": {  # When client initialisation happens

        },
        "tick": {  # Every X seconds

        }
    }

    def get_config(self, name=None):
        if name is None:
            return get_config(self)
        else:
            return get_config(name)


def get_config(target):
    """
    Get a config file for a given module.
    :param target: Target module
    :return: Config dict
    """
    name = get_name(target)
    config_path = get_config_path(name)
    if not path.exists(config_path):
        disp(f"Generating config file for module \"{name}\"...")
        set_config(name, target.mb_default_config)

    config_file = open(config_path, 'r')
    config = json.load(config_file)
    config_file.close()
    return config


def set_config(target, config):
    """
    Dump config dict to JSON config file
    :param target: Target module
    :param config: config dict
    """
    name = get_name(target)
    config_path = get_config_path(name)
    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=4)


def get_name(target):
    """
    Get a safe module name
    :param target: Target Miror B.ot module
    """
    if target is str:
        return target
    else:
        file_path = frame_util.get_class_file(target)
        name = path.split(file_path)
        name = path.splitext(name[1])
        name = name[0]
    return name


def get_config_path(name):
    """
    Get path to Miror B.ot config file
    :param name: Name of config file, without file extension
    :return: Absolute path to file
    """
    return path.join(make_config_dir(), f"{name}.json")


def make_config_dir():
    """
    Create a configuration directory if it doesn't exist
    :return: Absolute path to configuration directory
    """
    config_dir = path.join(getcwd(), "config")
    if not path.exists(config_dir):
        disp("No config directory exists, it will be created!")
        makedirs(config_dir)
    return config_dir


def is_module(obj):
    """
    Determine whether or not an object is a Miror B.ot Module
    :param obj: Object to test
    :return: True or False
    """
    return issubclass(obj, MirorModule)


def verify_module(mod):
    """
    Raise an exception if a given Miror B.ot Module does not meet basic requirements for auto-import
    :param mod: Miror B.ot Module
    :return: True if passes all checks, False if not designed for auto-import
    """
    if mod.mb_mod is False:
        return False
    if mod.mb_import is False:
        return False
    if mod.mb_name == "__DefaultName__" or mod.mb_name is None or mod.mb_name == "":
        raise NoNameException("Attempted to load a module that has no name or the default name!")
    return True


class MirorBotException(Exception):
    """Miror B.ot Exception class"""
    pass


class NoNameException(MirorBotException):
    """Missing name Exception class"""
    pass
