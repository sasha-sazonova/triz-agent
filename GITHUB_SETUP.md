# GitHub setup

This folder is a local git repository prepared for GitHub. No credentials or
tokens are stored here.

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

## What is intentionally not included

- `.env` and any API keys.
- `memory/`, `USER.md`, `.learnings/`.
- The full anti-drone research archive (582 references) and raw case files.
- The C1 `zontik` demo and the source build workspace.

The repository contains the agent framework, the knowledge base, the bilingual
presentation, and the C4 case demo.
