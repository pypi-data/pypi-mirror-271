import logging

from argparse import ArgumentParser, BooleanOptionalAction
from smb_sync.file_base import FileSyncOptions
from smb_sync.file_factory import CreateFileContextManager


def setup_logger():
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


def arg_parser():
    parser = ArgumentParser(
        prog="smb-sync",
        description="A tool for copying files between local drive and smb network drive",
    )

    parser.add_argument("source", help="source file or directory")
    parser.add_argument("target", help="target file or directory")

    parser.add_argument(
        "--auto-delete",
        action=BooleanOptionalAction,
        help="delete target files if they are removed in the source folder",
        default=False,
    )

    return parser


def main():
    setup_logger()

    parser = arg_parser()
    args = parser.parse_args()

    if args.source == None and args.target == None:
        parser.print_usage()
        return

    with CreateFileContextManager(args.source) as source_fcm:
        with CreateFileContextManager(args.target) as target_fcm:
            source_fcm.Entry().SyncTo(
                target_fcm.Entry(), FileSyncOptions(auto_delete=args.auto_delete)
            )
