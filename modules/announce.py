import os
from .asslib import disp

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
            path = os.path.join(dir, file)
            break
    if path is None:
        disp(f"No announce sound for ID {id}")
    else:
        self.play(path)


async def announce_cmd(self, message, content, author, words, *args):
    # Announce the user's or an arbitrary ID
    if len(words) > 0:
        target = words[0]
        if "<@!" in target:  # Camper has a weird @ID
            target = target[3:-1]
        if "<@" in target:
            target = target[2:-1]
        try:
            id = int(target)
        except:
            disp(f"{target} is not a valid integer and cannot be announced")
            return
    else:
        id = author.id
    await self.announce(id)


mb_mod = True
mb_import = True
mb_action = {
    {
        "cmd": {
            "announce": announce_cmd
        },
        "voice_join": {
            "announce": announce
        }

    }
}
