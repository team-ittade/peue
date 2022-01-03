import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR / "docs"
WHITELIST_PATH = ROOT_DIR / "whitelist.json"

files = [x for x in DOCS_DIR.iterdir() if x.suffix == ".md"]

WHITELIST = [x.lower() for x in json.loads(WHITELIST_PATH.read_text("utf8"))]


def remove_links(text: str) -> str:
    text = re.sub(r"\[.*\]\(.*\)", "", text)
    lines = text.splitlines()
    lines = [x if not x.startswith("#") else "# dummy" for x in lines]
    return "\n".join(lines)


def main():
    for file in files:
        text = remove_links(file.read_text("utf8"))
        for i, line in enumerate(text.splitlines()):
            for match in re.findall(r"[a-záéíóú]+-[a-záéíóú]+", line, re.IGNORECASE):
                if match.lower() in WHITELIST:
                    continue
                print(f"{file.stem}:{i+1:3d} {match!r}")


if __name__ == "__main__":
    main()
