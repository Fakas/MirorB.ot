import os
from .asslib import disp


async def announce(*_args, force_announce=False, **kwargs):
    client = kwargs["client"]
    if client.vclient is None:
        return
    if "user_id" in kwargs.keys():
        user_id = kwargs["user_id"]
    elif "member" in kwargs.keys():
        # Play a user's announce sound
        user_id = kwargs["member"].id
    else:
        # Play our own announce sound
        user_id = client.user.id

    do_announce = False
    if force_announce:
        do_announce = True
    else:
        for member in client.vclient.channel.members:
            if member.id == user_id:
                do_announce = True
                break

    if not do_announce:
        return

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


async def announce_self(*args, **kwargs):
    kwargs.update({"member": kwargs["client"].user})
    await announce(*args, **kwargs)


async def announce_cmd(*args, **kwargs):
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

    await announce(*args, **kwargs, force_announce=True)


mb_mod = True
mb_import = True
mb_actions = {
    "on_command": {
        "announce": announce_cmd
    },
    "on_voice_join": {
        "announce": announce
    },
    "on_voice_join_self": {
        "announce_self": announce_self
    }
}
