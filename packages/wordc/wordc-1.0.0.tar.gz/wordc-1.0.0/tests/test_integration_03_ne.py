import subprocess

from pathlib import Path

BASE_DIR = Path(__file__).parents[0]


def test_command_line_usage():
    test_file = BASE_DIR / "resources" / "mobydic.txt"
    result = subprocess.run(["wordc", test_file], capture_output=True, text=True)
    assert result.returncode == 1
    assert result.stderr == ""
    assert result.stdout == "The file 'mobydic.txt' does not appear to be a file\n"

