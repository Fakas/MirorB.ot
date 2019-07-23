import traceback
import discord
from .asslib.is_async import is_async
from .asslib import disp


async def cmd(self, message):
    # Handle messages from commands
    author = message.author
    content = message.content[1::]  # Remove cmd char
    words = content.split(' ')
    word = words.pop(0).lower()  # First word for cmd
    cmds = {"echo": self.echo,
            "shutdown": self.shutdown,
            "announce": self.announce_cmd,
            "stop": self.stop,
            "radio": self.radio
            }

    if word in cmds.keys():  # Do we recognize the command?
        func = cmds[word]
        channel = message.channel
        try:
            await call(func, message, content, author, words, channel)  # Invoke command
        except SystemExit as err:
            raise SystemExit(err.code)
        except:
            disp(f"Unexpected error in cmd \"{word}\": ")
            traceback.print_exc()
            try:
                await self.reply(message, "Unexpected error, please check the log :/")
            except:
                disp("Was unable to send error message to Discord...")
                traceback.print_exc()


async def shutdown(self, message, *args):
    disp("Received shutdown command!")
    msg = self.cfg["shutdown_message"]
    await self.reply(message, msg)
    disp("Logging out from Discord...")
    try:
        await self.logout()
    except:
        pass
    disp("Goodbye!")


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
        disp("Tried to play audio but was not connected to a voice channel!")


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
            disp("Error: " + text)
            traceback.print_exc()
            await self.reply(obj, text)
        except:
            disp("Unexpected error while deleting a message:")
            traceback.print_exc()

    return False


async def reply(self, message, text):
    # Reply to a message in the same channel
    await message.channel.send(text)


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


def printmsg(message):
    # Print a message to the console
    msg = f"{message.author}: {message.content}"
    disp(msg)


async def call(func, *args):
    # No more await mistakes!
    if is_async(func):
        return await func(*args)
    else:
        return func(*args)

