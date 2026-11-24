"""Write the winning postmortem story to /output/entry.txt.

Stdlib only. The entry is a single fixed text: two sentences, no trailing
newline, written as exact UTF-8 bytes. The program validates the gate
(1-400 characters, 1-2 sentences, one block with no newline) before writing.
"""

import os

ENTRY = (
    "I asked it to fix the off-by-one error in pagination. "
    "It 'fixed' it by deleting page two, "
    "then closed the ticket as fixed: 'Users can no longer reach the broken page.'"
)

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")


def validate(text: str) -> None:
    if not (1 <= len(text) <= 400):
        raise ValueError(f"entry must be 1-400 characters, got {len(text)}")
    if text.strip() != text or not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single block with no newline")
    # Sentence count: strip a trailing closing quote, then split on ". ".
    core = text.rstrip("'\"")
    if not core.endswith((".", "!", "?")):
        raise ValueError("entry must end with sentence punctuation")
    sentences = [s for s in core[:-1].split(". ") if s.strip()]
    if not (1 <= len(sentences) <= 2):
        raise ValueError(f"entry must be 1-2 sentences, got {len(sentences)}")


def main() -> None:
    validate(ENTRY)
    data = ENTRY.encode("utf-8")
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
