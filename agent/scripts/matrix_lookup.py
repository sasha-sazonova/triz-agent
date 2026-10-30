#!/usr/bin/env python3
"""matrix_lookup.py — детерминированный доступ к матрице противоречий ТРИЗ.

Использование:
  python3 matrix_lookup.py 9 19          # принципы на пару improving=9 worsening=19
  python3 matrix_lookup.py 9 19 --json   # то же в JSON
  python3 matrix_lookup.py --find speed  # найти параметр по имени (регистронезависимо)
  python3 matrix_lookup.py --principle 15  # определение принципа с подпринципами
  python3 matrix_lookup.py --list        # все 39 параметров

Матрица симметрична: если пара (a,b) не найдена, проверяется (b,a).
Если пары нет в курируемом сабсете — печатает пусто и подсказку (код выхода 2).
"""
import csv
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "knowledge"
PARAMS_F = BASE / "39_parameters.yaml"
PRINC_F = BASE / "40_principles.yaml"
MATRIX_F = BASE / "contradiction_matrix.csv"


def load_params():
    try:
        import yaml
        data = yaml.safe_load(PARAMS_F.read_text(encoding="utf-8"))
        return {p["id"]: p for p in data["parameters"]}
    except ImportError:
        # минимальный парсер нужных полей (без PyYAML)
        params = {}
        pid = None
        for line in PARAMS_F.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("- id:"):
                pid = int(s.split(":", 1)[1])
                params[pid] = {"id": pid}
            elif pid and s.startswith("name:"):
                params[pid]["name"] = s.split(":", 1)[1].strip()
            elif pid and s.startswith("description:"):
                params[pid]["description"] = s.split(":", 1)[1].strip()
        return params


def load_principles():
    text = PRINC_F.read_text(encoding="utf-8")
    try:
        import yaml
        data = yaml.safe_load(text)
        return {p["id"]: p for p in data["principles"]}
    except ImportError:
        out = {}
        pid = None
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("- id:"):
                pid = int(s.split(":", 1)[1])
                out[pid] = {"id": pid}
            elif pid and s.startswith("name:"):
                out[pid]["name"] = s.split(":", 1)[1].strip()
            elif pid and s.startswith("description:"):
                out[pid]["description"] = s.split(":", 1)[1].strip()
        return out


def load_matrix():
    m = {}
    with open(MATRIX_F, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            a = int(row["improving_parameter"])
            b = int(row["worsening_parameter"])
            seen, pr = set(), []
            for x in row["recommended_principles"].split(";"):
                x = x.strip()
                if not x:
                    continue
                n = int(x)
                if n not in seen:
                    seen.add(n)
                    pr.append(n)
            m[(a, b)] = pr
            if (b, a) not in m:      # каноническая матрица асимметрична:
                m[(b, a)] = pr       # зеркалим ТОЛЬКО отсутствующие пары
    return m


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1

    if args[0] == "--list":
        for pid, p in sorted(load_params().items()):
            print(f"{pid:>2}  {p.get('name','?')}")
        return 0

    if args[0] == "--find":
        q = args[1].lower()
        found = [(i, p) for i, p in sorted(load_params().items())
                 if q in p.get("name", "").lower() or q in p.get("description", "").lower()
                 or q in p.get("name_ru", "").lower() or q in p.get("description_ru", "").lower()]
        if not found:
            print(f"не найдено: {q}")
            return 2
        for i, p in found:
            print(f"{i:>2}  {p.get('name')} — {p.get('description','')}")
        return 0

    if args[0] == "--principle":
        n = int(args[1])
        pr = load_principles().get(n)
        if not pr:
            print(f"принцип {n} не найден (1..40)")
            return 2
        print(json.dumps(pr, ensure_ascii=False, indent=1))
        return 0

    # пара параметров
    try:
        a, b = int(args[0]), int(args[1])
    except (IndexError, ValueError):
        print("нужно: matrix_lookup.py <improving> <worsening> | --find | --list | --principle N")
        return 1
    as_json = "--json" in args

    params, matrix = load_params(), load_matrix()
    if a not in params or b not in params:
        print(f"параметры должны быть из 1..39 (есть {sorted(params)})")
        return 2
    pr = matrix.get((a, b)) or matrix.get((b, a))
    if not pr:
        msg = (f"пара ({a}, {b}) отсутствует в курируемой матрице; "
               f"принципы-кандидаты по частоте: 1, 2, 10, 15, 35 [матрица не содержит пару]")
        print(json.dumps({"improving": a, "worsening": b, "principles": []},
                         ensure_ascii=False) if as_json else msg)
        return 2

    if as_json:
        print(json.dumps({
            "improving": {"id": a, "name": params[a].get("name")},
            "worsening": {"id": b, "name": params[b].get("name")},
            "principles": [{"id": n, "name": load_principles().get(n, {}).get("name")} for n in pr],
        }, ensure_ascii=False, indent=1))
    else:
        print(f"improving {a} ({params[a].get('name')}) × worsening {b} ({params[b].get('name')})")
        print("рекомендованные принципы: " + ", ".join(
            f"№{n} {load_principles().get(n, {}).get('name', '?')}" for n in pr))
    return 0


if __name__ == "__main__":
    sys.exit(main())
