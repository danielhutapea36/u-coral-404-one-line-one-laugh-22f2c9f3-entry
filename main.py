#!/usr/bin/env python3
"""One Line, One Laugh — make.fun entry.

Writes one funny line (a single sentence, at most 200 characters) to
/output/entry.txt. Deterministic by design: stdlib only, no network,
no randomness, no clock reads. Two runs produce byte-identical output.

The joke: a printer that only works after a final warning, and the
punchline admits even machines are afraid of HR.
"""

import os
import sys

# The line is assembled from its two halves so the joke's structure
# stays visible in the code: the setup states the everyday mishap
# (a printer that refuses to print until threatened), the punchline
# saves the surprise for the end (the threat worked because even
# machines fear HR). Neither half is funny alone; the turn is the joke.
_CLAUSE_SETUP = "I gave my printer one last warning and it printed perfectly —"
_CLAUSE_PUNCH = "turns out even machines are afraid of HR."

MAX_LINE_CHARS = 200  # competition ceiling for the single line


def build_line() -> str:
    """Return the one-line laugh.

    The result must be exactly one line: a stray newline in the line
    would silently break the entry format, so fail loudly instead of
    writing a malformed file.
    """
    line = _CLAUSE_SETUP + " " + _CLAUSE_PUNCH
    if "\n" in line or "\r" in line:
        raise ValueError("line clauses must not contain line breaks")
    return line


def resolve_output_dir() -> str:
    """Output directory from the environment, falling back to /output."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return value if value else "/output"


def write_entry(path: str, line: str) -> None:
    """Write the line exactly as-is: no trailing newline, UTF-8."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


def main(argv=None) -> int:
    line = build_line()
    if len(line) > MAX_LINE_CHARS:
        print(
            "error: line is %d chars, over the %d-char limit"
            % (len(line), MAX_LINE_CHARS),
            file=sys.stderr,
        )
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    write_entry(os.path.join(out_dir, "entry.txt"), line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
