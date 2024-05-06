from os import listdir, makedirs, path, remove
from os.path import abspath, join
from shutil import copyfileobj, rmtree
from typing import IO

from .file_base import FileBase, FileContextManager


class FileLocal(FileBase):
    _path: str

    def __init__(self, path: str) -> None:
        super().__init__()
        self._path = path

    def Path(self) -> str:
        return self._path

    def Url(self) -> str:
        return f"file://{abspath(self.Path())}"

    def Resolve(self, path: str) -> FileBase:
        return FileLocal(join(self.Path(), path))

    def Exists(self) -> bool:
        return path.exists(self.Path())

    def IsDirectory(self) -> bool:
        return path.isdir(self.Path())

    def MakeDirectory(self) -> None:
        makedirs(self.Path())

    def LastWriteTimestamp(self) -> float:
        return path.getmtime(self.Path())

    def FileSizeInBytes(self) -> int:
        return path.getsize(self.Path())

    def Children(self) -> list[FileBase]:
        return [FileLocal(join(self.Path(), file)) for file in listdir(self.Path())]

    def Read(self) -> IO[bytes]:
        return open(self.Path(), "rb")

    def Write(self, content: IO[bytes]) -> None:
        with open(self.Path(), "wb") as file:
            copyfileobj(content, file)

    def Remove(self) -> None:
        if self.IsDirectory():
            rmtree(self.Path())
        else:
            remove(self.Path())


class FileContextManagerLocal(FileContextManager):
    _path: str

    def __init__(self, path: str) -> None:
        self._path = path

    def Entry(self) -> FileBase:
        return FileLocal(self._path)
