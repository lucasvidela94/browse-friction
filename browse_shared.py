"""Shared by browse-friction and browse-coverage: waiting, counting, summarising.

Both scripts import this from the repo directory, so the rules that decide what a
snapshot "shows" live in one place.
"""

import re
import time

CONTROL_ROLES = (
    "button|link|textbox|searchbox|checkbox|radio|combobox|listbox|option|tab|"
    "menuitem|menuitemcheckbox|menuitemradio|switch|slider|spinbutton|treeitem|disclosure"
)

_CONTROL_LINE = re.compile(rf"^\s*- '?(?:{CONTROL_ROLES})\b", re.M)
# 0.1.0 folded as "[8 controls]"; 0.1.2 says "[8 links, collapsed]" and adds a scope
# note naming what it left outside <main>. Both mean "not shown, but not lost".
_DECLARED = re.compile(r"- navigation .*?\[(\d+)(?: controls?| links?, collapsed)\]")
_SCOPED = re.compile(r"scoped to <main>[^;]*;.*?(\d+) controls? outside it are not shown")
_TRUNCATED = re.compile(r"- \.\.\. truncated after \d+ items")
_DIALOG = re.compile(r"^- dialog\b", re.M)
_IFRAME = re.compile(r"^\s*- iframe\b", re.M)


def controls_in(text):
    return _CONTROL_LINE.findall(text)


def declared_in(text):
    """Controls browse says it left out: folded landmarks plus the main-scoping note."""
    return sum(int(n) for n in _DECLARED.findall(text)) + sum(int(n) for n in _SCOPED.findall(text))


def is_truncated(text):
    return bool(_TRUNCATED.search(text))


def is_dialog_scoped(text):
    return bool(_DIALOG.search(text))


def is_scoped(text):
    """A note naming what a <main>-scoped snapshot left out: already accounted for."""
    return bool(_SCOPED.search(text))


def has_iframes(text):
    return bool(_IFRAME.search(text))


def settle(take_snapshot, max_seconds=8.0, min_seconds=3.0, poll=0.4):
    """Snapshot until it stops changing, and long enough for a skeleton to be replaced.

    Stability alone is not enough: a skeleton is perfectly stable for the second it
    takes the app to fetch its data (bsky.app: two identical empty snapshots, 544
    controls half a second later). So a snapshot only counts as settled once several
    samples agree AND min_seconds have passed.
    """
    start = time.time()
    deadline = start + max_seconds
    previous = None
    stable = 0
    while time.time() < deadline:
        current = take_snapshot()
        stable = stable + 1 if current == previous else 0
        previous = current
        if stable >= 2 and time.time() - start >= min_seconds and current.strip():
            return current
        time.sleep(poll)
    return previous or ""
