"""Dummy plugin so that we can separately test kitovu and the plugin architecture."""

from kitovu.sync import syncplugin
import pathlib
import typing
import time
import hashlib

class DummyPlugin(syncplugin.AbstractSyncPlugin):

    """provides fake connection info with hard-coded credentials for testing."""

    connection_state: typing.Optional[bool] = False

    def configure(self, info: typing.Dict[str, typing.Any]) -> None:
        self._info.username = info.get("username", "legger")
        self._info.password = info.get("password", "swordfish")
        self._info.hostname = info.get("hostname", "localhost")
        self._info.port = info.get("port", 8000)

    def connect(self) -> None:
            self.connection_state = True
            print("connection established")

    def disconnect(self) -> None:
            self.connection_state = False
            print("connection closed")

    def create_local_digest(self, path: pathlib.Path) -> str:
        return hashlib.sha256(path.lstat().st_size + time.strftime("%d/%m/%Y"))

    def create_remote_digest(self, path: pathlib.PurePath) -> str:
        return hashlib.sha256(path.lstat().st_size + time.strftime("%d/%m/%Y"))

    def list_path(self, path: pathlib.PurePath) -> typing.Iterable[pathlib.PurePath]:
        return path.parent()

    def retrieve_file(self, path: pathlib.PurePath, fileobj: typing.IO[bytes]) -> None:
        pass

