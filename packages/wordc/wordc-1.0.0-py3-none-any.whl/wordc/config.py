#!/usr/bin/env python3


class Config:
    """Configuration class"""

    encoding: str = "utf-8"  # default file encoding to use when reading a file
    chunk: bool = False  # determine if file chunking should be used
    chunk_size: int = 1024  # file chunk size (bytes) to use when file chunking
    memory_threshold: int = 25  # (filesize / memory available) ratio threshold
    filesize_threshold: int = 100  # filesize (Mb)threshold when chunking begins
    top_words: int = 20  # No. of top words to be printed
    sample_size: int = 1024  # bytes of a file to sample (for various utilities)


config = Config()
