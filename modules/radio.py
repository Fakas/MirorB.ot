import json
import socket


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