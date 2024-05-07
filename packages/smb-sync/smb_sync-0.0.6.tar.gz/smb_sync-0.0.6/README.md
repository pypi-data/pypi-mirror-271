# smb-sync

![PyPI - Version](https://img.shields.io/pypi/v/smb-sync)
![PyPI - Downloads](https://img.shields.io/pypi/dm/smb-sync)

**smb-sync** is a command-line tool for synchronizing files between a local drive and a SMB network drive. It is designed to efficiently copy files while minimizing data transfer by checking last modified timestamps and checksums.

## Features

- Synchronize files between a local drive and a SMB network drive.
- Efficiently transfer only modified files by checking last modified timestamps and checksums.
- Minimize data transfer by caching checksums of files.
- Command-line interface for easy usage.

## Installation

You can install `smb-sync` using pip:

```bash
pip install smb-sync
```

## Usage

```
usage: smb-sync [-h] [--auto-delete | --no-auto-delete] [--version] source target

A tool for copying files between local drive and smb network drive

positional arguments:
  source                source file or directory
  target                target file or directory

options:
  -h, --help            show this help message and exit
  --auto-delete, --no-auto-delete
                        automatically delete extraneous files from target directories
  --version             show program's version number and exit
```

### Examples

#### Synchronize from a local directory to a directory on SMB network drive.

```bash
smb-sync ~/Pictures smb://user:pass@nas.local/Pictures
```

#### Synchromize from a directory on SMB network drive to a local directory (guest access).

With `auto-delete` option, it will also delete extraneous files on target directories.

```
smb-sync --auto-delete smb://nas.local/Documents ~/Documents
```

#### Download a PDF document from SMB network drive.

```bash
smb-sync smb://nas.local/Documents/example.pdf ~/Documents/example.pdf
```

#### Upload a PDF document to SMB network drive.

```bash
smb-sync ~/Documents/example.pdf smb://nas.local/Documents/example.pdf 
```
