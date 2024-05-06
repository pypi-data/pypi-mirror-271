from smb_sync.file_base import FileContextManager
from smb_sync.file_local import FileContextManagerLocal
from smb_sync.file_samba import FileContextManagerSamba
from typing import ContextManager
from urllib.parse import ParseResult, urlparse


def _CreateFileContextManagerLocal(
    parsed_url: ParseResult,
) -> ContextManager[FileContextManagerLocal]:
    return FileContextManagerLocal(parsed_url.path)


def _CreateFileContextManagerSamab(
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


def CreateFileContextManager(url: str) -> ContextManager[FileContextManager]:
    parsed_url = urlparse(url)
    match parsed_url.scheme:
        case "smb":
            return _CreateFileContextManagerSamab(parsed_url)
        case "file":
            return _CreateFileContextManagerLocal(parsed_url)
        case _:
            return _CreateFileContextManagerLocal(parsed_url)
