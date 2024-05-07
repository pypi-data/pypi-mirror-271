"""
smb_sync.cli
"""

import logging
import sys

from argparse import ArgumentParser, BooleanOptionalAction
from smb_sync.file_base import FileSyncOptions
from smb_sync.file_factory import create_file_context_manager


def setup_logger():
    """
    Setup logger.
    """
    # Create a formatter to specify the log message format
    formatter = logging.Formatter("[%(levelname)s] %(name)s - %(message)s")

    # Create a StreamHandler to log messages to stdout
    console_handler = logging.StreamHandler()

    # Set the logging level for the console handler (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    console_handler.setLevel(logging.INFO)

    # Set the formatter for the console handler
    console_handler.setFormatter(formatter)

    # Set the logging level for the root logger (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logging.basicConfig(level=logging.INFO, handlers=[console_handler])

    # Only show error logs from pysmb.
    logging.getLogger("SMB.SMBConnection").setLevel(logging.ERROR)


def arg_parser():
    """
    Build argument parser.
    """
    parser = ArgumentParser(
        prog="smb-sync",
        description="A tool for copying files between local drive and smb network drive",
    )

    parser.add_argument("source", help="source file or directory")
    parser.add_argument("target", help="target file or directory")

    parser.add_argument(
        "--auto-delete",
        action=BooleanOptionalAction,
        help="automatically delete extraneous files from target directories",
        default=False,
    )

    return parser


def main():
    """
    Main.
    """
    setup_logger()

    parser = arg_parser()
    args = parser.parse_args()

    if args.source is None and args.target is None:
        parser.print_usage()
        return

    with create_file_context_manager(args.source) as source_fcm:
        source_entry = source_fcm.entry()
        # We should quit immediately if source entry does not exist.
        if not source_entry.exists():
            logging.getLogger("smb_sync").fatal(
                "Source `%s` does not exist.", source_entry.url()
            )
            sys.exit(1)
        with create_file_context_manager(args.target) as target_fcm:
            source_entry.sync_to(
                target_fcm.entry(), FileSyncOptions(auto_delete=args.auto_delete)
            )
