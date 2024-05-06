# pylint: disable=too-many-branches

"""
Unit test file.
"""
import os
import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from youtube_html_parser.parser import parse_yt_page

ENABLE_FETCH_UP_NEXT_VIDEOS = False

HERE = Path(__file__).parent
DATA_DIR = HERE / "data"
assert DATA_DIR.exists()

TEST_HTML = list(DATA_DIR.glob("*.html"))
# Filter out *.pretty.html files
TEST_HTML = [file for file in TEST_HTML if not file.name.endswith(".pretty.html")]


PROJECT_ROOT = HERE.parent
COMMAND = "youtube-html-parser"


def invoke_parse_py(html: str) -> str:
    parsed_data = parse_yt_page(html)
    return parsed_data.serialize()


def invoke_parse_bin(html: str) -> str:
    with TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file = temp_dir_path / "temp.html"
        temp_file.write_text(html, encoding="utf-8")
        output_file = temp_dir_path / "output.json"
        command = f'{COMMAND} --input-html "{temp_file}" --output-json "{output_file}"'
        print(f"Running command: {command}")
        rtn = os.system(command)
        assert rtn == 0
        return output_file.read_text(encoding="utf-8")


class ParseTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skip("Slow test")
    def test_parse_performance_py(self) -> None:
        """Test the performance of parsing."""
        print("Testing performance of parsing.")
        test_html = TEST_HTML[0].read_text(encoding="utf-8")
        start = time.time()
        for _ in range(10):
            _ = invoke_parse_py(test_html)
        # print(parsed_json)
        dif = time.time() - start
        print(f"Time taken: {dif}")

    @unittest.skip("Slow test, binary executable seems slower than the Python version.")
    def test_parse_performance_bin(self) -> None:
        """Test the performance of parsing."""
        print("Testing performance of parsing.")
        test_html = TEST_HTML[0].read_text(encoding="utf-8")
        start = time.time()
        for _ in range(10):
            _ = invoke_parse_bin(
                test_html
            )  # faster execution, slower startup because it's a process.
        # print(parsed_json)
        dif = time.time() - start
        print(f"Time taken: {dif}")


if __name__ == "__main__":
    unittest.main()
