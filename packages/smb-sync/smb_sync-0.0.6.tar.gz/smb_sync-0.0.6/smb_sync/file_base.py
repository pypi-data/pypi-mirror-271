"""
smb_sync.file_base
"""

from abc import ABC, abstractmethod
from hashlib import sha1
from logging import getLogger
from os.path import basename, expanduser
from typing import IO, Self
from diskcache import Cache


def _get_cache():
    return Cache(directory=expanduser("~/.cache/smb_sync"))


class FileSyncOptions:
    """
    File sync options.
    """

    # Delete target files which do not exist in the source folder.
    _auto_delete: bool

    def __init__(self, auto_delete=False):
        self._auto_delete = auto_delete

    def auto_delete(self) -> bool:
        """
        Returns should we auto delete files.
        """
        return self._auto_delete


class FileBase(ABC):
    """
    File base.
    """

    logger = getLogger("smb_sync")

    @abstractmethod
    def path(self) -> str:
        """
        Returns the path of current file.
        """
        raise NotImplementedError()

    @abstractmethod
    def url(self) -> str:
        """
        Returns the URL of current file.
        """
        raise NotImplementedError()

    @abstractmethod
    def resolve(self, path: str) -> Self:
        """
        Returns resolved file by given path.
        """
        raise NotImplementedError()

    @abstractmethod
    def parent(self) -> Self:
        """
        Returns parent directory by given path.
        """
        raise NotImplementedError()

    @abstractmethod
    def exists(self) -> bool:
        """
        Returns if the file exists or not.
        """
        raise NotImplementedError()

    @abstractmethod
    def is_directory(self) -> bool:
        """
        Returns if the file is directory.
        """
        raise NotImplementedError()

    @abstractmethod
    def make_directory(self) -> Self:
        """
        Makes it directory.
        """
        raise NotImplementedError()

    @abstractmethod
    def last_write_timestamp(self) -> float:
        """
        Returns last write timestamp.
        """
        raise NotImplementedError()

    @abstractmethod
    def file_size_in_bytes(self) -> int:
        """
        Returns file size in bytes.
        """
        raise NotImplementedError()

    @abstractmethod
    def children(self) -> set[Self]:
        """
        Returns chilren of current file.
        """
        raise NotImplementedError()

    @abstractmethod
    def read(self) -> IO[bytes]:
        """
        Returns bytes of current file.
        """
        raise NotImplementedError()

    @abstractmethod
    def write(self, content: IO[bytes]) -> Self:
        """
        Writes bytes into current file.
        """
        raise NotImplementedError()

    @abstractmethod
    def remove(self) -> Self:
        """
        Removes current file.
        """
        raise NotImplementedError()

    def checksum(self) -> str | None:
        """
        Returns checksum of current file.
        """
        cache_key = f"check_sum:{self.url()}:{self.last_write_timestamp()}"

        # Try to re-use cached check sum if it exists.
        with _get_cache() as cache:
            cached_checksum = cache.get(cache_key)
            if cached_checksum:
                self.logger.debug(
                    "Re-using cached checksum: %s for %s",
                    str(cached_checksum),
                    self.url(),
                )
                return str(cached_checksum)

        # Compute checksum (algorithm: SHA1).
        hash_val = sha1()
        with self.read() as content:
            while True:
                block = content.read(65536)
                if not block:
                    break
                hash_val.update(block)
        checksum = hash_val.hexdigest()

        self.logger.debug("Computed checksum: %s for %s", checksum, self.url())

        # Save cached checksum.
        with _get_cache() as cache:
            cache.set(cache_key, checksum)

        return checksum

    def sync_to(self, target: Self, options: FileSyncOptions) -> Self:
        """
        Syncs current file to given target file.
        """
        self.logger.info("Checking %s", target.url())

        if not self.exists():
            # Remove target if it exists.
            if target.exists() and options.auto_delete():
                self.logger.info("Removing %s", target.url())
                target.remove()

        elif self.is_directory():
            # Remove target if target is not directory.
            if target.exists() and not target.is_directory():
                self.logger.info("Removing %s", target.url())
                target.remove()

            # Creates directory target if it does not exist.
            if not target.exists():
                self.logger.info("Creating directory %s", target.url())
                target.make_directory()

            self_children = {basename(c.path()): c for c in self.children()}
            target_children = {basename(c.path()): c for c in target.children()}

            # Recursively sync self children.
            for name, self_child in self_children.items():
                self_child.sync_to(target=target.resolve(name), options=options)

            if options.auto_delete():
                # Remove target child if there is no equivalent child in self.
                for name, target_child in target_children.items():
                    if name not in self_children:
                        self.logger.info("Removing %s", target_child.url())
                        target_child.remove()

        else:
            # Remove target if target is a directory.
            if target.exists() and target.is_directory():
                self.logger.info("Removing %s", target.url())
                target.remove()

            # Check if target file's parent directory exists.
            target_parent = target.parent()
            if not target_parent.exists():
                target_parent.make_directory()

            # If src and target are at same size, we assume they are same.
            # Otherwise we override the content.
            if (
                not target.exists()
                or target.file_size_in_bytes() != self.file_size_in_bytes()
                or target.checksum() != self.checksum()
            ):
                self.logger.info("Writing %s", target.url())
                with self.read() as self_content:
                    target.write(self_content)

        return self


class FileContextManager(ABC):
    """
    File context manager.
    """

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        pass

    @abstractmethod
    def entry(self) -> FileBase:
        """
        Returns the entry file.
        """
        raise NotImplementedError()
