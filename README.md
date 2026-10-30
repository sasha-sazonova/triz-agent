# Heinrich — TRIZ Inventor Agent

A gate-controlled invention co-pilot built on classical TRIZ. It takes an
engineering problem in natural language (RU/EN), turns it into a formal
contradiction, searches the TRIZ knowledge base, generates concepts with full
traceability, and subjects them to independent critique and a preliminary
patent check.

The agent is not a “generate ten ideas” button. It is a disciplined pipeline:
**mini-problem → contradiction → Ideal Final Result → principles and effects →
concepts → critique → report**. Compromises are rejected; the goal is to
separate a contradiction in space, time, or structure.

## What is inside

| Layer | What it does |
|---|---|
| **LITE** | Seven artifacts (`01_task` … `07_report`) with file-based gate control. Default cycle: 5–15 minutes. |
| **DEEP / ARIZ-85C** | Nine parts of ARIZ-85C for cases where LITE stalls: resource model, information fund, problem redefinition, answer control. |
| **Knowledge base** | 39 parameters, 40 principles, 1,190 contradiction pairs, 15 effects, 76 standard solutions, 4 separation axes, 8 evolution trends. |
| **Six craft roles** | Contradiction Miner, Principle Selector, Effects Lookup, Synectic, Critic, Patent Checker — one-shot subagents with clean context. |
| **Research** | `science-search` (arXiv, Crossref, Semantic Scholar) and `patent-search` (EPO OPS, USPTO, Rospatent) adapters. |
| **Quality** | Scorecard on five axes, traceability of every concept to a principle or effect, evaluation thresholds, archive and lessons. |
| **Visualization** | Isometric engineering explainers built with the MIT `anatomy` skill. |

## Repository map

```
triz-agent/
├── agent/                  # runtime instruction set and knowledge base
│   ├── AGENTS.md           # startup, gate control, subagent rules
│   ├── SOUL.md             # persona and method principles
│   ├── IDENTITY.md         # agent identity
│   ├── USER.md             # generic user profile template
│   ├── DESCRIPTION.md      # short project description
│   ├── TOOLS.md            # local tools and search skills
│   ├── methods/            # LITE, DEEP/ARIZ-85C, report template
│   ├── craft/              # six subagent role definitions
│   ├── knowledge/          # 39/40/matrix/effects/ARIZ/trends
│   ├── scripts/            # deterministic matrix lookup
│   └── eval/               # evaluation runner and seed cases
├── presentation/
│   ├── ru/index.html       # Russian 13-slide deck
│   ├── en/index.html       # English 13-slide deck
│   ├── deck.js             # shared navigation script
│   └── README.md
├── cases/
│   └── c4-dipole/
│       ├── ru/index.html   # Russian case page
│       ├── en/index.html   # English case page
│       ├── assets/         # interactive stand, images, report
│       └── README.md
├── LICENSES/               # third-party license texts
├── THIRD_PARTY.md          # attribution and license map
├── GITHUB_SETUP.md         # how to publish this folder
├── requirements.txt
└── LICENSE                 # project license (All rights reserved)
```

## Quick start

### Open the presentation

| Version | Live page | Local file |
|---|---|---|
| Russian | [Открыть презентацию](https://sasha-sazonova.github.io/triz-agent/presentation/ru/) | `presentation/ru/index.html` |
| English | [Open presentation](https://sasha-sazonova.github.io/triz-agent/presentation/en/) | `presentation/en/index.html` |

No server or build step is required. To open locally, double-click the file.
Keep `presentation/deck.js` next to the language folders; the pages reference
it as `../deck.js`.

Controls: `←` / `→`, `PageUp` / `PageDown`, wheel or swipe; `Esc` for the slide
index; `B` for static mode.

### Query the contradiction matrix

```sh
python3 agent/scripts/matrix_lookup.py 30 33
# improving 30 (External harm affects the object)
# × worsening 33 (Ease of operation)
# → principles 2, 25, 28, 39
```

The matrix is queried by script, not recalled by the model. Parameters are
checked against `agent/knowledge/39_parameters.yaml`; principles against
`agent/knowledge/40_principles.yaml`.

### Run the evaluation

```sh
python3 -m pip install -r requirements.txt
python3 agent/eval/run_eval.py --help
python3 agent/eval/run_eval.py --case classic-01 --run <path-to-run>
```

The evaluation checks contradiction accuracy, top-3 recall, P@5 principles,
traceability, groundedness, report completeness, stability, and time. The
runner and three seed cases are included; the two smoke runs are part of the
development log, not the repository. This is a v0.9 contour, not a production
acceptance claim.

### Open the C4 case

| Version | Live page | Local file |
|---|---|---|
| Russian | [Открыть кейс C4](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/ru/) | `cases/c4-dipole/ru/index.html` |
| English | [Open C4 case](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/en/) | `cases/c4-dipole/en/index.html` |

The case page links to the interactive stand:

| Theme | English | Russian |
|---|---|---|
| Dark | [dipole-en.html](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/assets/dipole-en.html) | [dipole.html](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/assets/dipole.html) |
| Light | [dipole-light-en.html](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/assets/dipole-light-en.html) | [dipole-light.html](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/assets/dipole-light.html) |

Keep the `.js` file next to its HTML page.

## Method in one paragraph

A technical contradiction is written as “if A, useful X improves but harmful Y
worsens”. The conflicting pair is mapped to two of the 39 parameters; the
contradiction matrix returns candidate principles; the effects database and
external research add physical mechanisms; at least three concepts from
different classes are generated, each traced to a principle or effect. An
independent critic scores physicality, contradiction resolution, ideality,
feasibility, and side effects. Only PASS/CONSIDER concepts go to synthesis.
The final report records risks, assumptions, and the next engineering step.

## Sources and attribution

The method is classical TRIZ by **Genrich S. Altshuller** (1946–1985). The
knowledge base and the seven-module reference implementation grew from the
open-source **Heinrich** project by Nick Scherbakov and contributors
(Apache-2.0). The agent runtime is **OpenClaw** (MIT). The isometric
explanations use **anatomy** by Ryan (MIT). External search uses EPO OPS,
USPTO, Rospatent, arXiv, Crossref, and Semantic Scholar. The Python scripts
(`run_eval.py`, `complete_principles.py`) use PyYAML (MIT).

See [`THIRD_PARTY.md`](THIRD_PARTY.md) for the full attribution and
[`LICENSES/`](LICENSES/) for the license texts.

## Status and limitations

- **Status:** v0.9 — the contour is live; the public evaluation set is small.
- **Patent check:** preliminary novelty assessment only, not a legal opinion
  and not a patentability guarantee.
- **Case numbers:** the C4 case uses estimates from the track B report, not
  measurements. `[estimate]` marks are intentional.
- **DEEP:** implemented and documented, but not yet field-tested.
- **Scope:** the repository contains the agent framework, the bilingual deck,
  and the C4 demo. It does not contain the full anti-drone research archive,
  client files, memory, or API keys.

## Rights

Copyright (c) 2026 Alexandra Sazonova. **All rights reserved.**

The repository is public for viewing and evaluation. Public visibility does not
grant a license to use, copy, modify, or redistribute the project content.
Third-party components retain their own licenses; see
[`THIRD_PARTY.md`](THIRD_PARTY.md) and [`NOTICE`](NOTICE).

## Repository and live pages

The project is public:

- Source: <https://github.com/sasha-sazonova/triz-agent>
- Landing page: <https://sasha-sazonova.github.io/triz-agent/>
- Presentation EN: <https://sasha-sazonova.github.io/triz-agent/presentation/en/>
- Presentation RU: <https://sasha-sazonova.github.io/triz-agent/presentation/ru/>
- Case C4 EN: <https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/en/>
- Case C4 RU: <https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/ru/>

The folder is already a git repository. See [`GITHUB_SETUP.md`](GITHUB_SETUP.md)
if you need to mirror it to another account or recreate the remote.
