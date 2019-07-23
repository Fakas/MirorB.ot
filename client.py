# import discord
import json
import asyncio

from modules.default import *
from modules.asslib import disp

# Main Client Module


class Client(discord.Client):
    cfg = {}
    vclient = None

    def __init__(self, jcfg):
        # Call parent __init__ before we continue
        super(Client, self).__init__()
        self.cfg = jcfg

    def run(self, token=None):
        if token is None:
            token = self.cfg["token"]
        return super(Client, self).run(token)

    async def on_ready(self):
        # When logged in
        report = f"Logged in as {self.user.name}! ({self.user.id})"
        disp(report)

    async def on_voice_state_update(self, member, before, after):
        # When a user changes their voice state
        if member.bot:
            # We don't care about bots
            return
        channels = member.guild.voice_channels
        users = []
        for channel in channels:
            members = channel.members
            count = 0
            if channel.id not in self.cfg["forbidden_channels"]:
                for user in members:
                    if not user.bot:
                        count += 1
            users.append(count)
        num = max(users)
        if num > 0:
            channel = channels[users.index(num)]
            join = await self.join_channel(channel)
            if not join and self.vclient is not None and after.channel == self.vclient.channel and after.channel is not None and before.channel != after.channel:
                await self.announce(member.id)
                pass


        elif self.vclient is not None:
            await self.leave_channel()

    async def on_message(self, message):
        # Handle message input
        printmsg(message)
        if message.content[0] == self.cfg["cmd"]:
            await self.cmd(message)


def startup():
    # Prepare things before logging in

    with open("./config.json", 'r') as fp:
        jcfg = json.load(fp)
        fp.close()

    discord.opus.load_opus("libopus.so.0")
    client = Client(jcfg)

    client.run()


if __name__ == "__main__":
    # Don't auto startup if we're imported
    startup()
