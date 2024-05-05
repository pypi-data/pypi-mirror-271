
from wordc import wordc
from pathlib import Path


BASE_DIR = Path(__file__).parents[0]


def test_nominal():
    test_file = BASE_DIR / "resources" / "small.txt"
    words = wordc.read_file_contents(test_file, "utf-8")
    assert words == "hello world\n"



