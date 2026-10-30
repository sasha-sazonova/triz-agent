# GitHub setup

**Status:** the project is public at
<https://github.com/sasha-sazonova/triz-agent> (branch `main`).

GitHub Pages: <https://sasha-sazonova.github.io/triz-agent/>

This folder is already a git repository. No credentials or tokens are stored
here. The commands below are for mirroring to another account or recreating the
remote.

## Option A — GitHub CLI (recommended)

If `gh` is not installed:

```sh
brew install gh
```

Then:

```sh
cd triz-agent
gh auth login
gh repo create triz-agent --private --source=. --remote=origin --push
```

`--private` is the default choice because the case materials include patent
assessments and client context. Change to `--public` only after a deliberate
review of the content.

## Option B — create the repository manually

1. Create an empty repository named `triz-agent` on GitHub.
2. Add the remote and push:

```sh
cd triz-agent
git remote add origin git@github.com:<your-account>/triz-agent.git
git branch -M main
git push -u origin main
```

## Repository scope

This public repository is a curated release, not a mirror of the private
working environment. It contains the agent framework, the knowledge base, the
bilingual presentation, and the C4 case demo.

It deliberately does not publish:

- `.env` and API keys — secrets are never committed.
- `memory/`, personal profile, `.learnings/` — private working notes.
- The full anti-drone research archive and raw case files — third-party and
  client material; kept private.
- The C1 `zontik` demo and the source build workspace — separate working
  artifacts.

This is a deliberate scope decision, not a missing upload. A public repository
does not need to mirror every private file.
