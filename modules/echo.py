from .default import call


async def echo(self, message, content, author, words, channel):
    # Delete and repost a message as ourselves
    if not await call(self.delete, message):
        return
    else:
        content = content[4::].strip()  # Remove "echo" and extraneous whitespace
        await self.reply(message, content)