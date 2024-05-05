from wordc import utils
from pathlib import Path


BASE_DIR = Path(__file__).parents[0]


def test_false():
    test_file = BASE_DIR / "resources" / "small.txt"
    boolean = utils.is_binary(test_file)
    assert boolean is False


def test_true():
    test_file = BASE_DIR / "resources" / "moby.exe"
    boolean = utils.is_binary(test_file)
    assert boolean is True
