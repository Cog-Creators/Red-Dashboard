from typing import Optional
from pathlib import Path
import appdirs
import logging
import sys
import os

from reddash.app.data_manager.core import CoreManager
from reddash.app.data_manager.ui import UIManager


class LoadManager:
    """Central class for loading Red Dashboard's configuration"""

    def __init__(self, instance: Optional[str] = None):
        self.instance = instance
        self.logger = logging.getLogger("reddash")

        self.config_dir: Optional[Path] = None
        self.base_dir: Optional[Path] = None
        appdir = appdirs.AppDirs("Red-Dashboard")
        if sys.platform == "linux":
            if 0 < os.getuid() < 1000:
                self.base_dir = Path(appdir.site_data_dir)

        if not self.base_dir:
            self.base_dir = Path(appdir.user_config_dir)

        self.core = CoreManager()
        self.ui = UIManager()

    def initialize(self):
        self.logger.debug("Initializing Load Manager")
        try:
            self.base_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise PermissionError(f"You don't have permission to write to '{self.base_dir}'.")

        children = [child for child in self.base_dir.iterdir()]

        if not children:
            self.config_dir = self.base_dir / "reddash"
            self.config_dir.mkdir()
            self.initialize_base_config(self.config_dir)
        elif self.instance and self.instance not in children:
            self.config_dir = self.base_dir / self.instance
            self.config_dir.mkdir()
            self.initialize_base_config(self.config_dir)
        elif len(children) == 1:
            self.config_dir = self.base_dir / children[0]
        elif self.instance:
            self.config_dir = self.base_dir / self.instance
        else:
            raise RuntimeError(
                "An instance must be specified with the --instance flag.  "
                "There are multiple instances registered for Red - Dashboard."
            )

        self.core.load_settings(self.config_dir)
        self.ui.load_settings(self.config_dir)

        self.logger.debug("Configuration managers ready.")

    def initialize_base_config(self, path: Path):
        self.logger.info("Detected new instance.  Initializing configuration")
        try:
            path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise PermissionError(f"You don't have permission to write to '{path}'.")

        self.core.initialize_base_config(path)
        self.ui.initialize_base_config(path)
