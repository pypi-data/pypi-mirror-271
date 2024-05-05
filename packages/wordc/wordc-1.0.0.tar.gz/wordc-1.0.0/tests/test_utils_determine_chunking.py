from wordc import utils
from pathlib import Path
from wordc.config import config


BASE_DIR = Path(__file__).parents[0]


def test_false():
    test_file = BASE_DIR / "resources" / "mobydick.txt"      # size = 417986
    filesize = Path(test_file).stat().st_size
    threshold = int(filesize * (100 / config.memory_threshold))
    boolean = utils.determine_chunking(test_file, threshold+10)
    assert boolean is False


def test_true():
    test_file = BASE_DIR / "resources" / "mobydick.txt"      # size = 417986
    filesize = Path(test_file).stat().st_size
    threshold = int(filesize * (100 / config.memory_threshold))
    boolean = utils.determine_chunking(test_file, threshold-10)
    assert boolean is True
