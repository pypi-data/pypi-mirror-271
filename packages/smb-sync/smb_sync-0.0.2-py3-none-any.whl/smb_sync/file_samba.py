from io import BytesIO
from os.path import join
from smb.base import OperationFailure, SharedFile
from smb.SMBConnection import SMBConnection
from typing import IO, Self

from .file_base import FileBase, FileContextManager


class FileSamba(FileBase):
    _base_url: str
    _name: str
    _path: str
    _conn: SMBConnection

    def __init__(self, base_url: str, name: str, path: str, conn: SMBConnection):
        self._base_url = base_url
        self._name = name
        self._path = path
        self._conn = conn

    def Path(self) -> str:
        return self._path

    def Url(self) -> str:
        return f"{self._base_url}/{self.Path()}"

    def Resolve(self, path: str) -> Self:
        return FileSamba(
            self._base_url, self._name, join(self.Path(), path), self._conn
        )

    def _Stat(self) -> SharedFile | None:
        try:
            return self._conn.getAttributes(self._name, self.Path())
        except OperationFailure:
            return None

    def Exists(self) -> bool:
        return self._Stat() != None

    def IsDirectory(self) -> bool:
        stat = self._Stat()
        return stat != None and stat.isDirectory

    def MakeDirectory(self) -> Self:
        current_path = ""
        for directory in self.Path().strip("/").split("/"):
            current_path = join(current_path, directory)
            current_file = FileSamba(
                base_url=self._base_url,
                name=self._name,
                path=current_path,
                conn=self._conn,
            )

            attr: None | SharedFile = current_file._Stat()

            if attr == None:
                self._conn.createDirectory(self._name, current_path)
            elif not attr.isDirectory:
                raise Exception(f"Cannot create directory: {current_path}")

        return self

    def LastWriteTimestamp(self) -> float:
        stat = self._Stat()
        if stat == None:
            raise Exception(f"File / directory {self.Path()} does not exist")
        return stat.last_write_time

    def FileSizeInBytes(self) -> int:
        stat = self._Stat()
        if stat == None:
            raise Exception(f"File / directory {self.Path()} does not exist")
        return stat.file_size

    def Children(self) -> set[Self]:
        files: list[SharedFile] = self._conn.listPath(self._name, self.Path())
        files = [f for f in files if not f.filename in [".", ".."]]
        return set([self.Resolve(file.filename) for file in files])

    def Read(self) -> IO[bytes]:
        content = BytesIO()
        self._conn.retrieveFile(self._name, self.Path(), content)
        content.seek(0)
        return content

    def Write(self, content: IO[bytes]) -> Self:
        self._conn.storeFile(self._name, self.Path(), content)
        return self

    def Remove(self) -> Self:
        stat = self._Stat()
        if stat != None:
            if stat.isDirectory:
                for c in self.Children():
                    c.Remove()
                self._conn.deleteDirectory(self._name, self.Path())
            else:
                self._conn.deleteFiles(self._name, self.Path())
        return self


class FileContextManagerSamba(FileContextManager):
    _username: str
    _password: str
    _name: str
    _path: str
    _host: str
    _port: int
    _conn: SMBConnection

    def __init__(
        self, username: str, password: str, name: str, path: str, host: str, port: int
    ):
        self._username = username
        self._password = password
        self._name = name
        self._path = path
        self._host = host
        self._port = port
        self._conn = SMBConnection(
            username=username,
            password=password,
            my_name="smb_sync",
            remote_name=name,
            use_ntlm_v2=True,
            is_direct_tcp=True,
        )

    def __enter__(self):
        if not self._conn.connect(ip=self._host, port=self._port):
            raise Exception(f"Cannot connect to {self.BaseUrl()}")
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self._conn.close()

    def Username(self) -> str:
        return self._username

    def Password(self) -> str:
        return self._password

    def Name(self) -> str:
        return self._name

    def Host(self) -> str:
        return self._host

    def Port(self) -> int:
        return self._port

    def BaseUrl(self) -> str:
        return f"smb://{self.Host()}:{self.Port()}/{self.Name()}"

    def Entry(self) -> FileBase:
        return FileSamba(self.BaseUrl(), self._name, self._path, self._conn)
