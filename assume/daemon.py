import json
import os
import socket
from typing import Dict

from .constants import Constants
from .exceptions import AssumeDaemonError, AssumeValidationError
from .models import RequestModel
from .session import Session, SessionCache


class Client:
    def __init__(self, constants: Constants) -> None:
        self.constants = constants
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.client.connect(str(self.constants.socket_path))

    def send(self, request: Dict[str, str]) -> str:
        self.client.sendall(json.dumps(request).encode("utf-8"))
        return self.client.recv(1024).decode("utf-8")

    def close(self) -> None:
        self.client.close()


class Server:
    def __init__(self, constants: Constants, **kwargs) -> None:
        self.constants = constants
        self.cache = SessionCache(**kwargs)

        # remove the socket file if it already exists
        try:
            os.unlink(self.constants.socket_path)
        except OSError:
            if os.path.exists(self.constants.socket_path):
                raise AssumeDaemonError(
                    "Could not remove existing socket file: "
                    f"{self.constants.socket_path}"
                )

        # create the socket and listen for connections
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(str(self.constants.socket_path))
        self.server.listen(1)
        self.connection, self.client_address = self.server.accept()

    def add(self, config: str) -> None:
        try:
            self.cache[config] = Session(config)
        except Exception as e:
            raise AssumeDaemonError(
                f"Failed to add session for config: '{config}'"
            ) from e

    def credentials(self, config: str) -> bytes:
        if (session := self.cache.get(config)) is None:
            raise AssumeDaemonError(
                f"No session found for any config named '{config}'. "
                "You may need to initialize the session for that config first."
            )

        return json.dumps(session.credentials).encode("utf-8")

    def kill(self) -> None:
        self.connection.close()
        self.server.close()
        os.unlink(self.constants.socket_path)

    def list(self) -> bytes:
        try:
            return json.dumps(list(self.cache.keys())).encode("utf-8")
        except Exception as e:
            raise AssumeDaemonError("Failed to list sessions") from e

    def remove(self, config: str) -> None:
        try:
            del self.cache[config]
        except Exception as e:
            raise AssumeDaemonError(
                f"Failed to remove session for config: '{config}'"
            ) from e

    def run(self) -> None:
        try:
            while True:
                response: bytes = self.connection.recv(1024)

                if not response:
                    break

                _response: str = response.decode("utf-8")

                try:
                    request: Dict[str, str] = RequestModel.model_validate(
                        json.loads(_response)
                    ).model_dump(exclude_none=True)
                except Exception as e:
                    raise AssumeValidationError(
                        f"Invalid request: {_response}"
                    ) from e

                match action := request.pop("action"):
                    case "add":
                        self.add(**request)
                    case "credentials":
                        self.connection.sendall(self.credentials(**request))
                    case "kill":
                        self.kill()
                    case "list":
                        self.connection.sendall(self.list())
                    case "remove":
                        self.remove(**request)
                    case "whoami":
                        self.connection.sendall(self.whoami(**request))
                    case _:
                        raise AssumeDaemonError(f"Unknown action: '{action}'")

        finally:
            self.kill()

    def whoami(self, config: str) -> bytes:
        if (session := self.cache.get(config)) is None:
            raise AssumeDaemonError(
                f"No session found for any config named '{config}'. "
                "You may need to initialize the session for that config first."
            )

        return json.dumps(session.whoami()).encode("utf-8")
