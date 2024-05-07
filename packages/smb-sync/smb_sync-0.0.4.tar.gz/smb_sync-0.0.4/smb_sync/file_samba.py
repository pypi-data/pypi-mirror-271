"""
smb_sync.file_samba
"""

from io import BytesIO
from os.path import dirname, join
from typing import IO, Self
from smb.base import OperationFailure, SharedFile
from smb.SMBConnection import SMBConnection

from .file_base import FileBase, FileContextManager


class FileSamba(FileBase):
    """
    File samba.
    """

    _base_url: str
    _name: str
    _path: str
    _conn: SMBConnection

    def __init__(self, base_url: str, name: str, path: str, conn: SMBConnection):
        self._base_url = base_url
        self._name = name
        self._path = path
        self._conn = conn

    def stat(self) -> SharedFile | None:
        """
        Returns samba file state.
        """
        try:
            return self._conn.getAttributes(self._name, self.path())
        except OperationFailure:
            return None

    def path(self) -> str:
        return self._path

    def url(self) -> str:
        return f"{self._base_url}/{self.path()}"

    def resolve(self, path: str) -> Self:
        return FileSamba(
            self._base_url, self._name, join(self.path(), path), self._conn
        )

    def parent(self) -> Self:
        return FileSamba(self._base_url, self._name, dirname(self.path()), self._conn)

    def exists(self) -> bool:
        return self.stat() is not None

    def is_directory(self) -> bool:
        stat = self.stat()
        return stat is not None and stat.isDirectory

    def make_directory(self) -> Self:
        current_path = ""
        for directory in self.path().strip("/").split("/"):
            current_path = join(current_path, directory)
            current_file = FileSamba(
                base_url=self._base_url,
                name=self._name,
                path=current_path,
                conn=self._conn,
            )

            attr: None | SharedFile = current_file.stat()

            if attr is None:
                self._conn.createDirectory(self._name, current_path)
            elif not attr.isDirectory:
                raise Exception(f"Cannot create directory: {current_path}")

        return self

    def last_write_timestamp(self) -> float:
        stat = self.stat()
        if stat is None:
            raise Exception(f"File / directory {self.Path()} does not exist")
        return stat.last_write_time

    def file_size_in_bytes(self) -> int:
        stat = self.stat()
        if stat is None:
            raise Exception(f"File / directory {self.Path()} does not exist")
        return stat.file_size

    def children(self) -> set[Self]:
        files: list[SharedFile] = self._conn.listPath(self._name, self.path())
        files = [f for f in files if not f.filename in [".", ".."]]
        return set([self.resolve(file.filename) for file in files])

    def read(self) -> IO[bytes]:
        content = BytesIO()
        self._conn.retrieveFile(self._name, self.path(), content)
        content.seek(0)
        return content

    def write(self, content: IO[bytes]) -> Self:
        self._conn.storeFile(self._name, self.path(), content)
        return self

    def remove(self) -> Self:
        stat = self.stat()
        if stat is not None:
            if stat.isDirectory:
                for c in self.children():
                    c.remove()
                self._conn.deleteDirectory(self._name, self.path())
            else:
                self._conn.deleteFiles(self._name, self.path())
        return self


class FileContextManagerSamba(FileContextManager):
    """
    File context manager samba.
    """

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
            raise Exception(f"Cannot connect to {self.base_url()}")
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self._conn.close()

    def username(self) -> str:
        """
        Returns username.
        """
        return self._username

    def password(self) -> str:
        """
        Returns password.
        """
        return self._password

    def name(self) -> str:
        """
        Returns name.
        """
        return self._name

    def host(self) -> str:
        """
        Returns host.
        """
        return self._host

    def port(self) -> int:
        """
        Returns port.
        """
        return self._port

    def base_url(self) -> str:
        """
        Returns base URL.
        """
        return f"smb://{self.host()}:{self.port()}/{self.name()}"

    def entry(self) -> FileBase:
        return FileSamba(self.base_url(), self._name, self._path, self._conn)
