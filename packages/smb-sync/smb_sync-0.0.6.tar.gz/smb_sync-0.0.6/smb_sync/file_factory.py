"""
smb_sync.file_factory
"""

from typing import ContextManager
from urllib.parse import ParseResult, urlparse

from .file_base import FileContextManager
from .file_local import FileContextManagerLocal
from .file_samba import FileContextManagerSamba


def _create_file_context_manager_local(
    parsed_url: ParseResult,
) -> ContextManager[FileContextManagerLocal]:
    return FileContextManagerLocal(parsed_url.path)


def _create_file_context_manager_samba(
    parsed_url: ParseResult,
) -> ContextManager[FileContextManagerSamba]:
    name = parsed_url.path.split("/")[1]
    path = "/".join(parsed_url.path.split("/")[2:])

    return FileContextManagerSamba(
        username=parsed_url.username or "guest",
        password=parsed_url.password or "guest",
        name=name,
        path=path,
        host=parsed_url.hostname or "127.0.0.1",
        port=parsed_url.port or 445,
    )


def create_file_context_manager(url: str) -> ContextManager[FileContextManager]:
    """
    Creates file context manager.
    """
    parsed_url = urlparse(url)
    match parsed_url.scheme:
        case "smb":
            return _create_file_context_manager_samba(parsed_url)
        case "file":
            return _create_file_context_manager_local(parsed_url)
        case _:
            return _create_file_context_manager_local(parsed_url)
