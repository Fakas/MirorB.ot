from modules.asslib.async_util import call
from modules.miror_module import MirorModule


class Echo(MirorModule):
    mb_mod = True
    mb_import = True
    mb_name = "Echo"

    mb_help = "Echo module, I talk back! \n\n" \
              "Commands: \n" \
              "__cmd__echo <text> - I'll repeat what you said"

    def __init__(self):
        self.mb_actions = {
            "on_command": {
                "echo": self.echo
            }
        }

    @staticmethod
    async def echo(*_args, **kwargs):
        client = kwargs["client"]
        message = kwargs["message"]
        content = kwargs["content"]
        # Delete and repost a message as ourselves
        if not await call(client.delete, message):
            return
        else:
            content = content[4::].strip()  # Remove "echo" and extraneous whitespace
            if content:
                await client.reply(message, content)
