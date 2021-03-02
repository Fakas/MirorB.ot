"""Pin-tracking Miror B.ot Module"""

from modules.miror_module import MirorModule
from collections import OrderedDict
from discord import TextChannel, errors


class Pins(MirorModule):
    """Pin-tracking Miror B.ot Module"""
    mb_mod = True
    mb_import = True
    mb_name = "Pins"

    mb_help = "Pins module, keeps track of the pin count! \n\n" \
              "Commands: \n" \
              "__cmd__pins - Display the current pin leaderboard for a channel \n" \
              "__cmd__pin_count - Display the current pin count for a channel \n" \
              "__cmd__pin_leaderboard - Display the current pin count for the server"

    def __init__(self):
        self.mb_actions = {
            "on_guild_channel_pins_update": {
                "pins_update": self.pins_update
            },
            "on_command": {
                "pins": self.pins_cmd,
                "pins_count": self.count_cmd,
                "pin_count": self.count_cmd,
                "pins_leaderboard": self.leaderboard_cmd,
                "pin_leaderboard": self.leaderboard_cmd
            }
        }

    async def pins_update(*_args, **kwargs):
        channel = kwargs["channel"]
        pins = await get_pins(channel)
        await channel.send(format_count(pins))

    async def pins_cmd(self, *_args, **kwargs):
        client = kwargs["client"]
        message_channel = kwargs["channel"]
        if kwargs["words"]:
            channel_id = kwargs["words"][0].replace("<", "").replace(">", "").replace("#", "")
            channel = message_channel.guild.get_channel(channel_id)
            if not channel:
                channel = message_channel.guild.get_channel(int(channel_id))
        else:
            channel = message_channel

        pins = await get_pins(channel)
        text = await format_stats(generate_stats(pins), channel.name)
        text += f"\n{format_count(pins)}\n"
        await message_channel.send(text)

    async def count_cmd(self, *_args, **kwargs):
        await self.pins_update(**kwargs)

    async def leaderboard_cmd(self, *_args, **kwargs):
        message_channel = channel = kwargs["channel"]
        message = await message_channel.send("Working on it...")
        stats = await generate_leaderboard(channel.guild)
        text = await format_stats(stats, channel.guild.name)
        await message.edit(content=text)


def format_count(pins):
    return f"{len(pins)}/50 Pins used!"


async def format_stats(unsorted_stats, name):
    stats = sort_dict(unsorted_stats)
    if not stats:
        return ""
    text = "```\n"
    text += f"Pin Leaderboard for {name}\n\n"
    for user, count in stats.items():
        text += f"{user.display_name} - {count} \n"
    text += "```"
    return text


def generate_stats(pins):
    stats = {}
    for pin in pins:
        if pin.author not in stats:
            stats[pin.author] = 0
        stats[pin.author] += 1
    return stats


async def generate_leaderboard(guild):
    all_stats = {}
    for channel in guild.channels:
        if not isinstance(channel, TextChannel):
            continue
        try:
            pins = await channel.pins()
        except errors.Forbidden:
            continue
        all_stats[channel] = generate_stats(pins)

    leaderboard = {}
    for _, stats in all_stats.items():
        for user, count in stats.items():
            if user not in leaderboard:
                leaderboard[user] = 0
            leaderboard[user] += count

    return leaderboard


async def get_pins(channel):
    return await channel.pins()


def sort_dict(d):
    return OrderedDict({k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)})
