import threading
import websocket

__version__ = "0.1.5a.dev"
__author__ = "Neuro Assassin#4779"


class Lock:
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, *args):
        self.lock.release()


DEFAULTS = {
    "botname": "Red Discord Bot",
    "botavatar": "https://cdn.discordapp.com/icons/133049272517001216/a_aab012f3206eb514cac0432182e9e9ec.gif?size=1024",
    "botinfo": "Hello, welcome to the Red Discord Bot dashboard!  Here you can see basic information, commands list and even interact with your bot!  Unfortunately, this dashboard is not connected to any bot currently, so none of these features are available.  If you are the owner of the bot, please load the dashboard cog from Toxic Cogs.",
    "owner": "Cog Creators",
    "color": "red",
}

WS_URL = "ws://localhost:"
WS_EXCEPTIONS = (
    ConnectionRefusedError,
    websocket._exceptions.WebSocketConnectionClosedException,
    ConnectionResetError,
    ConnectionAbortedError,
)

ALLOWED_LOCALES = [
    "af",
    "ar",
    "bg",
    "ca",
    "cs",
    "da",
    "de",
    "el",
    "en",
    "es_es",
    "fi",
    "fr",
    "he",
    "hu",
    "id",
    "it",
    "ja",
    "ko",
    "nl",
    "no",
    "pl",
    "pt_br",
    "pt_pt",
    "ro",
    "ru",
    "sk",
    "sr",
    "sv_se",
    "tr",
    "uk",
    "vi",
    "zh_cn",
    "zh_hk",
    "zh_tw",
]
