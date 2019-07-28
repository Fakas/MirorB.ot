import discord
import json
import traceback
from inspect import ismodule
from modules.asslib import disp, async_util, get_frame_name

import modules as mb_modules


# Main Client Module
class Client(discord.Client):
    cfg = {}
    vclient = None
    modules = {}

    def __init__(self, jcfg):
        # Call parent __init__ before we continue
        super(Client, self).__init__()
        self.cfg = jcfg

        self.load_modules()
        self.init_modules()

    def load_modules(self):
        everything = mb_modules.__dict__
        for key in everything.keys():
            if key[0] != '_' and ismodule(everything[key]):
                module = everything[key]
                grab = (hasattr(module, "mb_mod") and hasattr(module, "mb_import")) and (
                            module.mb_mod and module.mb_import)
                if grab:
                    self.modules.update({key: module})

    def init_modules(self):
        self.general_module_event("init", client=self)

    def general_module_event(self, event, *args, **kwargs):
        for key in self.modules.keys():
            module = self.modules[key]
            if event in module.mb_actions.keys():
                for func_name in module.mb_actions[event]:
                    func = module.mb_actions[event][func_name]
                    kwargs.update({"client": self})
                    func(*args, **kwargs)

    async def async_module_event(self, event, *args, **kwargs):
        for key in self.modules.keys():
            module = self.modules[key]
            if event in module.mb_actions.keys():
                for func_name in module.mb_actions[event]:
                    func = module.mb_actions[event][func_name]
                    kwargs.update({"client": self})
                    await async_util.call(func, *args, **kwargs)

    async def command_event(self, event, command, *args, **kwargs):
        for key in self.modules.keys():
            module = self.modules[key]
            if event in module.mb_actions.keys():
                for func_name in module.mb_actions[event]:
                    if func_name == command:
                        func = module.mb_actions[event][func_name]
                        kwargs.update({"client": self})
                        await async_util.call(func, *args, **kwargs)

    # Discord events

    async def on_connect(self):
        await self.async_module_event(get_frame_name())

    async def on_disconnect(self):
        await self.async_module_event(get_frame_name())

    async def on_ready(self):
        # When logged in
        report = f"Logged in as {self.user.name}! ({self.user.id})"
        disp(report)

        await self.async_module_event(get_frame_name())

    async def on_resumed(self):
        await self.async_module_event(get_frame_name())

    # noinspection PyBroadException
    async def on_error(self, event, *args, **kwargs):
        try:
            await super(Client, self).on_error(event, *args, **kwargs)
        except Exception:
            disp("Default error handling failed! Traceback:")
            traceback.print_exc()
        # noinspection PyBroadException
        try:
            await self.async_module_event(get_frame_name(), *args, **kwargs)
        except Exception:
            disp("Encountered an error in an on_error function! Traceback:")
            traceback.print_exc()

    async def on_socket_raw_receive(self, msg):
        await self.async_module_event(get_frame_name(), msg=msg)

    async def on_socket_raw_send(self, payload):
        await self.async_module_event(get_frame_name(), payload=payload)

    async def on_typing(self, channel, user, when):
        await self.async_module_event(get_frame_name(), channel=channel, user=user, when=when)

    async def on_message(self, message):
        # Handle message input
        await self.async_module_event(get_frame_name(), message=message)

        if message.content[0] == self.cfg["cmd"]:
            await self.cmd(message)

    async def on_message_delete(self, message):
        await self.async_module_event(get_frame_name(), message=message)

    async def on_bulk_message_delete(self, messages):
        await self.async_module_event(get_frame_name(), messages=messages)

    async def on_message_edit(self, before, after):
        await self.async_module_event(get_frame_name(), before=before, after=after)

    async def on_reaction_add(self, reaction, user):
        await self.async_module_event(get_frame_name(), reaction=reaction, user=user)

    async def on_reaction_remove(self, reaction, user):
        await self.async_module_event(get_frame_name(), reaction=reaction, user=user)

    async def on_reaction_clear(self, message, reactions):
        await self.async_module_event(get_frame_name(), message=message, reactions=reactions)

    async def on_guild_channel_delete(self, channel):
        await self.async_module_event(get_frame_name(), channel=channel)

    async def on_guild_channel_create(self, channel):
        await self.async_module_event(get_frame_name(), channel=channel)

    async def on_guild_channel_update(self, before, after):
        await self.async_module_event(get_frame_name(), before=before, after=after)

    async def on_guild_channel_pins_update(self, before, after):
        await self.async_module_event(get_frame_name(), before=before, after=after)

    async def on_guild_integrations_update(self, guild):
        await self.async_module_event(get_frame_name(), guild=guild)

    async def on_webhooks_update(self, channel):
        await self.async_module_event(get_frame_name(), channel=channel)

    async def on_member_join(self, member):
        await self.async_module_event(get_frame_name(), member=member)

    async def on_member_remove(self, member):
        await self.async_module_event(get_frame_name(), member=member)

    async def on_member_update(self, before, after):
        await self.async_module_event(get_frame_name(), before=before, after=after)

    async def on_user_update(self, before, after):
        await self.async_module_event(get_frame_name(), before=before, after=after)

    async def on_guild_join(self, guild):
        await self.async_module_event(get_frame_name(), guild=guild)

    async def on_guild_remove(self, guild):
        await self.async_module_event(get_frame_name(), guild=guild)

    async def on_guild_update(self, before, after):
        await self.async_module_event(get_frame_name(), before=before, after=after)

    async def on_guild_emojis_update(self, guild, before, after):
        await self.async_module_event(get_frame_name(), guild=guild, before=before, after=after)

    async def on_guild_available(self, guild):
        await self.async_module_event(get_frame_name(), guild=guild)

    async def on_guild_unavailable(self, guild):
        await self.async_module_event(get_frame_name(), guild=guild)

    async def on_member_ban(self, guild, user):
        await self.async_module_event(get_frame_name(), guild=guild, user=user)

    async def on_member_unban(self, guild, user):
        await self.async_module_event(get_frame_name(), guild=guild, user=user)

    async def on_voice_join(self, member, before, after):
        await self.async_module_event(get_frame_name(), member=member, before=before, after=after)

    async def on_voice_leave(self, member, before, after):
        await self.async_module_event(get_frame_name(), member=member, before=before, after=after)

    async def on_voice_join_self(self, channel):
        await self.async_module_event(get_frame_name(), channel=channel)

    async def on_voice_leave_self(self):
        await self.async_module_event(get_frame_name())

    async def on_voice_state_update(self, member, before, after):
        # When a user changes their voice state
        v_self = False
        if member.bot:  # TODO Should we have separate events for bots?
            if member.id != self.user.id:
                # We don't care about other bots
                return
            else:
                v_self = True

        if after.channel is not None and after.channel != before.channel:
            await self.on_voice_join(member, before, after)
        elif after.channel is None and before.channel is not None:
            await self.on_voice_leave(member, before, after)

        if not v_self:
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
                if not join and self.vclient is not None and after.channel == self.vclient.channel and \
                        after.channel is not None and before.channel != after.channel:
                    pass

            elif self.vclient is not None:
                await self.leave_channel()

    def run(self, token=None):
        if token is None:
            token = self.cfg["token"]
        return super(Client, self).run(token)

    async def shutdown(self, message, *_args):
        disp("Received shutdown command!")
        msg = self.cfg["shutdown_message"]
        await self.reply(message, msg)
        disp("Logging out from Discord...")
        await self.logout()
        disp("Goodbye!")

    def play(self, audio):
        if self.vclient is not None:
            self.stop()
            if type(audio) is str:
                audio = discord.FFmpegPCMAudio(audio)
            audio = discord.PCMVolumeTransformer(audio, volume=self.cfg["volume"])

            if self.vclient.is_playing() or self.vclient.is_paused():  # We check twice to avoid some race conditions
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
            except Exception as e:
                disp("Unexpected error while deleting a message:")
                raise e from None

        return False

    @staticmethod
    async def reply(message, text):
        # Reply to a message in the same channel
        await message.channel.send(text)

    async def join_channel(self, channel):
        # Join a voice channel if we're not already in it
        if self.vclient is not None and channel != self.vclient.channel:
            await self.vclient.move_to(channel)
        elif self.vclient is None:
            self.vclient = await channel.connect()
        else:
            return False

        await self.on_voice_join_self(channel)
        return True

    async def leave_channel(self):
        # Leave the current voice channel if we're in one
        await self.vclient.disconnect()
        self.vclient = None

        await self.on_voice_leave_self()

    async def cmd(self, message):
        # Handle messages from commands
        author = message.author
        content = message.content[1::]  # Remove cmd prefix character
        words = content.split(' ')
        word = words.pop(0).lower()  # First word for cmd

        channel = message.channel
        try:
            await self.command_event("on_command", word, message=message, content=content, author=author,
                                     words=words, channel=channel)
            # await call(func, message, content, author, words, channel)  # Invoke command
        except SystemExit as err:
            raise SystemExit(err.code)
        except Exception as e:
            try:
                await self.reply(message, "Unexpected error, please check the log :/")
            except Exception as ee:
                disp("Was unable to send error message to Discord...")
                raise ee from None
            disp(f"Unexpected error in cmd \"{word}\": ")
            raise e from None


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
