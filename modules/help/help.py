from modules.miror_module import MirorModule


class Help(MirorModule):
    mb_mod = True
    mb_import = True
    mb_name = "Help"
    mb_help = "Help module, gives access to module help strings! \n\n" \
              "Commands: \n" \
              "__cmd__help          - Return this help string! \n" \
              "__cmd__help modules  - Return a list of auto-loaded modules, use this to find available modules \n" \
              "__cmd__help <module> - Return the help string for a given module, use this to find usage and commands \n"

    def __init__(self):
        self.mb_actions = {
            "on_command": {
                "help": self.help_cmd
            }
        }

    async def help_cmd(self, *_args, **kwargs):
        words = kwargs["words"]
        channel = kwargs["channel"]
        client = kwargs["client"]

        if len(words) == 0:
            await self.show_help("help", channel, client)
        elif words[0] == "modules":
            await self.show_modules(channel, client)
        else:
            await self.show_help(words[0], channel, client)

    async def show_help(self, module_name, channel, client):
        module_name = module_name.lower()
        module_name.replace(' ', '_')

        modules = self.get_modules(client)
        cmd_prefix = client.cfg["cmd"]
        keys = modules.keys()
        for key in keys:
            new_key = key.lower()
            new_key.replace(' ', '_')
            if new_key == module_name:
                help_string = self.get_help(modules[new_key], cmd_prefix)
                await channel.send(f"```\n{help_string}\n```")
                return
        await channel.send("Could not find that module! :(")

    async def show_modules(self, channel, client):
        modules = self.get_modules(client)
        mods_string = "\n".join(modules.keys())
        mods_string = f"```\nHere are the loaded modules I found: \n{mods_string}\n```"
        await channel.send(mods_string)

    @staticmethod
    def get_modules(client):
        return client.modules

    @staticmethod
    def get_help(module, cmd_prefix):
        if module.mb_help is not None:
            return module.mb_help.replace("__cmd__", cmd_prefix)
        else:
            return "No help string available! :("
