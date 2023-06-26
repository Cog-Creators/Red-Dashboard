import threading
import websocket


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
    "en",
    "af_ZA",
    "ar_SA",
    "bg_BG",
    "ca_ES",
    "cs_CZ",
    "da_DK",
    "de_DE",
    "el_GR",
    "es_ES",
    "fi_FI",
    "fr_FR",
    "he_IL",
    "hu_HU",
    "id_ID",
    "it_IT",
    "ja_JP",
    "ko_KR",
    "nl_NL",
    "nb_NO",
    "pl_PL",
    "pt_BR",
    "pt_PT",
    "ro_RO",
    "ru_RU",
    "sk_SK",
    "sv_SE",
    "tr_TR",
    "uk_UA",
    "vi_VN",
    "zh_CN",
    "zh_HK",
    "zh_TW",
]

AVAILABLE_COLORS = [
    {"name": "red", "class": "badge-red"},
    {"name": "primary", "class": "badge-primary"},
    {"name": "blue", "class": "badge-info"},
    {"name": "green", "class": "badge-success"},
    {"name": "darkgreen", "class": "badge-darkgreen"},
    {"name": "yellow", "class": "badge-yellow"},
]
