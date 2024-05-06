from abc import ABC, abstractmethod
from diskcache import Cache
from hashlib import sha1
from logging import getLogger
from os.path import basename, expanduser, join
from typing import IO, Self


def _GetCache():
    return Cache(directory=expanduser("~/.cache/smb_sync"))


class FileSyncOptions:
    # Delete target files which do not exist in the source folder.
    auto_delete: bool

    def __init__(self, auto_delete=False):
        self.auto_delete = auto_delete


class FileBase(ABC):
    logger = getLogger("smb_sync")

    @abstractmethod
    def Path(self) -> str:
        pass

    @abstractmethod
    def Url(self) -> str:
        pass

    @abstractmethod
    def Resolve(self, path: str) -> Self:
        pass

    @abstractmethod
    def Exists(self) -> bool:
        pass

    @abstractmethod
    def IsDirectory(self) -> bool:
        pass

    @abstractmethod
    def MakeDirectory(self) -> Self:
        pass

    @abstractmethod
    def LastWriteTimestamp(self) -> float:
        pass

    @abstractmethod
    def FileSizeInBytes(self) -> int:
        pass

    @abstractmethod
    def Children(self) -> set[Self]:
        pass

    @abstractmethod
    def Read(self) -> IO[bytes]:
        pass

    @abstractmethod
    def Write(self, content: IO[bytes]) -> Self:
        pass

    @abstractmethod
    def Remove(self) -> Self:
        pass

    def Checksum(self) -> str | None:
        cache_key = f"check_sum:{self.Url()}:{self.LastWriteTimestamp()}"

        # Try to re-use cached check sum if it exists.
        with _GetCache() as cache:
            cached_checksum = cache.get(cache_key)
            if cached_checksum:
                self.logger.debug(
                    f"Re-using cached checksum: {cached_checksum} for {self.Url()}"
                )
                return str(cached_checksum)

        # Compute checksum (algorithm: SHA1).
        hash = sha1()
        with self.Read() as content:
            while True:
                block = content.read(65536)
                if not block:
                    break
                hash.update(block)
        checksum = hash.hexdigest()

        self.logger.debug(f"Computed checksum: {checksum} for {self.Url()}")

        # Save cached checksum.
        with _GetCache() as cache:
            cache.set(cache_key, checksum)

        return checksum

    def SyncTo(self, target: Self, options: FileSyncOptions) -> Self:
        self.logger.info(f"Checking {target.Path()}")

        if not self.Exists():
            # Remove target if it exists.
            if target.Exists():
                self.logger.info(f"Removing {target.Path()}")
                target.Remove()

        elif self.IsDirectory():
            # Remove target if target is not directory.
            if target.Exists() and not target.IsDirectory():
                target.Remove()

            # Creates directory target if it does not exist.
            if not target.Exists():
                self.logger.info(f"Creating directory {target.Path()}")
                target.MakeDirectory()

            self_children = {basename(c.Path()): c for c in self.Children()}
            target_children = {basename(c.Path()): c for c in target.Children()}

            # Recursively sync self children.
            for name, self_child in self_children.items():
                self_child.SyncTo(target=target.Resolve(name), options=options)

            if options.auto_delete:
                # Remove target child if there is no equivalent child in self.
                for name, target_child in target_children.items():
                    if name not in self_children:
                        self.logger.info(f"Removing {target_child.Path()}")
                        target_child.Remove()

        else:
            # Remove target if target is a directory.
            if target.Exists() and target.IsDirectory():
                self.logger.info(f"Removing {target.Path()}")
                target.Remove()

            # If src and target are at same size, we assume they are same.
            # Otherwise we override the content.
            if (
                not target.Exists()
                or target.FileSizeInBytes() != self.FileSizeInBytes()
                or target.Checksum() != self.Checksum()
            ):
                self.logger.info(f"Writing {target.Path()}")
                with self.Read() as self_content:
                    target.Write(self_content)

        return self


class FileContextManager(ABC):
    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        pass

    @abstractmethod
    def Entry(self) -> FileBase:
        pass
