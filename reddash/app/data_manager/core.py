from cryptography.fernet import Fernet
from typing import Optional
from pathlib import Path
import json

from reddash import __version__


class CoreManager:
    """Manager for core Red Dashboard storage configuration"""

    def __init__(self, path: Optional[Path] = None):
        self.path = path
        self.file: Optional[Path] = None
        if self.path and (self.path / "core.json").exists():
            self.file = self.path / "core.json"

        self._data = {}

    def __getitem__(self, item):
        return self._data[item]

    def initialize_base_config(self, path: Optional[Path] = None):
        if not (self.path or path):
            raise ValueError(
                "A path must be specified in either class instantiation or in method parameter."
            )

        if path:
            self.path = path

        self.file = self.path / "core.json"
        try:
            self.file.touch(exist_ok=True)
        except PermissionError:
            raise PermissionError(f"You don't have permission to write to '{self.file}'.")

        default_data = {
            "version": __version__,
            "secret_key": Fernet.generate_key().decode(),
            "jwt_secret_key": Fernet.generate_key().decode(),
            "commands": [],
            "variables": {
                "bot": {
                    "name": "Red Discord Bot",
                    "avatar": "/static/assets/img/cog.png",
                    "id": 0,
                    "clientid": 0,
                    "info": (
                        "Hey there! Welcome to this fresh instance of Red-Dashboard! This is a "
                        "static page that's used when the dashboard hasn't made initial "
                        "connection to a Redbot. If you're following the guide, great!  Continue "
                        "forward with setting up your Redbot to get everything squared away!"
                    ),
                    "prefix": ["[p]"],
                    "owners": [],
                    "owner": "",
                },
                "oauth": {"redirect": "", "secret": "", "blacklisted": []},
                "ui": {
                    "support": "https://discord.gg/vQZTdB9",
                    "invite": "",
                    "stats": {
                        "servers": 0,
                        "text": 0,
                        "voice": 0,
                        "categories": 0,
                        "users": 0,
                        "uptime": "Connection not yet established.",
                    },
                },
            },
            "locked": False,
            "third_parties": {},
        }

        file = open(self.file, "w")
        json.dump(default_data, file)
        file.close()

    def load_settings(self, path: Optional[Path] = None):
        if not (path / "core.json").exists():
            raise ValueError(f"{path / 'core.json'} does not exist!")
        if path:
            self.path = path
            self.file = path / "core.json"

        try:
            core = open(self.file, "r")
        except PermissionError:
            raise PermissionError(f"I require read permissions in {self.path}.")
        try:
            self._data = json.load(core)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                "Core Configuration file is corrupt.  An instance reset is required."
            ) from e
        core.close()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._data:
                self._data[key] = value
            else:
                raise KeyError(f"{key} is not a valid key.")
        self.save()

    def save(self):
        try:
            f = open(self.file, "w")
        except PermissionError:
            raise PermissionError(f"I require write permissions in {self.path}.")
        json.dump(self._data, f)
        f.close()
