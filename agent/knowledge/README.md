# Knowledge base — provenance

The files in this folder implement the classical TRIZ knowledge base used by
the agent:

- `39_parameters.yaml` — 39 engineering parameters;
- `40_principles.yaml` — 40 inventive principles (extended);
- `contradiction_matrix.csv` — 1,190 improving/worsening pairs;
- `effects_database.json` — 15 physical effects;
- `76_standard_solutions.md` — Su-Field standard solutions;
- `ariz_85c.md` — ARIZ-85C, nine parts;
- `separation_principles.md` — four separation axes for physical contradictions;
- `evolution_trends.md` — eight trends of engineering system evolution;
- `glossary.md` — terminology.

## Provenance and rights

The 39 parameters, the base of the 40 principles, the effects database, and the
general shape of the contradiction matrix are derived from the open-source
**Heinrich: The Inventing Machine** project by Nick Scherbakov and contributors
(Apache-2.0, Copyright 2025). The matrix is expanded to 1,190 pairs; the
principles file is extended.

TRIZ itself is the methodology of Genrich S. Altshuller (1926–1998). The
additional references used in `76_standard_solutions.md` are Salamatov (1999),
Mann (2002), and ICG training materials; those works remain attributed to their
authors.

See the repository-level [`THIRD_PARTY.md`](../../THIRD_PARTY.md) and
[`LICENSES/Apache-2.0-heinrich.txt`](../../LICENSES/Apache-2.0-heinrich.txt).
