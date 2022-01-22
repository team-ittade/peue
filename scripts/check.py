import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / "docs"
WHITELIST_PATH = ROOT_DIR / "whitelist.json"

files = [x for x in DOCS_DIR.iterdir() if x.suffix == ".md"]

WHITELIST = [x.lower() for x in json.loads(WHITELIST_PATH.read_text("utf8"))]


def remove_links(text: str) -> str:
    text = re.sub(r"\[.*\]\(.*\)", "", text)
    lines = text.splitlines()
    lines = [x if not x.startswith("#") else "# dummy" for x in lines]
    return "\n".join(lines)


def find_extra_hypens():
    errors_found = 0
    for file in files:
        text = remove_links(file.read_text("utf8"))
        for i, line in enumerate(text.splitlines()):
            for match in re.findall(r"[a-záéíóú]+-[a-záéíóú]+", line, re.IGNORECASE):
                if match.lower() in WHITELIST:
                    continue
                errors_found += 1
                print(f"{file.stem}:{i+1:3d} {match!r}", file=sys.stderr)

    return errors_found == 0


def find_accents_in_links():
    errors_found = 0
    for file in files:
        text = file.read_text("utf8")
        for i, line in enumerate(text.splitlines()):
            for match in re.findall(r"\]\(.*?[áéíóú].*?\)", line, re.IGNORECASE):
                errors_found += 1
                match_text = str(match)[1:]
                if " " in match_text:
                    continue
                print(f"{file.stem}:{i+1:3d} {match_text!r}", file=sys.stderr)

    return errors_found == 0


def main():
    r1 = find_extra_hypens()
    r2 = find_accents_in_links()
    if not all((r1, r2)):
        sys.exit(0)


if __name__ == "__main__":
    main()
