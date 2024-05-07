"""
smb_sync.file_local
"""

from os import listdir, makedirs, remove
from os.path import abspath, dirname, join, exists, isdir, getmtime, getsize
from shutil import copyfileobj, rmtree
from typing import IO

from .file_base import FileBase, FileContextManager


class FileLocal(FileBase):
    """
    File local.
    """

    _path: str

    def __init__(self, path: str) -> None:
        super().__init__()
        self._path = path

    def path(self) -> str:
        return self._path

    def url(self) -> str:
        return f"file://{abspath(self.path())}"

    def resolve(self, path: str) -> FileBase:
        return FileLocal(join(self.path(), path))

    def parent(self) -> FileBase:
        return FileLocal(dirname(self.path))

    def exists(self) -> bool:
        return exists(self.path())

    def is_directory(self) -> bool:
        return isdir(self.path())

    def make_directory(self) -> None:
        makedirs(self.path())

    def last_write_timestamp(self) -> float:
        return getmtime(self.path())

    def file_size_in_bytes(self) -> int:
        return getsize(self.path())

    def children(self) -> list[FileBase]:
        return [FileLocal(join(self.path(), file)) for file in listdir(self.path())]

    def read(self) -> IO[bytes]:
        return open(self.path(), "rb")

    def write(self, content: IO[bytes]) -> None:
        with open(self.path(), "wb") as file:
            copyfileobj(content, file)

    def remove(self) -> None:
        if self.is_directory():
            rmtree(self.path())
        else:
            remove(self.path())


class FileContextManagerLocal(FileContextManager):
    """
    File context manager local.
    """

    _path: str

    def __init__(self, _path: str) -> None:
        self._path = _path

    def entry(self) -> FileBase:
        return FileLocal(self._path)
