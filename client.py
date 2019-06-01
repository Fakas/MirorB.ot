import discord
import json
import asyncio
import traceback

class Client(discord.Client):
    cfg = {}

    def __init__(self, jcfg):
        # Call parent __init__ before we continue
        super(Client, self).__init__()
        self.cfg = jcfg

    async def on_ready(self):
        # When logged in
        print("Logged in as {0}! ({1})".format(self.user.name, str(self.user.id)))

    async def on_message(self, message):
        # Handle message input
        printmsg(message)
        if message.content[0] == self.cfg["cmd"]:
            await self.cmd(message)

    async def cmd(self, message):
        # Handle messages from commands
        author = message.author
        content = message.content[1::] # Remove cmd char
        words = content.split(' ')
        word = words.pop(0).lower() # First word for cmd
        cmds = {"echo":self.echo,
                "shutdown":self.shutdown}

        if word in cmds.keys(): # Do we recognize the command?
            func = cmds[word]
            channel = message.channel
            try:
                await call(func, message, content, author, words, channel) # Invoke command
            except SystemExit as err:
                raise SystemExit(err.code)
            except:
                print("Unexpected error in cmd '{0}': ".format(word))
                traceback.print_exc()
                try:
                    await self.reply(message, "Unexpected error, please check the log :/")
                except:
                    print("Was unable to send error message to Discord...")
                    traceback.print_exc()

    async def shutdown(self, message, *args):
        print("Received shutdown command!")
        msg = self.cfg["shutdown_message"]
        await self.reply(message, msg)
        print("Logging out from Discord...")
        try:
            await self.logout()
        except:
            pass
        print("Goodbye!")
        raise SystemExit(0)

    async def echo(self, message, content, author, words, channel):
        # Delete and repost a message as ourselves
        if not await call(self.delete, message):
            return
        else:
            content = content[4::].strip() # Remove "echo" and extraneous whitespace
            await self.reply(message, content)

    async def delete(self, obj):
        # Delete something (probably a Discord object)
        if type(obj) is discord.Message:
            try:
                await obj.delete()
                return True
            except discord.Forbidden:
                text = "I don't have permissions to delete messages :/"
                print("Error: " + text)
                traceback.print_exc()
                await self.reply(obj, text)
            except:
                print("Unexpected error while deleting a message:")
                traceback.print_exc()

        return False

    async def reply(self, message, text):
        # Reply to a message in the same channel
        await message.channel.send(text)


def startup():
    # Prepare things before logging in
    with open("./config.json", 'r') as fp:
        jcfg = json.load(fp)
    client = Client(jcfg)
    client.run(jcfg["token"])


def printmsg(message):
    # Print a message to the console
    msg = "{0.author}: {0.content}".format(message)
    print(msg)


def isAsync(func):
    # Wrapper for asyncio.iscoroutine
    return asyncio.iscoroutinefunction(func) or asyncio.iscoroutine(func)


async def call(func, *args):
    # No more await mistakes!
    if isAsync(func):
        return await func(*args)
    else:
        return func(*args)



if __name__ == "__main__":
    # Don't auto startup if we're imported
    startup()