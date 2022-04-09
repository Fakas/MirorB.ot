import logging
import feedparser
from modules.miror_module import get_json, set_json
from .consumer import Consumer

CACHE_NAME = "news_cache_rss"


class RSSConsumer(Consumer):
    async def _consume(self, client):
        print("Consuming RSS feeds...")
        cache = get_json(CACHE_NAME, [])

        channel = await client.fetch_channel(self.channel_id)
        for url, options in self.feeds.items():
            # Get customised feed metadata
            identifier = options.get("identifier", None)
            if not identifier:
                logging.error("No identifier for feed %s", url)
            header = options.get("header", None)
            text = options.get("text", None)
            link = options.get("link", None)
            include = options.get("include", [])
            exclude = options.get("exclude", [])
            buffer = options.get("buffer", 0)

            # Get published items
            feed = feedparser.parse(url)
            entries = feed["entries"]

            # Filter received items
            if include:
                for keyword in include:
                    entries = [entry for entry in entries if keyword in entry["title"]]
            if exclude:
                for keyword in exclude:
                    entries = [entry for entry in entries if keyword not in entry["title"]]
            if buffer and len(entries) > buffer:
                entries = entries[:buffer]

            # Process each item into something we can post
            for entry in entries:
                if entry[identifier] in cache:
                    # We've already processed this item, don't push it again
                    continue
                content = ""
                if header:
                    content += f"**{entry[header]}**\n"
                if text:
                    content += f"{entry[text]}\n"
                if link:
                    content += f"\n{entry[link]}"

                # Send the news item to the configured channel
                await channel.send(content)

                # Update the cache
                cache.append(entry[identifier])
                set_json(CACHE_NAME, cache)
