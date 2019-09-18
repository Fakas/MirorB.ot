from .asslib.async_util import call


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

mb_mod = True
mb_import = True
mb_actions = {
    "on_command": {
        "echo": echo
    }
}
