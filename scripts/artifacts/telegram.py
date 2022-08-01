import imp
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "./telegram"))

from teleparser_shim import parse_cache_db

__artifacts__ = {
    "Telegram": (
        "CacheDB",
        ("*/org.telegram.messenger/files/cache4.db*"),
        parse_cache_db,
    )
}
