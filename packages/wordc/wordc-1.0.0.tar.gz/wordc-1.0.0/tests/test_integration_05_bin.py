import subprocess

from pathlib import Path

BASE_DIR = Path(__file__).parents[0]


def test_command_line_usage():
    test_file = BASE_DIR / "resources" / "moby.exe"
    result = subprocess.run(["wordc", test_file], capture_output=True, text=True)
    assert result.returncode == 1
    assert result.stderr == ""
    assert result.stdout == "The file 'moby.exe' appears to be a binary file\n"

