# PEUE

Notes for the subject "Políticas Económicas de la Unión Europea"

To launch a local version of the app, just type `mkdocs serve`.

## Scripts

### Check

Checks for common errors while redacting notes:

- Sometimes, while copying text from the class PDF the sentences end with a split word, and that word is split with a dash. So, random dashes may appear in this notes. This script finds all occurences of `<WORD>-<WORD>` and it checks it against the [whitelist](whitelist.json).
- There are a finite number of available [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/). This script also finds and validates the admonitions.
- When creating internal links (the ones starting with `#`) sometimes the intelisense messes up and keeps the accents in the links, which makes them invalid. This script finds all the internal link and while you have a local app running on port 8000 it will make requests to the local app and validate each internal link.

### Copy Rendered Content

This is not written using word or something like that, so check spelling isn't availble. A workaround is to copy the site content (you need to have the local app running) and then paste in a [new google doc](https://docs.new/).
