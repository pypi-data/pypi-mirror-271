import json
import mimetypes
from functools import lru_cache
from pathlib import Path
from typing import List

from ._storage import JSON


@lru_cache
def _get_storage():
    from ._storage import Storage

    return Storage()


def list_assets() -> List[str]:
    """
    Retrieves a list of all asset names.

    Returns:
        A list of all asset names.
    """

    storage = _get_storage()
    return storage.list_assets()


def delete_asset(name: str):
    """
    Deletes the specified asset.

    Parameters:
        name: The name identifier of the asset to delete.
    """

    storage = _get_storage()
    storage.delete_asset(name)


def get_bytes(name: str) -> bytes:
    """
    Retrieves the specified asset as raw bytes.

    Parameters:
        name: The name identifier of the asset to retrieve.

    Returns:
        The raw byte content of the asset.
    """

    storage = _get_storage()
    return storage.get_bytes(name)


def get_file(name: str, path: str) -> str:
    """
    Downloads the specified asset and saves it to a file.

    Parameters:
        name: The name identifier of the asset to retrieve.
        path: The filesystem path where the file will be saved.

    Returns:
        The path to the saved file, confirming the operation's success.
    """

    storage = _get_storage()
    return storage.get_file(name, path)


def get_json(name: str) -> JSON:
    """
    Retrieves the specified asset and parses it as JSON.

    Parameters:
        name: The name identifier of the asset to retrieve.

    Returns:
        The parsed JSON data, which can be a dict, list, or primitive data type.
    """

    storage = _get_storage()
    return storage.get_json(name)


def get_text(name: str) -> str:
    """
    Retrieves the specified asset as a text string.

    Parameters:
        name: The name identifier of the asset to retrieve.

    Returns:
        The content of the asset as a text string.
    """

    storage = _get_storage()
    return storage.get_text(name)


def set_bytes(name: str, data: bytes, content_type="application/octet-stream"):
    """
    Uploads raw bytes as an asset.

    Parameters:
        name: The name identifier of the asset to upload.
        data: The raw byte content to upload.
        content_type: The MIME type of the asset.
    """

    storage = _get_storage()
    storage.set_bytes(name, data, content_type)


def set_file(name: str, path: str, content_type: str = None):
    """
    Uploads a file as an asset.

    Parameters:
        name: The name identifier of the asset to upload.
        path: The filesystem path of the file to upload.
        content_type: The MIME type of the asset.
    """

    content = Path(path).read_bytes()
    if content_type is None:
        content_type, _ = mimetypes.guess_type(path)
        if content_type is None:
            content_type = "application/octet-stream"

    storage = _get_storage()
    storage.set_bytes(name, content, content_type)


def set_json(name: str, value: JSON, **kwargs):
    """
    Uploads JSON data as an asset.

    Parameters:
        name: The name identifier of the asset to upload.
        value: The JSON data to upload.
        kwargs: Additional keyword arguments to pass to json.dumps.
    """

    content = json.dumps(value, **kwargs).encode("utf-8")
    content_type = "application/json"

    storage = _get_storage()
    storage.set_bytes(name, content, content_type)


def set_text(name: str, text: str):
    """
    Uploads text content as an asset.

    Parameters:
        name: The name identifier of the asset to upload.
        text: The text content to upload.
    """

    content = text.encode("utf-8")
    content_type = "text/plain"

    storage = _get_storage()
    storage.set_bytes(name, content, content_type)


__all__ = [
    "list_assets",
    "delete_asset",
    "get_bytes",
    "get_file",
    "get_json",
    "get_text",
    "set_bytes",
    "set_file",
    "set_json",
    "set_text",
]
