"""
Main entry point.
"""

import sys
from argparse import ArgumentParser
from pathlib import Path

from youtube_html_parser.run import Input, run


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    parser = ArgumentParser()
    parser.add_argument("--input-html", help="The HTML file to parse.", required=True)
    parser.add_argument("--output-json", help="The output json.", required=True)
    parser.add_argument("--search", help="Parse a search page.", action="store_true")
    args = parser.parse_args()
    infile = Path(args.input_html)
    outfile = Path(args.output_json)
    _input: Input = Input(infile=infile, outfile=outfile, search=args.search)
    run(_input)
    return 0


if __name__ == "__main__":
    sys.exit(main())
