import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / "docs"
WHITELIST_PATH = ROOT_DIR / "whitelist.json"

files = [x for x in DOCS_DIR.iterdir() if x.suffix == ".md"]

WHITELIST = [x.lower() for x in json.loads(WHITELIST_PATH.read_text("utf8"))]
KNOWN_ADMONITIONS = [
    "abstract",
    "bug",
    "check",
    "danger",
    "error",
    "example",
    "fail",
    "faq",
    "info",
    "note",
    "pied-piper",
    "question",
    "success",
    "tip",
    "tldr",
]

EXTRA_HYPENS_PATTERN = r"[a-záéíóú0-9]+-[a-záéíóú]+"
LINKS_PATTERN = r"\[.+?\]\((.+?)\)"
ADMONITIONS_PATTERN = r"(?:!!!|\?\?\?) ([\w-]+)"


def remove_links(text: str) -> str:
    text = re.sub(r"\[.*\]\(.*\)", "", text)
    lines = text.splitlines()
    return "\n".join(lines)


def find_extra_hypens():
    errors_found = 0
    for file in files:
        text = remove_links(file.read_text("utf8"))
        for i, line in enumerate(text.splitlines()):
            for match in re.findall(EXTRA_HYPENS_PATTERN, line, re.IGNORECASE):
                if match.lower() in WHITELIST:
                    continue
                errors_found += 1
                print(f"[extra-hypen] {file.stem}:{i+1:3d} {match!r}", file=sys.stderr)

    return errors_found == 0


def validate_admonitions():
    errors_found = 0

    for file in files:
        text = file.read_text("utf8")
        for i, line in enumerate(text.splitlines()):
            for match in re.finditer(ADMONITIONS_PATTERN, line, re.IGNORECASE):
                title = match.group(1)
                if title not in KNOWN_ADMONITIONS:
                    print(
                        f"[invalid-admonition] {file.stem}:{i+1:3d} {title!r}",
                        file=sys.stderr,
                    )

    return errors_found == 0


def check_internal_links():
    errors_found = 0
    for file in files:
        if file.stem == "index":
            continue

        url = f"http://localhost:8000/{file.stem}/"
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        text = file.read_text("utf8")
        for i, line in enumerate(text.splitlines()):
            for match in re.finditer(LINKS_PATTERN, line, re.IGNORECASE):
                link_id = match.group(1)
                if link_id[0] != "#":
                    continue
                link_id = link_id[1:]

                if not soup.find(id=link_id):
                    errors_found += 1
                    print(
                        f"[invalid-internal-link] {file.stem}:{i+1:3d} {match.group(0)!r}",
                        file=sys.stderr,
                    )

    return errors_found == 0


def main():
    r1 = find_extra_hypens()
    r2 = validate_admonitions()
    r3 = check_internal_links()
    if not all((r1, r2, r3)):
        sys.exit(1)


if __name__ == "__main__":
    main()
