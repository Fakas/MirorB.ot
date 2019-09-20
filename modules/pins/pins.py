"""Pin-tracking Miror B.ot Module"""

from modules.miror_module import MirorModule


class Pins(MirorModule):
    """Pin-tracking Miror B.ot Module"""
    mb_mod = True
    mb_import = True
    mb_name = "Pins"

    mb_help = "Pins module, keeps track of the pin count! \n\n" \
              "Commands: \n" \
              "__cmd__pins - Display the current pin count for this channel"

    def __init__(self):
        self.mb_actions = {
            "on_guild_channel_pins_update": {
                "pins_update": self.pins_update
            },
            "on_command": {
                "pins": self.pins_cmd
            }
        }

    @staticmethod
    async def pins_update(*_args, **kwargs):
        channel = kwargs["channel"]
        pins = await channel.pins()
        await channel.send(f"{len(pins)}/50 Pins used!")

    async def pins_cmd(self, *_args, **kwargs):
        await self.pins_update(**kwargs)
