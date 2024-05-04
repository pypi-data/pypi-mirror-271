from importlib import import_module

from .unknown import command_unknown

COMMANDS = {}

for command in [
    "help",
    "newroom",
    "botinfo",
    "privacy",
    "addfeed",
    "listfeeds",
    "processfeeds",
    "removefeed",
]:
    function = getattr(import_module(
        "." + command, "matrix_rssbot.classes.commands"), "command_" + command)
    COMMANDS[command] = function

COMMANDS[None] = command_unknown
