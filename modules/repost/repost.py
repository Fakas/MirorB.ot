from modules.miror_module import MirorModule
from modules.asslib import frame_util
from os import path
import random
import json


class Repost(MirorModule):
    mb_mod = True
    mb_import = True
    mb_name = "Repost"
    cfg = None
    cache = None
    dir = None

    mb_help = "Repost module, bullies people who submit reposts!"

    mb_default_config = {
        "hosts": ["youtube.com", "youtu.be", "twitter.com", "twimg.com"],
        "responses": ["nice repost, nerd", "REEEEEEEEEEEEEEEEpost", "hey, I've seen this one before",
                      "happy groundhog day", "what a blast from the past", "thank you for recycling"]
    }

    def __init__(self):
        self.cfg = self.get_config()
        self.dir = frame_util.get_directory()
        self.cache_path = path.join(self.dir, "link_cache.json")
        self.stats_path = path.join(self.dir, "stats.json")
        self.read_cache()
        self.mb_actions = {
            "on_message": {
                "check_post": self.check_post
            }
        }

    async def check_post(self, *_args, **kwargs):
        msg = kwargs["message"]
        client = kwargs["client"]
        content = msg.content
        for host in self.cfg["hosts"]:
            if host in content:
                words = content.split(' ')
                for word in words:
                    if host in word and word not in self.cache["whitelist"]:
                        if word in self.cache["posts"]:
                            stats = self.get_stats()
                            user_id = str(msg.author.id)
                            if user_id not in stats.keys():
                                stats.update({user_id: 0})
                            stats[user_id] += 1
                            self.update_stats(stats)
                            reply = random.choice(self.cfg["responses"])
                            await client.reply(msg, reply)
                        else:
                            self.cache["posts"].append(word)
                            self.update_cache()

    def read_cache(self):
        with open(self.cache_path, 'r') as cache_file:
            self.cache = json.load(cache_file)
            cache_file.close()

    def update_cache(self):
        if self.cache is None:
            self.read_cache()
        with open(self.cache_path, 'w') as cache_file:
            json.dump(self.cache, cache_file)
            cache_file.close()

    def get_stats(self):
        with open(self.stats_path, 'r') as stats_file:
            stats = json.load(stats_file)
            stats_file.close()
        return stats

    def update_stats(self, stats):
        with open(self.stats_path, 'w') as stats_file:
            json.dump(stats, stats_file)
            stats_file.close()
