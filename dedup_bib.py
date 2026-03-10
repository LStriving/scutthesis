#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import sys

ENTRY_START_RE = re.compile(r"(?m)^[ \t]*@\w+[ \t]*\{[ \t]*([^,\s][^,]*?)[ \t]*,")


def find_entry_end(text, start_index):
    brace_open = text.find("{", start_index)
    if brace_open < 0:
        return -1

    depth = 0
    i = brace_open
    in_quote = False

    while i < len(text):
        ch = text[i]
        prev = text[i - 1] if i > 0 else ""

        if ch == '"' and prev != "\\":
            in_quote = not in_quote
        elif not in_quote:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i + 1

        i += 1

    return -1


def dedup_bib_entries(text):
    matches = list(ENTRY_START_RE.finditer(text))
    if not matches:
        return text, [], False

    seen = set()
    removed_keys = []
    parts = []
    last_end = 0

    for m in matches:
        entry_start = m.start()
        entry_end = find_entry_end(text, entry_start)
        if entry_end < 0:
            raise ValueError("Failed to parse BibTeX entry: unmatched braces")

        key = m.group(1).strip()

        if entry_start > last_end:
            parts.append(text[last_end:entry_start])

        entry_text = text[entry_start:entry_end]

        if key in seen:
            removed_keys.append(key)
            # Keep one trailing newline where possible to avoid gluing entries.
            if entry_end < len(text) and text[entry_end] == "\n":
                parts.append("\n")
        else:
            seen.add(key)
            parts.append(entry_text)

        last_end = entry_end

    if last_end < len(text):
        parts.append(text[last_end:])

    new_text = "".join(parts)
    changed = new_text != text
    return new_text, removed_keys, changed


def main():
    parser = argparse.ArgumentParser(description="Deduplicate BibTeX entries by citation key.")
    parser.add_argument("--input", "-i", required=True, help="Path to .bib file")
    parser.add_argument(
        "--backup",
        action="store_true",
        default=True,
        help="Write a .bak backup before rewriting (default: true)",
    )
    parser.add_argument("--no-backup", action="store_true", help="Do not write backup file")
    args = parser.parse_args()

    bib_path = args.input
    do_backup = args.backup and not args.no_backup

    if not os.path.exists(bib_path):
        print(f"[dedup-bib] Skip: file not found: {bib_path}")
        return 0

    try:
        with open(bib_path, "r", encoding="utf-8") as f:
            original = f.read()

        new_text, removed_keys, changed = dedup_bib_entries(original)

        if not changed:
            print("[dedup-bib] No duplicate keys found.")
            return 0

        if do_backup:
            backup_path = bib_path + ".bak"
            shutil.copyfile(bib_path, backup_path)
            print(f"[dedup-bib] Backup written: {backup_path}")

        with open(bib_path, "w", encoding="utf-8", newline="") as f:
            f.write(new_text)

        removed_summary = ", ".join(removed_keys) if removed_keys else "(none)"
        print(f"[dedup-bib] Removed {len(removed_keys)} duplicate entrie(s): {removed_summary}")
        return 0
    except Exception as exc:
        print(f"[dedup-bib] Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
