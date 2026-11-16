# browse-friction

Two commands for finding and reporting frictions in [browse](https://github.com/anomalyco/browse) by using it, not by reading it.

- **`browse-friction`** packs one tab's evidence: the compact snapshot, the aria snapshot, `innerText`, the page markup, a screenshot, and the versions — then compares them and writes `REPORT.md` with the numbers filled in and the sections still empty.
- **`browse-corpus`** runs that over a set of hostile pages and diffs each case against the previous run, so a change between browse versions shows up as a diff instead of as a surprise weeks later.

Both read the browser through the installed `browse` CLI. Nothing else is needed.

## Install

```sh
git clone <this repo> ~/Code/labs/browse-friction
ln -s ~/Code/labs/browse-friction/browse-friction ~/.local/bin/browse-friction
ln -s ~/Code/labs/browse-friction/browse-corpus   ~/.local/bin/browse-corpus
```

## browse-friction

```sh
browse-friction --url https://www.instagram.com/direct/inbox/
browse-friction --tab 12 --name ig-inbox
```

Writes `friction-<slug>-<stamp>/`:

| file | what it is |
|---|---|
| `REPORT.md` | the side-by-side table, the automatic flags, and empty sections for expected / happened / minimal repro |
| `snapshot.txt`, `aria.txt` | the two snapshots of the same instant |
| `innerText.txt`, `dom.html` | what the page says about itself |
| `screenshot.png` | what the user sees |
| `page.json`, `status.json` | counts, url, versions, extension state |
| `replay.sh` | the same calls again |

The flags exist because the expensive bugs are silent: a snapshot that returns success with nothing in it, a landmark that summarises itself as `[0 controls]`, a control that the aria tree has and the compact one does not. A correctly collapsed sidebar declares its controls and is not a flag.

## browse-corpus

```sh
browse-corpus                 # run, compare with the previous runs
browse-corpus --ci            # fail only when a flag appears
browse-corpus --update        # accept this run as the baseline
browse-corpus --only nav-rows # one case
browse-corpus --diff nav-rows # full snapshot diff for one case
browse-corpus --list
```

Cases live in `~/.config/browse-corpus/cases.json`, written on first run. A case is either `html` (set on `about:blank`) or a `url`, plus a `why`. Runs land in `~/.local/state/browse-corpus/runs/`, pruned to the newest 20.

Baselines are per case: `--only nav-rows` compares with the newest run that has `nav-rows`, so a partial run never makes the other cases look removed.

## Comparing two builds

The relay captures the pages, not the CLI. Pointing `--browse` at a candidate binary tests nothing unless that binary is the one behind the relay, and swapping the relay costs the extension's reconnect delay. The run prints the relay version and warns when the two disagree.

## Why these flags and not a log

A log records what the tool did. The bugs here live in what the tool *claimed*: `snapshot` said the inbox was empty and it was not. The only way to catch that is to put two independent views of the same instant side by side, which is what the pack is for.
