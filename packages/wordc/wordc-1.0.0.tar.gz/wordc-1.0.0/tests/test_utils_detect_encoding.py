from wordc import utils
from pathlib import Path


BASE_DIR = Path(__file__).parents[0]


def test_nominal():
    test_file = BASE_DIR / "resources" / "small.txt"
    encoding = utils.detect_encoding(test_file)
    assert encoding == "utf-8"
