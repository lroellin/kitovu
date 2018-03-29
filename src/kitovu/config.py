"""Storage and parsing of kitovu's configuration."""

import typing
import getpass

import keyring


def get_password(plugin: str, identifier: str) -> str:
    """Get the password for the given URL via keyring.

    Args:
       plugin: The name of the plugin requesting a password.
       identifier: An unique identifier (such as an URL) for the connection.
    """
    service = f'kitovu-{plugin}'
    password: typing.Optional[str] = keyring.get_password(service, identifier)
    if password is None:
        # FIXME handle this in a nicer way
        password = getpass.getpass()
        keyring.set_password(service, identifier, password)
    return password
