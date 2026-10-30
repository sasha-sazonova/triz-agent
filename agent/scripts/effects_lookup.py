#!/usr/bin/env python3
"""effects_lookup.py — детерминированный доступ к базе эффектов ТРИЗ.

Использование:
  python3 effects_lookup.py --function "измерить малые перемещения"  # поиск по функции
  python3 effects_lookup.py --tag sense_measure                       # по тегу функции
  python3 effects_lookup.py --principle 35                            # эффекты принципа №35
  python3 effects_lookup.py --find leidenfrost                        # по имени/алиасу (RU/EN)
  python3 effects_lookup.py --id supercritical_water                  # полная запись
  python3 effects_lookup.py --domain Fluid                            # по technical_domains
  python3 effects_lookup.py --list                                    # все записи: id | name | name_ru
  python3 effects_lookup.py --stats                                   # покрытие: категории × функции
  python3 effects_lookup.py --selftest                                # эталонные запросы (зачёт ≥70% top-3)

Каждая запись имеет function_tags (см. TAXONOMY) — поиск по функции первичен,
свободный текст (name/aliases/applications/description) — вторичен.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "knowledge"
DB_F = BASE / "effects_database.json"

TAXONOMY = {
    "move_substance": "перемещать вещество/объект",
    "fix_hold": "закреплять/удерживать",
    "change_shape": "изменять форму/геометрию",
    "change_state": "менять агрегатное состояние/фазу",
    "change_property": "изменять физическое свойство",
    "generate_field": "создавать поле/силу/действие",
    "convert_energy": "преобразовывать энергию между формами",
    "sense_measure": "измерять/обнаруживать/регистрировать",
    "transmit": "передавать энергию/вещество/сигнал/силу",
    "separate_mix": "разделять/очищать/сортировать",
    "mix_join": "смешивать/соединять",
    "store": "накапливать энергию/вещество",
    "suppress_harm": "подавлять/защищать от вредного фактора",
}

# ключевые слова запроса (RU/EN) -> тег функции
KEYWORDS = {
    "move_substance": ["перемест", "прокач", "перекач", "перенос", "move", "pump", "transport"],
    "fix_hold": ["закреп", "удерж", "фиксир", "зафикс", "fix", "hold", "lock", "clamp", "схват"],
    "change_shape": ["форм", "геометр", "изгиб", "изогн", "shape", "bend", "deform"],
    "change_state": ["агрегат", "фазов", "фазу", "фаз", "испар", "замороз", "плав", "конденса",
                     "state", "phase", "freez", "melt", "boil", "vaporiz"],
    "change_property": ["свойств", "прочн", "вязкост", "жёсткост", "жесткост", "цвет", "проводимост",
                        "охлад", "охлажд", "холод", "property", "stiff", "viscos", "strength",
                        "color", "conduct", "cool", "chill"],
    "generate_field": ["создать поле", "создава поле", "генерир", "поле", "силу", "field", "force",
                       "generate"],
    "convert_energy": ["энерг", "преобразов", "конверт", "energy", "convert"],
    "sense_measure": ["измер", "обнаруж", "детект", "регистриров", "сенсор", "датчик", "чувств",
                      "sense", "measure", "detect", "sensor", "diagnos"],
    "transmit": ["передать", "передач", "транслир", "отвест", "теплопередач", "тепл", "нагр",
                 "transmit", "relay", "channel", "heat"],
    "separate_mix": ["раздел", "очист", "фильтр", "сортир", "extract", "separate", "filter",
                     "purif", "sort"],
    "mix_join": ["смеш", "соедин", "объедин", "сварк", "mix", "join", "weld", "bond"],
    "store": ["накоп", "аккум", "запас", "store", "accumul", "buffer"],
    "suppress_harm": ["защит", "подав", "глуш", "экранир", "suppress", "protect", "shield",
                      "damp", "reduce harm"],
}

STOP = {"the", "and", "for", "with", "без", "или", "для", "как", "что", "при", "это", "есть"}


def load_db():
    data = json.loads(DB_F.read_text(encoding="utf-8"))
    return data["effects"]


def tags_for_query(q):
    q = q.lower()
    tags = []
    for slug, kws in KEYWORDS.items():
        for kw in kws:
            if kw in q:
                tags.append(slug)
                break
    if q in TAXONOMY:
        tags.insert(0, q)
    return sorted(set(tags))


def tokenize(text):
    return {w for w in re.findall(r"[a-zа-яё0-9\-]+", text.lower()) if len(w) > 3 and w not in STOP}


def score_effect(e, tags, words):
    s = 0.0
    if tags and set(e.get("function_tags", [])) & set(tags):
        s += 3
    # имя/алиасы: двустороннее вхождение токенов и русская морфология по 4-буквенному
    # префиксу ("тепло" ↔ "тепловая", "охладить" ↔ "охлаждение")
    name_tokens = set()
    for part in [e.get("name", ""), e.get("name_ru", "")] + list(e.get("aliases", []) or []):
        name_tokens |= tokenize(part)
    if words and (name_tokens & words or any(
            t in w for t in name_tokens for w in words if len(t) > 3)
            or any(t[:4] == w[:4] for t in name_tokens for w in words if len(t) >= 5 and len(w) >= 5)):
        s += 2
    hay_text = " ".join([e.get("description", ""), " ".join(e.get("applications", []) or [])]).lower()
    hits = sum(1 for w in words if w in hay_text)
    s += min(hits, 3) * 0.5
    return s


def search(effects, tags, words, principle=None, limit=5):
    out = []
    for e in effects:
        s = score_effect(e, tags, words)
        if principle is not None:
            if int(principle) in e.get("related_principles", []):
                s += 4
            elif tags or words:
                s = 0 if s < 2 else s  # при явном запросе по принципу — только релевантные
        if s > 0:
            out.append((s, len(e.get("function_tags", [])), e))
    # тай-брейк: более «специализированная» запись (меньше функций) выше
    out.sort(key=lambda t: (-t[0], t[1], t[2].get("id", "")))
    return [(s, e) for s, _, e in out[:limit]]


def brief(e):
    src = e.get("source", "")
    src_short = (src[:100] + "…") if len(src) > 100 else src
    return (f"- {e['id']} | {e['name']} / {e.get('name_ru','—')}"
            f" [{e.get('category','?')}] теги: {','.join(e.get('function_tags', []))}"
            f"\n  числа: {e.get('quantitative','—')}"
            f"\n  примен.: {('; '.join(e.get('applications', []) or [])[:160])}"
            f"\n  источник: {src_short}")


GOLD = [
    # (запрос по функции, валидный набор эффектов для top-3)
    ("измерить малые перемещения высокой точности",
     ["piezoelectric", "laser_interferometry", "photoelasticity", "hall_effect", "quantum_tunneling"]),
    ("охладить объект без движущихся частей", ["thermoelectric", "magnetocaloric", "radiative_cooling"]),
    ("быстро отвести большое тепло через стенку", ["heat_pipe", "critical_heat_flux", "latent_heat_phase_change"]),
    ("обнаружить зарождающуюся трещину в конструкции", ["acoustic_emission", "photoelasticity"]),
    ("получить водород из воды химическим путём", ["aluminum_water_reaction", "hydrothermal_synthesis"]),
    ("закрепить и отпустить деталь по команде",
     ["magnetorheological", "ferrofluid", "shape_memory", "shear_thickening",
      "electrostatic_chucking", "gecko_adhesion", "acoustic_levitation"]),
    ("очистить вещество на молекулярном уровне", ["supercritical_water", "adsorption_zeolite", "reverse_osmosis"]),
    ("создать сильное магнитное поле без катушки", ["superconductivity", "magnetocaloric", "magnetic_levitation"]),
]


def selftest(effects, threshold=0.7):
    ok, total, fails = 0, len(GOLD), []
    for q, valid in GOLD:
        tags = tags_for_query(q)
        words = tokenize(q)
        top = search(effects, tags, words, limit=3)
        got = [e["id"] for _, e in top]
        hit = bool(set(valid) & set(got))
        ok += hit
        if not hit:
            fails.append((q, valid, got))
    rate = ok / total
    print(f"selftest: {ok}/{total} запросов с валидным эффектом в top-3 ({rate:.0%}, порог {threshold:.0%})")
    for q, valid, got in fails:
        print(f"  FAIL: {q!r} ожидался любой из {valid} — got {got}")
    return 0 if rate >= threshold else 2


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    effects = load_db()

    if args[0] == "--list":
        for e in sorted(effects, key=lambda x: x["id"]):
            print(f"{e['id']:<38} {e['name']:<42} / {e.get('name_ru','—')}")
        return 0

    if args[0] == "--stats":
        by_cat, by_tag = {}, {}
        for e in effects:
            by_cat[e.get("category", "?")] = by_cat.get(e.get("category", "?"), 0) + 1
            for t in e.get("function_tags", []):
                by_tag[t] = by_tag.get(t, 0) + 1
        print(f"всего записей: {len(effects)}")
        print("категории:", json.dumps(by_cat, ensure_ascii=False, sort_keys=True))
        print("функции:", json.dumps(by_tag, ensure_ascii=False, sort_keys=True))
        missing = [e["id"] for e in effects if not e.get("source")]
        if missing:
            print("БЕЗ ИСТОЧНИКА:", ", ".join(missing))
        return 0

    if args[0] == "--selftest":
        return selftest(effects)

    if args[0] == "--tag":
        t = args[1]
        if t not in TAXONOMY:
            print(f"нет тега {t!r}; доступно: {', '.join(sorted(TAXONOMY))}")
            return 2
        hits = [e for e in effects if t in e.get("function_tags", [])]
        print(f"{TAXONOMY[t]} — {len(hits)} эффектов:")
        for e in hits:
            print(f"- {e['id']} | {e['name']} / {e.get('name_ru','—')} — {e.get('quantitative','—')[:110]}")
        return 0

    if args[0] == "--principle":
        n = int(args[1])
        hits = [e for e in effects if n in e.get("related_principles", [])]
        print(f"эффекты, реализующие принцип №{n}: {len(hits)}")
        for e in hits:
            print(f"- {e['id']} | {e['name']} / {e.get('name_ru','—')} — {e.get('description','')[:110]}")
        return 0

    if args[0] == "--find":
        q = args[1].lower()
        hits = [e for e in effects
                if q in e.get("name", "").lower()
                or q in e.get("name_ru", "").lower()
                or q in " ".join(e.get("aliases", []) or []).lower()
                or q in e.get("id", "").lower()]
        if not hits:
            print(f"не найдено: {q}")
            return 2
        for e in hits:
            print(brief(e))
        return 0

    if args[0] == "--id":
        for e in effects:
            if e.get("id") == args[1]:
                print(json.dumps(e, ensure_ascii=False, indent=1))
                return 0
        print(f"нет записи с id {args[1]!r}")
        return 2

    if args[0] == "--domain":
        d = args[1].lower()
        hits = [e for e in effects if d in " ".join(e.get("technical_domains", []) or []).lower()]
        print(f"домен {d!r}: {len(hits)} эффектов")
        for e in hits:
            print(f"- {e['id']} | {e['name']} / {e.get('name_ru','—')}")
        return 0

    if args[0] == "--function":
        qi = args.index("--function")
        q = args[qi + 1]
        as_json = "--json" in args
        principle = None
        if "--principle" in args:
            principle = args[args.index("--principle") + 1]
        tags = tags_for_query(q)
        words = tokenize(q)
        hits = search(effects, tags, words, principle=principle, limit=8)
        if not hits:
            print(f"по запросу {q!r} ничего; теги не распознаны: {tags or '—'}")
            return 2
        if as_json:
            print(json.dumps({"query": q, "tags": tags,
                              "results": [{"id": e["id"], "name": e["name"], "name_ru": e.get("name_ru"),
                                           "score": s, "quantitative": e.get("quantitative"),
                                           "source": e.get("source")} for s, e in hits]},
                             ensure_ascii=False, indent=1))
        else:
            print(f"запрос: {q} (теги: {', '.join(tags) if tags else '—'})")
            for s, e in hits:
                print(f"[score {s:.1f}] {brief(e)}")
        return 0

    print("нужно: --function | --tag | --principle | --find | --id | --domain | --list | --stats | --selftest")
    return 1


if __name__ == "__main__":
    sys.exit(main())
