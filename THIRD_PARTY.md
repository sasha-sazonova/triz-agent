# Third-party attribution and licenses

This repository builds on classical TRIZ and on several open-source projects.
The project's own content is licensed as “All rights reserved” (see
[`LICENSE`](LICENSE)); the components below retain their own licenses.

## 1. TRIZ methodology

- **Author:** Genrich S. Altshuller (Генрих Саулович Альтшуллер), 1926–1998.
- **Works used as the methodological basis:** “Creativity as an Exact Science”
  (1979), “To Find an Idea” (“Найти идею”), ARIZ-85C (1985), the 39×39
  contradiction matrix, the 40 inventive principles, the 76 standard solutions,
  and the trends of engineering system evolution.
- **What is used here:** the method, terminology, and the structure of the
  knowledge base. The specific YAML/CSV implementation in `agent/knowledge/`
  is derived from the open-source Heinrich project (see below) and extended.

TRIZ is a methodology, not a software license. The books and the method remain
attributed to their authors; this repository does not claim authorship of TRIZ.

## 2. Heinrich — The Inventing Machine

- **Project:** Heinrich: The Inventing Machine.
- **Author:** Nick Scherbakov and Heinrich contributors.
- **License:** Apache License 2.0 (Copyright 2025 Nick Scherbakov and Heinrich
  Contributors).
- **Repository:** <https://github.com/NickScherbakov/Heinrich-The-Inventing-Machine>
- **What is used here:** the 39 parameters, the base of the 40 principles, the
  effects database, the seven-module pipeline as a reference architecture, and
  the general shape of the contradiction matrix. The matrix in this repository
  is expanded to 1,190 pairs; the principles file is extended.
- **License text:** [`LICENSES/Apache-2.0-heinrich.txt`](LICENSES/Apache-2.0-heinrich.txt).

## 3. OpenClaw

- **Project:** OpenClaw — an open-source agent runtime.
- **Copyright:** OpenClaw Foundation, 2026.
- **License:** MIT.
- **Repository:** <https://github.com/openclaw/openclaw>
- **What is used here:** the agent/subagent model, skills, cron, workspace, and
  file-based memory patterns described in `agent/`.
- **License text:** [`LICENSES/MIT-openclaw.txt`](LICENSES/MIT-openclaw.txt).

## 4. anatomy

- **Project:** anatomy — crafted isometric SVG figures that explain technical
  ideas as real physical objects.
- **Author:** Ryan.
- **License:** MIT (Copyright (c) 2026 Ryan).
- **Repository:** <https://github.com/wheresryan22/anatomy>
- **What is used here:** the C4 interactive stand in
  `cases/c4-dipole/assets/` was built with the anatomy kit; the generated
  `dipole.js` / `dipole-light.js` include portions of the kit code.
- **License text:** [`LICENSES/MIT-anatomy.txt`](LICENSES/MIT-anatomy.txt).

## 5. External search APIs

The agent's search adapters use public APIs. Their terms of service apply to
the corresponding requests; no API keys are stored in this repository.

| Source | Purpose | Entry point |
|---|---|---|
| EPO OPS (Espacenet) | Worldwide patent search | <https://developers.epo.org> |
| USPTO Open Data Portal | US patent search | <https://data.uspto.gov> |
| Rospatent online API | RU patent search | <https://online.rospatent.gov.ru> |
| arXiv | Preprints | <https://arxiv.org> |
| Crossref | Journal metadata and DOIs | <https://www.crossref.org> |
| Semantic Scholar | Citation-aware paper search | <https://www.semanticscholar.org/product/api> |

## 6. Case material

The C4 “Differential dipole (Ormia)” page is an illustrative case, not a
measurement report. The concept has a **CONSIDER (32)** verdict in the track B
report and a preliminary patent category **N2**. The patent assessment is not a
legal conclusion and does not guarantee patentability. Numbers marked
`[estimate]` are case estimates.

The full anti-drone research archive, client files, API keys, and session memory
are intentionally not part of this repository.
