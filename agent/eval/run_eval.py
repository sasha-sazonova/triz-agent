#!/usr/bin/env python3
"""run_eval.py — автоматический подсчёт метрик eval по артефактам прогона.

Использование:
  python3 run_eval.py --case cases/classic-01.yaml --run <путь к projects/<case-id>>
  python3 run_eval.py --all-runs <путь к projects>       # все прогоны, у которых есть 07_report.md

Метрики (ТЗ §9.2):
  TP_top1    — пара из 02_contradiction.md совпала с improving/worsening или top3_any_of
  P@5        — |принципы агента (04, ранги 1-5) ∩ principles_any_of| / |принципы агента|
  trace      — (блок.) каждая концепция в 05 упоминает Принцип/№ и/или эффект
  report_full— (блок.) 07_report содержит разделы 1-8 шаблона
  grounded   — доля внешних утверждений с URL/DOI (грубая эвристика: строки с фактами)
  approx     — наличие [приближение] в 02 (информативно для триггера DEEP)

Выход: JSON в stdout + строка для results.tsv (stderr).
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# фактические форматы: "| **Основная** | 39 Productivity | 14 Strength |",
# "improving **№3 …**" (+следующей строкой worsening **№27**), "Пара №3 → №27", "Пары: 39→14"
PAIR_RE = re.compile(r"Основная\D{0,5}(\d{1,2})\s+[A-Za-z]\D{0,30}?(\d{1,2})\s+[A-Za-z]", re.I)
PAIR_RE2 = re.compile(r"improving[^№\d]{0,12}№?\s*(\d{1,2})[\s\S]{0,140}?worsening[^№\d]{0,12}№?\s*(\d{1,2})", re.I)
PAIR_RE3 = re.compile(r"(?:Пара|Пары):?\s*№?(\d{1,2})\s*[→-]\s*№?(\d{1,2})", re.I)
# принципы: "| 15 | Name", "Принцип №15", "П28", жирные "**№15 (Name" — заголовки "Пара №N" не матчатся
PRIN_RE = re.compile(r"(?:^\|\s*(\d{1,2})\s*\|\s*[A-ZА-Яa-zа-я])|(?:Принцип\s*№?\s*(\d{1,2}))|(?:П\.?\s*(\d{1,2}))|(?:\*\*№\s*(\d{1,2})\s*\()", re.I | re.M)
SECTIONS = ["Постановка", "Противоречие", "ИКР", "инструмент", "Концепции", "Сводная",
            "Риск", "Следующие шаги"]


def read(p):
    f = Path(p)
    return f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""


def extract_pair(text):
    # приоритет: машинно-читаемый eval-маркер агента
    m = re.search(r"<!--\s*eval:\s*pair=(\d{1,2})\s*,\s*(\d{1,2})", text)
    if m:
        return int(m.group(1)), int(m.group(2))
    for rex in (PAIR_RE, PAIR_RE2, PAIR_RE3):
        m = rex.search(text)
        if m:
            g = [int(x) for x in m.groups() if x and x.isdigit()]
            if len(g) >= 2:
                return g[0], g[1]
    return None


def eval_case(case_file, run_dir):
    case = yaml.safe_load(Path(case_file).read_text(encoding="utf-8"))
    exp = case.get("expected", {})
    cid = case.get("id", Path(case_file).stem)
    r = {"case": cid, "run": str(run_dir)}

    # спец-режим: детерминированный selftest базы эффектов (run_dir не нужен)
    if case.get("mode") == "EFFECTS_LOOKUP":
        import subprocess, sys
        script = Path(__file__).resolve().parent.parent / "scripts" / "effects_lookup.py"
        rc = subprocess.run([sys.executable, str(script), "--selftest"],
                            capture_output=True, text=True).returncode
        r["mode"] = "EFFECTS_LOOKUP"
        r["selftest_pass"] = rc == 0
        r["metric"] = exp.get("metric", "top3_any_of_hit_rate")
        r["threshold"] = exp.get("threshold", 0.70)
        r["TP_top1"] = r["selftest_pass"]   # единый флаг зачёта для сводных
        return r

    c02 = read(Path(run_dir) / "02_contradiction.md")
    c04 = read(Path(run_dir) / "04_principles.md")
    c05 = read(Path(run_dir) / "05_concepts.md")
    c07 = read(Path(run_dir) / "07_report.md")

    # TP_top1
    pair = extract_pair(c02)
    r["pair_found"] = pair
    want = exp.get("top3_any_of") or [[exp.get("improving"), exp.get("worsening")]]
    r["TP_top1"] = bool(pair) and (list(pair) in [list(x) for x in want] or
                                   (pair[0] == exp.get("improving") and pair[1] == exp.get("worsening")))

    # P@5 — принципы из ранжированной части 04 (таблица/список до 8 номеров)
    m = re.search(r"<!--\s*eval:\s*principles=([\d,\s]+)", c04)
    if m:
        prin_unique = [int(n) for n in m.group(1).replace(" ", "").split(",") if n][:5]
    else:
        raw = PRIN_RE.findall(c04)
        seen = set(); prin = []
        for tup in raw:
            for n in tup:
                if n and int(n) not in seen:
                    seen.add(int(n)); prin.append(int(n))
        prin_unique = prin[:5]
    by_pair = exp.get("principles_by_pair") or {}
    key = f"{pair[0]},{pair[1]}" if pair else None
    anyof = set(by_pair.get(key) or exp.get("principles_any_of", []))
    r["principles_source"] = "by_pair" if (key and key in by_pair) else "any_of"
    r["agent_principles"] = prin_unique
    r["P@5"] = round(len([p for p in prin_unique if p in anyof]) / len(prin_unique), 2) if prin_unique else None

    # trace: каждая «Концепция C» содержит «Принцип|П.» или «эффект»
    conzept = re.split(r"\n##+\s*C\d|\n##+\s*Концепц", c05)[1:]
    r["trace"] = all(re.search(r"Принцип|П\.?\s*№?\d|эффект", c, re.I) for c in conzept) if conzept else False
    r["n_concepts"] = len(conzept)

    # report_full
    r["report_full"] = bool(c07) and all(s.lower() in c07.lower() for s in SECTIONS)

    # grounded: доля URL-bearing строк среди строк с DOI/http рядом с фактами (грубая)
    fact_lines = [l for l in c07.splitlines() if re.search(r"\d{4}|doi|http", l, re.I)]
    sourced = [l for l in fact_lines if re.search(r"doi|http", l, re.I)]
    r["grounded"] = round(len(sourced) / len(fact_lines), 2) if fact_lines else None

    r["approx_mark"] = bool(re.search(r"\[приближение\]", c02)) and \
        not re.search(r"Пометок\s*\[приближение\]\s*нет|нет пометок?\s*\[приближение\]", c02, re.I)
    r["complete"] = all([c02, c04, c05, c07])
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case")
    ap.add_argument("--run")
    ap.add_argument("--all-runs")
    a = ap.parse_args()
    base = Path(__file__).resolve().parent

    if a.all_runs:
        runs = [d for d in Path(a.all_runs).iterdir() if d.is_dir()
                and (d / "07_report.md").exists()]
        results = [eval_case(base / "cases" / f"{d.name}.yaml", d) for d in runs
                   if (base / "cases" / f"{d.name}.yaml").exists()]
    else:
        results = [eval_case(a.case, a.run)]

    ok = sum(1 for r in results if r["TP_top1"])
    json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
    print(file=sys.stderr)
    print(f"TP_top1: {ok}/{len(results)} | trace: {sum(r['trace'] for r in results)}/{len(results)} | "
          f"full: {sum(r['report_full'] for r in results)}/{len(results)}", file=sys.stderr)


if __name__ == "__main__":
    main()
