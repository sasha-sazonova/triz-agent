# C4 — Differential Dipole (Ormia)

A bilingual case page for the passive acoustic detection concept C4 from the
anti-drone track. The concept uses a pair of mechanically coupled membranes to
subtract common-mode noise and estimate bearing from the time difference of
arrival:

```
τ = d · sin θ / c
```

The interactive stand lets the reader move a quadcopter model along an arc and
toggle a common noise source.

## Files

- `ru/index.html` — Russian case page.
- `en/index.html` — English case page.
- `assets/dipole.html` / `assets/dipole-light.html` — interactive stand, Russian (dark / light).
- `assets/dipole-en.html` / `assets/dipole-light-en.html` — interactive stand, English (dark / light).
- `assets/dipole.js` / `assets/dipole-light.js` and their `-en` counterparts — external scripts; keep them next to the HTML.
- `assets/img/` — figures used by the case page.
- `assets/otchet-anatomy-integratsiya.html` — Russian report on the Anatomy integration.

Open `ru/index.html` or `en/index.html` directly; links to the stand and images
are relative and work without a server.

## Status

The concept is a CONSIDER (32) reserve from the track B report, with a
preliminary patent assessment N2. Numbers are case estimates, not measurements.
The patent assessment is not a legal conclusion.
