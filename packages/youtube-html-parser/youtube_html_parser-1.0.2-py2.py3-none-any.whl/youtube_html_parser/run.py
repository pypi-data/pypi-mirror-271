"""
Main entry point.
"""

import time
import traceback
import warnings
from dataclasses import dataclass

# import gunzip
from gzip import GzipFile
from pathlib import Path
from tempfile import TemporaryDirectory

from youtube_html_parser.parser import (
    YtPage,
    YtPageSearch,
    parse_yt_page,
    parse_yt_page_seach,
)


@dataclass
class Input:
    infile: Path
    outfile: Path
    search: bool

    # define hashing so that we can go into a dictionary
    def __hash__(self) -> int:
        return hash(self.infile)

    # define equality so that we can go into a dictionary
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Input):
            return False
        return self.infile == other.infile


def extract_html(infile: Path) -> str:
    """Extract the HTML from the file."""
    if infile.suffix == ".gz":
        try:
            with TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)
                temp_file = temp_dir_path / "temp.html"
                with GzipFile(infile, "r") as gzfile:
                    data = gzfile.read()
                    temp_file.write_text(data.decode("utf-8"), encoding="utf-8")
                return temp_file.read_text(encoding="utf-8")
        except Exception as e:  # pylint: disable=broad-except
            warnings.warn(
                f"Failed to gz extract {infile} because of {e}, falling back to normal read."
            )
    out = infile.read_text(encoding="utf-8")
    print(f"Extracted {len(out)} characters from {infile}")
    return out


def run(_input: Input) -> Exception | None:
    """Run the parser."""
    if isinstance(_input, list):
        for inp in _input:
            run(inp)
        return None
    assert isinstance(_input, Input)
    infile = _input.infile
    outfile = _input.outfile
    search = _input.search
    try:
        html = extract_html(infile)
        start_time = time.time()
        parsed: YtPage | YtPageSearch
        if search:
            parsed = parse_yt_page_seach(html)
        else:
            parsed = parse_yt_page(html)
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.2f} seconds.")
        parsed.write_json(outfile)
        return None
    except Exception as e:  # pylint: disable=broad-except
        stacktrace = traceback.format_exc()
        outmsg = f'"error": "Failed to parse", "file": "{infile}", "exception": "{e}", "stacktrace": "{stacktrace}"'
        warnings.warn(outmsg)
        outfile.write_text(outmsg, encoding="utf-8")
        return e


def bulk_run(_input: list[Input]) -> dict[Input, Exception]:
    """Run the parser."""
    out: dict[Input, Exception] = {}
    for inp in _input:
        err = run(inp)
        if err is not None:
            out[inp] = err
    return out


def main() -> None:
    """Main entry point for the template_python_cmd package."""
    infile = Path("tests/youtube/data/search_html/1.html")
    outfile = Path("tests/youtube/data/search_html/1.json")
    _input: Input = Input(infile=infile, outfile=outfile, search=True)
    run(_input)
