"""Game info Miror B.ot module"""

from modules.miror_module import MirorModule
from modules.asslib import callwebjson


class Games(MirorModule):
    """Game info Miror B.ot module"""
    mb_mod = True
    mb_import = True
    mb_name = "Games"

    mb_default_config = {
        "api_url": "https://games.api.serveymcserveface.com/"
    }

    mb_help = "Games module, displays game info! \n\n" \
              "Commands: \n" \
              "__cmd__games - Display game info"

    def __init__(self):
        self.cfg = self.get_config()
        self.mb_actions = {
            "on_command": {
                "games": self.games_cmd
            }
        }

    async def games_cmd(self, *_args, **kwargs):
        channel = kwargs["channel"]
        games = callwebjson(self.cfg["api_url"] + "all")
        for game_id in games.keys():
            game = games[game_id]
            title = game["server_name"] if game["online"] else f"{game_id} (Server offline)"
            game_name = game["game_name"]
            map_name = game["map_name"]
            players = game["player_count"]
            players_max = game["max_player_count"]
            info = f"**{title}** \n" \
                f"> Game: {game_name if game_name is not None else 'N/A'} \n" \
                f"> Map: {map_name if map_name is not None else 'N/A'} \n" \
                f"> Players: {f'{players}/{players_max}' if players is not None else 'N/A'} \n"
            await channel.send(info)
