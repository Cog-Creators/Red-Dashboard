import time
import websocket
import threading

from reddash.app.utils import initialize_websocket, secure_send, check_for_disconnect


class TaskManager:
    def __init__(self, app, console, progress):
        self.threads = []
        self.app = app
        self.console = console
        self.progress = progress

    def update_variables(self, method, task):
        self.progress.update(task, status="[bold green]Running[/bold green]")
        self.progress.refresh()

        try:
            while True:
                # Different wait times based on method, commands should be called less due to how much data it is
                if method == "DASHBOARDRPC__GET_VARIABLES":
                    time.sleep(self.app.interval)
                else:
                    time.sleep(self.app.interval * 2)

                if not self.app.running:
                    self.progress.update(task, status="[bold red]Killed[/bold red]")
                    self.progress.refresh()
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
                    self.app.variables = result["result"]
                    self.app.blacklisted = result["result"]["blacklisted"]
                else:
                    self.app.commanddata = result["result"]
                self.app.variables["disconnected"] = False
        except Exception as e:
            self.progress.update(task, status="[bold red]Stopped[/bold red]")
            self.progress.refresh()
            with self.console:
                if self.console.is_terminal:
                    self.console.print(self.progress._live_render.position_cursor())
                self.console.print_exception()
                if self.console.is_terminal:
                    self.console.print(self.progress._live_render)

    def update_version(self, task):
        self.progress.update(task, status="[bold green]Running[/bold green]")
        self.progress.refresh()

        try:
            while True:
                time.sleep(1)
                if not self.app.running:
                    self.progress.update(task, status="[bold red]Killed[/bold red]")
                    self.progress.refresh()
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

                        if (
                            result["result"]["v"] != self.app.rpcversion
                            and self.app.rpcversion != 0
                        ):
                            self.app.dashlog.warning(
                                "RPC websocket behind.  Closing and restarting..."
                            )
                            self.app.ws.close()
                            self.app.ws = websocket.WebSocket()
                            self.app.ws.connect(self.app.ws_url)
                        self.app.rpcversion = result["result"]["v"]
        except Exception as e:
            self.progress.update(task, status="[bold red]Stopped[/bold red]")
            self.progress.refresh()
            with self.console:
                if self.console.is_terminal:
                    self.console.print(self.progress._live_render.position_cursor())
                self.console.print_exception()
                if self.console.is_terminal:
                    self.console.print(self.progress._live_render)

    def check_if_connected(self, task):
        while True:
            if not self.app.running:
                self.app.ws.close()
                del self.app.ws
                self.progress.update(task, status="[bold red]Websocket Killed[/bold red]")
                self.progress.refresh()
                return
            time.sleep(0.1)
            if not (self.app.ws and self.app.ws.connected):
                self.progress.update(task, status="[bold red]Disconnected[/bold red]")
                self.progress.refresh()
            else:
                self.progress.update(task, status="[bold green]Connected[/bold green]")
                self.progress.refresh()

    def start_tasks(self, tasks):
        self.threads.append(
            threading.Thread(
                target=self.update_variables,
                args=["DASHBOARDRPC__GET_VARIABLES", tasks["var"]],
                daemon=True,
            )
        )
        self.threads.append(
            threading.Thread(
                target=self.update_variables,
                args=["DASHBOARDRPC__GET_COMMANDS", tasks["cmd"]],
                daemon=True,
            )
        )
        self.threads.append(
            threading.Thread(target=self.update_version, args=[tasks["ver"]], daemon=True)
        )
        self.threads.append(
            threading.Thread(target=self.check_if_connected, args=[tasks["con"]], daemon=True)
        )

        for t in self.threads:
            t.start()

    def stop_tasks(self):
        for t in self.threads:
            t.join()
