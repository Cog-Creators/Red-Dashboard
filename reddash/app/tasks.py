from datetime import datetime
import time
import logging
import threading

from reddash.app.utils import initialize_websocket, secure_send, check_for_disconnect


class TaskManager:
    def __init__(self, app, console):
        self.logger = logging.getLogger("reddash")
        self.threads = []
        self.app = app
        self.console = console
        self.ignore_disconnect = False

    def update_variables(self, method):
        try:
            while True:
                # Different wait times, commands should be called less due to processing
                if method == "DASHBOARDRPC__GET_VARIABLES":
                    for _ in range(self.app.config["WEBSOCKET_INTERVAL"]):
                        time.sleep(1)
                        if not self.app.running:
                            return
                else:
                    for _ in range(self.app.config["WEBSOCKET_INTERVAL"] * 2):
                        time.sleep(1)
                        if not self.app.running:
                            return

                request = {"jsonrpc": "2.0", "id": 0, "method": method, "params": []}
                with self.app.lock:
                    # This needs to be inside the lock, or both threads will create a websocket
                    if not self.app.ws:
                        initialized = initialize_websocket(self.app)
                        if not initialized:
                            continue

                    result = secure_send(self.app, request)
                    if not result:
                        continue

                    connected = check_for_disconnect(self.app, method, result)
                    if not connected:
                        continue

                if method == "DASHBOARDRPC__GET_VARIABLES":
                    if not self.app.data.core["variables"].get("bot", {"id": None})["id"]:
                        self.logger.info("Initial connection made with Redbot.  Syncing data.")
                    self.app.data.core.update(variables=result["result"])
                else:
                    self.app.data.core.update(commands=result["result"])
                self.app.config["RPC_CONNECTED"] = True
        except Exception:
            self.logger.exception(f"Background task {method} died unexpectedly.")

    def update_version(self):
        version = 0
        try:
            while True:
                time.sleep(1)
                if not self.app.running:
                    return
                if self.app.ws and self.app.ws.connected:
                    request = {
                        "jsonrpc": "2.0",
                        "id": 0,
                        "method": "DASHBOARDRPC__CHECK_VERSION",
                        "params": [],
                    }
                    with self.app.lock:
                        if not self.app.ws:
                            initialized = initialize_websocket(self.app)
                            if not initialized:
                                continue

                        result = secure_send(self.app, request)
                        if not result:
                            continue

                        if "error" in result:
                            continue

                        if "disconnected" in result["result"]:
                            continue

                        if result["result"]["v"] != version and version != 0:
                            self.ignore_disconnect = True
                            self.logger.info("RPC websocket behind.  Closing and restarting...")
                            self.app.ws.close()
                            initialize_websocket(self.app)
                            self.ignore_disconnect = False
                        version = result["result"]["v"]
        except Exception:
            self.logger.exception("Background task DASHBOARDRPC__CHECK_VERSION died unexpectedly.")

    def check_if_connected(self):
        last_state_disconnected = True
        while True:
            if not self.app.running:
                try:
                    self.app.ws.close()
                    del self.app.ws
                except AttributeError:
                    pass
                self.logger.info("RPC Websocket closed")
                return

            time.sleep(0.1)

            if self.ignore_disconnect:
                continue

            if not (self.app.ws and self.app.ws.connected):
                if not last_state_disconnected:
                    self.logger.warning("Disconnected from RPC Websocket")
                    self.app.config["LAST_RPC_EVENT"] = datetime.utcnow()
                    last_state_disconnected = True
            else:
                if last_state_disconnected:
                    self.logger.info("Reconnected to RPC Websocket")
                    self.app.config["LAST_RPC_EVENT"] = datetime.utcnow()
                    last_state_disconnected = False

    def start_tasks(self):
        self.threads.append(
            threading.Thread(
                target=self.update_variables,
                args=["DASHBOARDRPC__GET_VARIABLES"],
                daemon=True,
            )
        )
        self.threads.append(
            threading.Thread(
                target=self.update_variables,
                args=["DASHBOARDRPC__GET_COMMANDS"],
                daemon=True,
            )
        )
        self.threads.append(threading.Thread(target=self.update_version, daemon=True))
        self.threads.append(threading.Thread(target=self.check_if_connected, daemon=True))

        for t in self.threads:
            t.start()

    def stop_tasks(self):
        for t in self.threads:
            t.join()
