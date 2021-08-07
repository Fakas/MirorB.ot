"""Announce sounds module."""

import os
import time
from modules.asslib import disp
from modules.miror_module import MirorModule


class Announce(MirorModule):
    """Announce sounds Miror B.ot module"""
    mb_mod = True
    mb_import = True
    mb_name = "Announce"
    mb_default_config = {"announce_dir": "./announce/"}

    mb_help = "Announce module, plays announce sounds! \n\n" \
              "Change your announce sound at https://www.mirorbot.fakas.co.uk \n" \
              "Commands: \n" \
              "__cmd__announce <@user>     - Play someone's announce sound \n" \
              "__cmd__announce <User ID>   - Play an announce sound by user ID"

    def __init__(self, **_kwargs):
        self.mb_actions["on_command"] = {"announce": self.announce_cmd}
        self.mb_actions["on_voice_join"] = {"announce": self.announce}
        self.mb_actions["on_voice_join_self"] = {"announce": self.announce_self}
        self.cfg = self.get_config()
        self.announced = {}

    def should_announce(self, client, user_id, force_announce=False):
        do_announce = False
        if client.voice_client is None:
            return False
        elif force_announce:
            return True
        elif user_id in self.announced and time.time() < self.announced[user_id] + 60:
            return False
        else:
            for member in client.voice_client.channel.members:
                if member.id == user_id:
                    return True
        return do_announce

    async def announce(self, *_args, force_announce=False, **kwargs):
        client = kwargs["client"]
        if client.voice_client is None:
            return
        if "user_id" in kwargs.keys():
            user_id = kwargs["user_id"]
        elif "member" in kwargs.keys():
            # Play a user's announce sound
            user_id = kwargs["member"].id
        else:
            # Play our own announce sound
            user_id = client.user.id

        if not self.should_announce(client, user_id, force_announce=force_announce):
            return

        str_id = str(user_id)
        announce_dir = self.cfg["announce_dir"]
        # Get all files in directory
        files = [file for file in os.listdir(announce_dir) if os.path.isfile(os.path.join(announce_dir, file))]
        path = None
        for file in files:
            if str_id + '.' in file:
                path = os.path.join(announce_dir, file)
                break
        if path is None:
            # TODO Add default announce sound functionality (Fakas)
            disp(f"No announce sound for ID {str_id}")
        else:
            self.announced[user_id] = time.time()
            client.play(path)

    async def announce_self(self, *args, **kwargs):
        kwargs.update({"member": kwargs["client"].user})
        await self.announce(*args, **kwargs)

    async def announce_cmd(self, *args, **kwargs):
        # Announce the user's or an arbitrary ID
        author = kwargs["author"]
        words = kwargs["words"]

        if len(words) > 0:
            target = words[0]
            if "<@!" in target:  # Camper has a weird @ID
                target = target[3:-1]
            if "<@" in target:
                target = target[2:-1]
            try:
                user_id = int(target)
            except ValueError:
                disp(f"{target} is not a valid integer and cannot be announced")
                return
        else:
            user_id = author.id

        if user_id is not None:
            kwargs["user_id"] = user_id

        await self.announce(*args, **kwargs, force_announce=True)
