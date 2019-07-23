import discord
import json
import asyncio
import traceback
import os
import socket

# Main Client Module

class Client(discord.Client):
    cfg = {}
    vclient = None
    def __init__(self, jcfg):
        # Call parent __init__ before we continue
        super(Client, self).__init__()
        self.cfg = jcfg

    async def on_ready(self):
        # When logged in
        print("Logged in as {0}! ({1})".format(self.user.name, str(self.user.id)))

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

    async def join_channel(self, channel):
        # Join a voice channel if we're not already in it
        if self.vclient is not None and channel != self.vclient.channel:
            await self.vclient.move_to(channel)
        elif self.vclient is None:
            try:
                self.vclient = await channel.connect()
            except discord.errors.ClientException:
                self.vclient.move_to(channel)
        else:
            return False

        if self.vclient is not None:
            await self.announce()
        return True

    async def leave_channel(self):
        # Leave the current voice channel if we're in one
        await self.vclient.disconnect()
        self.vclient = None

    async def cmd(self, message):
        # Handle messages from commands
        author = message.author
        content = message.content[1::] # Remove cmd char
        words = content.split(' ')
        word = words.pop(0).lower() # First word for cmd
        cmds = {"echo":self.echo,
                "shutdown":self.shutdown,
                "announce":self.announce_cmd,
                "stop": self.stop,
                "radio": self.radio
                }

        if word in cmds.keys(): # Do we recognize the command?
            func = cmds[word]
            channel = message.channel
            try:
                await call(func, message, content, author, words, channel) # Invoke command
            except SystemExit as err:
                raise SystemExit(err.code)
            except:
                print("Unexpected error in cmd '{0}': ".format(word))
                traceback.print_exc()
                try:
                    await self.reply(message, "Unexpected error, please check the log :/")
                except:
                    print("Was unable to send error message to Discord...")
                    traceback.print_exc()

    async def shutdown(self, message, *args):
        print("Received shutdown command!")
        msg = self.cfg["shutdown_message"]
        await self.reply(message, msg)
        print("Logging out from Discord...")
        try:
            await self.logout()
        except:
            pass
        print("Goodbye!")


    async def echo(self, message, content, author, words, channel):
        # Delete and repost a message as ourselves
        if not await call(self.delete, message):
            return
        else:
            content = content[4::].strip() # Remove "echo" and extraneous whitespace
            await self.reply(message, content)

    async def announce_cmd(self, message, content, author, words, *args):
        # Announce the user's or an arbitrary ID
        if len(words) > 0:
            target = words[0]
            if "<@!" in target: # Camper has a weird @ID
                target = target[3:-1]
            if "<@" in target:
                target = target[2:-1]
            try:
                id = int(target)
            except:
                print("{0} is not a valid integer and cannot be announced".format(target))
                return
        else:
            id = author.id
        await self.announce(id)

    async def announce(self, id=None):
        # Play a user's announce sound
        if id is None:
            # Play our own announce sound
            id = self.user.id
        id = str(id)
        dir = self.cfg["announce"]
        # Get all files in directory
        files = [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]
        path = None
        for file in files:
            if id + '.' in file:
                path = os.path.join(dir,file)
                break
        if path is None:
            print("No announce sound for ID {0}".format(id))
        else:
            self.play(path)

    async def radio(self, message, content, author, words, channel, *args):
        respond = f":musical_note: {self.cfg['radio_url']} :musical_note:"
        if len(words) == 0:
            await self.reply(message, respond)
            return
        
        id = str(author.id)
        target = words[0]

        host = self.cfg["radio_host"]
        port = self.cfg["radio_port"]
        prefix = self.cfg["radio_prefix"]

        instructions = {
            "cmd": "enqueue",
            "target": target,
            "user": id
        }

        instruct = f"{prefix}:{json.dumps(instructions)}".encode("utf-8")

        sock = socket.socket()
        try:
            sock.connect((host, port))
            sock.send(instruct)
        except Exception:
            await self.reply(message, "Couldn't connect to the Miror Radio service :/")
        sock.close()

        await self.reply(message, respond)


    def play(self, audio):
        if self.vclient is not None:
            self.stop()
            if type(audio) is str:
                audio = discord.FFmpegPCMAudio(audio)
            audio = discord.PCMVolumeTransformer(audio,volume=self.cfg["volume"])

            if self.vclient.is_playing() or self.vclient.is_paused(): # We check twice to avoid some race conditions
                self.vclient.stop()
            self.vclient.play(audio)
        else:
            print("Tried to play audio but was not connected to a voice channel!")

    def stop(self):
        if self.vclient is not None:
            self.vclient.stop()

    async def delete(self, obj):
        # Delete something (probably a Discord object)
        if type(obj) is discord.Message:
            try:
                await obj.delete()
                return True
            except discord.Forbidden:
                text = "I don't have permissions to delete messages :/"
                print("Error: " + text)
                traceback.print_exc()
                await self.reply(obj, text)
            except:
                print("Unexpected error while deleting a message:")
                traceback.print_exc()

        return False

    async def reply(self, message, text):
        # Reply to a message in the same channel
        await message.channel.send(text)

    async def restart(self, message, *args):
        global reboot
        reboot = True
        await self.shutdown(message)


def startup():
    # Prepare things before logging in
    global reboot

    reboot = False
    autorestart = True
    reboot = False
    while autorestart or reboot:
        with open("./config.json", 'r') as fp:
            jcfg = json.load(fp)
        autorestart = jcfg["autorestart"]
        discord.opus.load_opus("libopus.so.0")
        client = Client(jcfg)
        if reboot:
            asyncio.set_event_loop(asyncio.new_event_loop())
            reboot = False
        client.run(jcfg["token"])


def printmsg(message):
    # Print a message to the console
    msg = "{0.author}: {0.content}".format(message)
    print(msg)


def isAsync(func):
    # Wrapper for asyncio.iscoroutine
    return asyncio.iscoroutinefunction(func) or asyncio.iscoroutine(func)


async def call(func, *args):
    # No more await mistakes!
    if isAsync(func):
        return await func(*args)
    else:
        return func(*args)


reboot = False
if __name__ == "__main__":
    # Don't auto startup if we're imported
        startup()