import json
import aio_pika
import uuid
from modules.asslib import disp, messaging
from modules.miror_module import MirorModule


class RadioController(MirorModule):
    mb_mod = True
    mb_import = True
    mb_name = "Miror Radio Client"

    mb_default_config = {
        "radio_host": "localhost",
        "radio_queue": "Miror_Radio",
        "radio_reply_queue": "Miror_Radio_Reply_Miror_Bot",
        "radio_url": "https://miror.bot/radio"
    }

    mb_help = "Radio module, let the music play! \n\n" \
              "Listen in at https://www.miror.bot/radio \n" \
              "Commands: \n" \
              "__cmd__play <link> - Add a track to the playlist \n" \
              "__cmd__play <text> - Automatically search YouTube for a track to add to the playlist \n" \
              "__cmd__radio       - (Alias for __cmd__play) \n" \
              "__cmd__skip        - Skip to the next track in the playlist \n" \
              "__cmd__stop        - Stop the current track and empty the playlist"

    client = None
    msg_client = None
    parameters = None
    reply = None
    channel = None
    corr_id = None
    cfg = None
    queue_obj = None
    conn_failed = False
    conn_failed_text = "Error: Could not establish a connection to the message queue server! :/"

    def __init__(self):
        self.corr_id = str(uuid.uuid4())
        self.mb_actions = {
            "on_command": {
                "radio": self.play,
                "play": self.play,
                "skip": self.skip,
                "stop": self.stop
            },
            "on_ready": {
                "setup": self.startup
            }
        }

    async def startup(self, *_args, **kwargs):
        self.client = kwargs["client"]
        self.cfg = self.get_config()
        self.msg_client = messaging.AsyncClient(verbose=True)

        await self.setup_connection()

    async def setup_connection(self):
        try:
            await self.msg_client.connect()
        except ConnectionError:
            self.conn_failed = True
            disp(self.conn_failed_text)
            return False

        await self.msg_client.register_channel()
        await self.msg_client.register_queue(self.cfg["radio_queue"])

        return True

    async def reply_callback(self, message: aio_pika.IncomingMessage):
        async with message.process():
            msg = message.body.decode("utf-8")
            content = json.loads(msg)
            if "context" not in content:
                disp("Error: Radio response did not include a context value!")
                return
            if "reply" in content:
                text = content["reply"]
                chan_id, msg_id = content["context"]
            else:
                text = "Radio service returned an invalid response! :/"

            d_chan = await self.client.fetch_channel(chan_id)
            d_msg = await d_chan.fetch_message(msg_id)
            await self.client.reply(d_msg, text)

    async def send_command(self, instructions):
        queue = self.cfg["radio_queue"]
        reply = messaging.reply_args(self.cfg["radio_reply_queue"], self.reply_callback)
        await self.msg_client.send_json(instructions, queue, reply=reply)

    async def process_command(self, instructions, message):
        if self.conn_failed and not await self.setup_connection():
            await self.client.reply(message, self.conn_failed_text)
            return
        await self.send_command(instructions)

    async def play(self, *_args, **kwargs):
        message = kwargs["message"]
        author = kwargs["author"]
        words = kwargs["words"]

        respond = f":musical_note: {self.cfg['radio_url']} :musical_note:"
        if len(words) == 0:
            await self.client.reply(message, respond)
            return

        user_id = str(author.id)
        target = ' '.join(words)

        instructions = {
            "cmd": "enqueue",
            "target": target,
            "user": user_id,
            "context": [message.channel.id, message.id]
        }

        await self.process_command(instructions, message)

    async def skip(self, *_args, **kwargs):
        message = kwargs["message"]
        author = kwargs["author"]

        user_id = str(author.id)

        instructions = {
            "cmd": "skip",
            "target": None,
            "user": user_id,
            "context": [message.channel.id, message.id]
        }

        await self.process_command(instructions, message)

    async def stop(self, *_args, **kwargs):
        message = kwargs["message"]
        author = kwargs["author"]

        user_id = str(author.id)

        instructions = {
            "cmd": "stop",
            "target": None,
            "user": user_id,
            "context": [message.channel.id, message.id]
        }

        await self.process_command(instructions, message)


controller = RadioController()
