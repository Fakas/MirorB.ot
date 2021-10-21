"""Newsfeed Miror B.ot Module"""
from modules.asslib.async_util import call
from modules.miror_module import MirorModule
from .rss import RSSConsumer


class News(MirorModule):
    """Newsfeed Miror B.ot Module"""
    mb_mod = True
    mb_import = True
    mb_name = "News"
    mb_help = "News module, No one cares!"
    mb_default_config = {"channel": "CHANGEME", "rss": {}}

    def __init__(self):
        self.cfg = self.get_config()
        self.rss_consumer = RSSConsumer(self.cfg["rss"], self.cfg["channel"])
        self.mb_actions = {
            "tick": {
                "rss": self.rss_consumer.consume
            }
        }
