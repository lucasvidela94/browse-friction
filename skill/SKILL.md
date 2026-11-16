---
name: browse-friction
description: Pack evidence when a browse call in the OpenCode browser is silent or contradictory — a snapshot that finds nothing, a click that returns without changing the page, a page that looks empty, or behaviour that differs after a browse update. Then reduce it to a minimal repro and file it upstream.
---

# browse friction

Tools: `browse-friction` and `browse-corpus`, from <https://github.com/lucasvidela94/browse-friction>. Findings go to <https://github.com/anomalyco/browse/issues>.

A browse call can return success and be wrong. `snapshot` is a summary of the page: it drops what it considers noise and does not say so, so "no controls", "no match" and "the nav isn't there" are claims about the summary, not about the page. When a conclusion depends on a summary being complete, **pack** before concluding.

## 1. Pack

```sh
browse-friction --tab <tab>        # or --url <url> to open and pack one
```

It prints the flags. Read them before anything else: `! empty landmark`, `! fields behind a summary`, `! no controls`.

Done when: the pack directory has a `REPORT.md` and you can either name the flags or state there are none.

## 2. Compare

Four views of the same instant disagree in different ways. Name which contradicts which, with the numbers:

| pair | a disagreement means |
|---|---|
| compact snapshot vs `aria.txt` | the compact view omits controls the accessibility tree has |
| snapshot vs `innerText.txt` | the page shows text that no snapshot line represents |
| `page.json` counts vs refs in `snapshot.txt` | the summary lost controls the DOM has |
| `screenshot.png` vs every text view | the user sees content nothing else mentions |

Done when: one sentence, for example "compact shows 1 of 3 controls; aria has the two rows the landmark hides".

## 3. Reduce

Take the failing piece and rebuild it on `about:blank` with `eval` setting `document.body.innerHTML`: five to fifteen lines, no framework, no login. Add back the structure only if the flag disappears without it.

Done when: the flag reproduces from the snippet alone — or you can say it needs the real page and why.

## 4. File

```sh
gh issue create --repo anomalyco/browse --title "..." --body-file body.md
```

Body: versions from `status.json`, the view table row by row, expected vs actual, the snippet, and the one command that shows it.

Done when: the URL is printed and the body carries the snippet and the versions.

## Before filing

- Reproduce on a second, simpler page. If a page you wrote disagrees, the finding is about the page.
- Check the call you made: out-of-scope tab, an element inside an iframe, a relay that restarted a minute ago.
- Check the docs. `snapshot` scopes to `<main>` and collapses link-only landmarks on purpose. When behaviour is intended, the finding is the silence: ask for a note that names what was left out, not for a different behaviour.
- Search the open issues for the same symptom before writing a new one.

## Traps

- A landmark line reading `[0 controls]` is a count of `a[href]` and `button` only: rows built as `div[role="button"]` are invisible to it.
- With a `<main>` on the page, landmarks outside it are dropped without a line saying so.
- `find` greps the rendered snapshot, so anything the summary dropped reports as "no match".
- `mode: "aria"` is the reliable second opinion when the compact view looks thin.
- Inputs may be announced as `textbox "textbox"` when the page sets only `aria-placeholder`; match by placeholder, not by name.
- After `browse restart` or a relay crash the extension needs one to two minutes to reconnect. Calls fail with "open it, check the extension" while the browser is open and fine. Wait, then retry once.

## When it is version-shaped

`browse-corpus --ci` runs the hostile-page set and fails only when a new flag appears. Run it after a browse update, or before reporting a regression: if a case already had the flag, the bug predates the version you suspect.
