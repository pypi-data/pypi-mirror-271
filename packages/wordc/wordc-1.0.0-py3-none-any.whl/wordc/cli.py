# Core Library modules
import argparse

# Local modules
from . import __version__
from .config import config


def parse_args(args: list) -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    """Function to return the ArgumentParser & Namespace objects created from the args.

    Args:
        args:   A list of arguments from the commandline
                e.g. ['wordc', 'mobydick.txt', '-c']
    """
    parser = argparse.ArgumentParser(
        prog="wordc", description="Utility to list the top word frequency in a document"
    )

    parser.add_argument(
        "filename",
        metavar="FILENAME",
        help="file to analyze for word frequency",
    )

    parser.add_argument(
        "-e",
        "--encoding",
        default=config.encoding,
        type=str,
        help="Encoding to use when reading file",
    )

    parser.add_argument(
        "-c",
        "--chunk",
        action="store_true",
        help="Force file chunking irrespective of file size",
    )

    parser.add_argument(
        "-s",
        "--size",
        default=config.chunk_size,
        type=int,
        help="Chunk size to use when reading file",
    )

    parser.add_argument(
        "-t",
        "--top_words",
        default=config.top_words,
        type=int,
        help="Number of top words to list",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="display version number",
    )

    return parser.parse_args(args), parser
