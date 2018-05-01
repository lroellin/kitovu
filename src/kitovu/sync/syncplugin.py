"""Loading and handling of sychronization plugins."""

import abc
import pathlib
import typing

from kitovu import utils


class AbstractSyncPlugin(metaclass=abc.ABCMeta):

    """The specification/"interface" a synchronization plugin implements.

    Every abstract method in this class is a plugin hook.
    """

    NAME: typing.Optional[str] = None

    def __init__(self, reporter: utils.AbstractReporter) -> None:
        self.reporter: utils.AbstractReporter = reporter

    @abc.abstractmethod
    def configure(self, info: typing.Dict[str, typing.Any]) -> None:
        """Read a configuration section intended for this plugin."""
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self) -> None:
        """Connect to the host given via 'configure'.

        This should raise an appropriate exception if the connection failed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def disconnect(self) -> None:
        """Close any open connection."""
        raise NotImplementedError

    @abc.abstractmethod
    def create_local_digest(self, path: pathlib.Path) -> str:
        """Create a digest for the given local file."""
        raise NotImplementedError

    @abc.abstractmethod
    def create_remote_digest(self, path: pathlib.PurePath) -> str:
        """Create a digest for the given remote file."""
        raise NotImplementedError

    @abc.abstractmethod
    def list_path(self, path: pathlib.PurePath) -> typing.Iterable[pathlib.PurePath]:
        """List all files recursively in the given remote path."""
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_file(self, path: pathlib.PurePath, fileobj: typing.IO[bytes]) -> None:
        """Retrieve the given remote file."""
        raise NotImplementedError

    @abc.abstractmethod
    def connection_schema(self) -> typing.Dict[str, typing.Any]:
        """Returns a jsonschema to check for required properties passed to the configure method."""
        raise NotImplementedError
