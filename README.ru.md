# Генрих — ТРИЗ-агент-изобретатель

Копилот-изобретатель с гейтами на классической методологии ТРИЗ. Принимает
инженерную задачу на естественном языке (RU/EN), превращает её в формальное
противоречие, ищет по базе знаний ТРИЗ, генерирует концепции с полной
трассировкой и пропускает их через независимую критику и предварительную
патентную проверку.

Это не «кнопка, которая выдаёт десять идей». Это дисциплинированный маршрут:
**мини-задача → противоречие → ИКР → принципы и эффекты → концепции → критика →
отчёт**. Компромиссы запрещены; задача — развести противоречие в пространстве,
времени или структуре.

## Что внутри

| Слой | Что делает |
|---|---|
| **LITE** | Семь артефактов (`01_task` … `07_report`) с файловым gate control. Обычный цикл: 5–15 минут. |
| **DEEP / АРИЗ-85С** | Девять частей АРИЗ-85С для случаев, где LITE упирается: модель ресурсов, информационный фонд, смена постановки, контроль ответа. |
| **База знаний** | 39 параметров, 40 принципов, 1190 пар противоречий, 15 эффектов, 76 стандартных решений, 4 оси разделения, 8 трендов эволюции. |
| **Шесть craft-ролей** | Contradiction Miner, Principle Selector, Effects Lookup, Synectic, Critic, Patent Checker — one-shot субагенты с чистым контекстом. |
| **Ресёрч** | Адаптеры `science-search` (arXiv, Crossref, Semantic Scholar) и `patent-search` (EPO OPS, USPTO, Роспатент). |
| **Качество** | Scorecard по пяти осям, трассировка каждой концепции к принципу или эффекту, пороги eval, архив и уроки. |
| **Визуализация** | Изометрические инженерные объяснения на MIT-скилле `anatomy`. |

## Структура репозитория

```
triz-agent/
├── agent/                  # инструкции рантайма и база знаний
│   ├── AGENTS.md           # старт, gate control, правила субагентов
│   ├── SOUL.md             # персона и принципы метода
│   ├── IDENTITY.md         # идентичность агента
│   ├── USER.md             # шаблон профиля пользователя
│   ├── DESCRIPTION.md      # краткое описание проекта
│   ├── TOOLS.md            # инструменты и поисковые скиллы
│   ├── methods/            # LITE, DEEP/АРИЗ-85С, шаблон отчёта
│   ├── craft/              # шесть ролей субагентов
│   ├── knowledge/          # 39/40/матрица/эффекты/АРИЗ/тренды
│   ├── scripts/            # детерминированный запрос матрицы
│   └── eval/               # запуск оценки и seed-кейсы
├── presentation/
│   ├── ru/index.html       # русская презентация, 13 слайдов
│   ├── en/index.html       # английская презентация, 13 слайдов
│   ├── deck.js             # общий скрипт навигации
│   └── README.md
├── cases/
│   └── c4-dipole/
│       ├── ru/index.html   # русская страница кейса
│       ├── en/index.html   # английская страница кейса
│       ├── assets/         # интерактивный стенд, изображения, отчёт
│       └── README.md
├── LICENSES/               # тексты сторонних лицензий
├── THIRD_PARTY.md          # авторство и карта лицензий
├── GITHUB_SETUP.md         # как опубликовать папку
├── requirements.txt
└── LICENSE                 # лицензия проекта (All rights reserved)
```

## Быстрый старт

### Открыть презентацию

| Версия | Живая страница | Локальный файл |
|---|---|---|
| Русская | [Открыть презентацию](https://sasha-sazonova.github.io/triz-agent/presentation/ru/) | `presentation/ru/index.html` |
| English | [Open presentation](https://sasha-sazonova.github.io/triz-agent/presentation/en/) | `presentation/en/index.html` |

Сервер и сборка не нужны. Локально — двойной щелчок по файлу. Держите
`presentation/deck.js` рядом с языковыми папками: страницы ссылаются на него
как `../deck.js`.

Управление: `←` / `→`, `PageUp` / `PageDown`, колесо или свайп; `Esc` — индекс
слайдов; `B` — статичный режим.

### Запросить матрицу противоречий

```sh
python3 agent/scripts/matrix_lookup.py 30 33
# improving 30 (External harm affects the object)
# × worsening 33 (Ease of operation)
# → принципы 2, 25, 28, 39
```

Матрица запрашивается скриптом, а не «вспоминается» моделью. Параметры
сверяются с `agent/knowledge/39_parameters.yaml`, принципы — с
`agent/knowledge/40_principles.yaml`.

### Запустить оценку

```sh
python3 -m pip install -r requirements.txt
python3 agent/eval/run_eval.py --help
python3 agent/eval/run_eval.py --case classic-01 --run <path-to-run>
```

Eval проверяет точность противоречия, полноту топ-3, P@5 принципов,
трассируемость, groundedness, полноту отчёта, устойчивость и время. В репозиторий входят runner и три seed-кейса; два smoke-прогона — часть
журнала разработки, а не репозитория. Это контур v0.9, а не производственная
приёмка.

### Открыть кейс C4

| Версия | Живая страница | Локальный файл |
|---|---|---|
| Русская | [Открыть кейс C4](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/ru/) | `cases/c4-dipole/ru/index.html` |
| English | [Open C4 case](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/en/) | `cases/c4-dipole/en/index.html` |

Страница кейса ведёт на интерактивный стенд:

| Тема | English | Русский |
|---|---|---|
| Тёмная | [dipole-en.html](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/assets/dipole-en.html) | [dipole.html](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/assets/dipole.html) |
| Светлая | [dipole-light-en.html](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/assets/dipole-light-en.html) | [dipole-light.html](https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/assets/dipole-light.html) |

Держите `.js`-файл рядом с его HTML-страницей.

## Метод одним абзацем

Техническое противоречие записывается как «если A, полезное X улучшается, но
вредное Y ухудшается». Конфликтующая пара отображается на два из 39 параметров;
матрица противоречий возвращает принципы-кандидаты; база эффектов и внешний
ресёрч добавляют физические механизмы; генерируются минимум три концепции
разных классов, каждая — со ссылкой на принцип или эффект. Независимый критик
оценивает физичность, разрешение противоречия, идеальность, реализуемость и
побочные эффекты. В синтез проходят только PASS/CONSIDER. Итоговый отчёт
фиксирует риски, допущения и следующий инженерный шаг.

## Источники и авторство

Метод — классическая ТРИЗ **Генриха Сауловича Альтшуллера** (1946–1985). База
знаний и семимодульная референс-реализация выросли из открытого проекта
**Heinrich** (Nick Scherbakov и участники, Apache-2.0). Рантайм агента —
**OpenClaw** (MIT). Изометрические объяснения — **anatomy** (Ryan, MIT).
Внешний поиск — EPO OPS, USPTO, Роспатент, arXiv, Crossref, Semantic Scholar.
Python-скрипты (`run_eval.py`, `complete_principles.py`) используют PyYAML (MIT).

Полное авторство и карта лицензий — в [`THIRD_PARTY.md`](THIRD_PARTY.md),
тексты лицензий — в [`LICENSES/`](LICENSES/).

## Статус и ограничения

- **Статус:** v0.9 — контур живой; публичный набор eval небольшой.
- **Патентная проверка:** только предварительная оценка новизны, не юридическое
  заключение и не гарантия патентоспособности.
- **Числа кейса:** в C4 используются ориентиры из отчёта трека B, а не измерения.
  Пометки `[оценка]` стоят намеренно.
- **DEEP:** реализован и описан, но полем пока не проверен.
- **Объём:** в репозитории — каркас агента, двуязычная презентация и демо C4.
  Полного research-архива anti-drone, клиентских файлов, памяти и ключей здесь нет.

## Права

Copyright (c) 2026 Alexandra Sazonova. **All rights reserved.**

Репозиторий публичен для просмотра и оценки. Публичная видимость не даёт
лицензию на использование, копирование, изменение или распространение
содержимого проекта. Сторонние компоненты сохраняют свои лицензии; см.
[`THIRD_PARTY.md`](THIRD_PARTY.md) и [`NOTICE`](NOTICE).

## Репозиторий и живые страницы

Проект опубликован публично:

- Исходники: <https://github.com/sasha-sazonova/triz-agent>
- Стартовая страница: <https://sasha-sazonova.github.io/triz-agent/>
- Презентация EN: <https://sasha-sazonova.github.io/triz-agent/presentation/en/>
- Презентация RU: <https://sasha-sazonova.github.io/triz-agent/presentation/ru/>
- Кейс C4 EN: <https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/en/>
- Кейс C4 RU: <https://sasha-sazonova.github.io/triz-agent/cases/c4-dipole/ru/>

Папка уже является git-репозиторием. Команды для зеркалирования в другой
аккаунт или пересоздания remote — в [`GITHUB_SETUP.md`](GITHUB_SETUP.md).
