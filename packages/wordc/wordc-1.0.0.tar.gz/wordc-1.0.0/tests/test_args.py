#!/usr/bin/env python3
# Core Library modules

# Core Library modules


# First party modules
from wordc import wordc


def test_default_args():
    args, parser = wordc.parse_args(["mobydick.txt"])
    assert args.filename == "mobydick.txt"
    assert args.encoding == "utf-8"
    assert args.chunk is False
    assert args.size == 1024
    assert args.top_words == 20


def test_args_project():
    args, parser = wordc.parse_args(
        [
            "mobydick.txt",
        ]
    )
    assert args.filename == "mobydick.txt"


def test_args_register():
    args, parser = wordc.parse_args(
        [
            "mobydick.txt",
            "-e",
            "utf-16"
        ]
    )
    assert args.encoding == "utf-16"


def test_args_dryrun():
    args, parser = wordc.parse_args(
        [
            "mobydick.txt",
            "-c",
        ]
    )
    assert args.chunk is True


def test_args_nocleanup():
    args, parser = wordc.parse_args(
        [
            "mobydick.txt",
            "-s",
            "4096"
        ]
    )
    assert args.size == 4096


def test_args_verbose():
    args, parser = wordc.parse_args(
        [
            "mobydick.txt",
            "-t",
            "10"
        ]
    )
    assert args.top_words == 10

