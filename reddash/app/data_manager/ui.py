from typing import Optional
from pathlib import Path
import json


class UIManager:
    """Manager for UI Red Dashboard storage configuration"""

    def __init__(self, path: Optional[Path] = None):
        self.path = path
        self.file: Optional[Path] = None
        if self.path and (self.path / "ui.json").exists():
            self.file = self.path / "ui.json"

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

        self.file = self.path / "ui.json"
        try:
            self.file.touch(exist_ok=True)
        except PermissionError:
            raise PermissionError(f"You don't have permission to write to '{self.file}'.")

        default_data = {
            "sidebar": [
                {
                    "pos": 1,
                    "name": "builtin-home",
                    "icon": "icon-chart-pie-36",
                    "route": "base_blueprint.index",
                    "is_http": False,
                    "session": None,
                    "admin": False,
                    "locked": True,
                    "hidden": False,
                },
                {
                    "pos": 2,
                    "name": "builtin-commands",
                    "icon": "icon-molecule-40",
                    "route": "base_blueprint.commands",
                    "is_http": False,
                    "session": None,
                    "admin": False,
                    "locked": False,
                    "hidden": False,
                },
                {
                    "pos": 3,
                    "name": "builtin-dashboard",
                    "icon": "icon-controller",
                    "route": "dashboard_blueprint.dashboard",
                    "is_http": False,
                    "session": True,
                    "admin": False,
                    "locked": False,
                    "hidden": False,
                },
                {
                    "pos": 4,
                    "name": "builtin-credits",
                    "icon": "icon-book-bookmark",
                    "route": "base_blueprint.credits",
                    "is_http": False,
                    "session": None,
                    "admin": False,
                    "locked": True,
                    "hidden": False,
                },
                {
                    "pos": 5,
                    "name": "builtin-admin",
                    "icon": "icon-coins",
                    "route": "base_blueprint.admin",
                    "is_http": False,
                    "session": True,
                    "admin": True,
                    "locked": True,
                    "hidden": False,
                },
                {
                    "pos": 6,
                    "name": "builtin-login",
                    "icon": "icon-key-25",
                    "route": "base_blueprint.login",
                    "is_http": False,
                    "session": False,
                    "admin": False,
                    "locked": True,
                    "hidden": False,
                },
                {
                    "pos": 7,
                    "name": "builtin-logout",
                    "icon": "icon-user-run",
                    "route": "base_blueprint.logout",
                    "is_http": False,
                    "session": True,
                    "admin": False,
                    "locked": True,
                    "hidden": False,
                },
            ],
            "default_color": "red",
            "meta": {"title": "", "icon": "", "description": "", "color": ""},
        }

        ui = open(self.file, "w")
        json.dump(default_data, ui)
        ui.close()

    def load_settings(self, path: Optional[Path] = None):
        if not (path / "ui.json").exists():
            raise ValueError(f"{path / 'ui.json'} does not exist!")
        if path:
            self.path = path
            self.file = path / "ui.json"

        try:
            ui = open(self.file, "r")
        except PermissionError:
            raise PermissionError(f"I require read permissions in {self.path}.")
        try:
            self._data = json.load(ui)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                "UI Configuration file is corrupt.  An instance reset is required."
            ) from e
        ui.close()
