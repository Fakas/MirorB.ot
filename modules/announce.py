import os
from .asslib import disp


async def announce(*_args, **kwargs):
    client = kwargs["client"]
    if "user_id" in kwargs.keys():
        # Play a user's announce sound
        user_id = kwargs["user_id"]
    else:
        # Play our own announce sound
        user_id = client.user.id

    user_id = str(user_id)
    announce_dir = client.cfg["announce"]
    # Get all files in directory
    files = [file for file in os.listdir(announce_dir) if os.path.isfile(os.path.join(announce_dir, file))]
    path = None
    for file in files:
        if user_id + '.' in file:
            path = os.path.join(announce_dir, file)
            break
    if path is None:
        # TODO Add default announce sound functionality
        disp(f"No announce sound for ID {user_id}")
    else:
        client.play(path)


async def announce_cmd(*_args, **kwargs):
    # Announce the user's or an arbitrary ID
    client = kwargs["client"]
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
    await announce(client, user_id=user_id)


mb_mod = True
mb_import = True
mb_actions = {
    "on_command": {
        "announce": announce_cmd
    },
    "on_voice_join": {
        "announce": announce
    }
}
