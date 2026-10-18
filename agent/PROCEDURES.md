# PROCEDURES.md — примеры вызовов субагентов

> Все пути абсолютные. WS = $TRIZ_WORKSPACE (после деплоя;
> при локальной отладке — путь к agent/ в проекте).
> ВСЕГДА `mode:"run"` + `cleanup:"delete"`. `mode:"session"` ЗАПРЕЩЁН.

## Contradiction Miner (Этап 1)
```
WS="$TRIZ_WORKSPACE"
sessions_spawn({
  "runtime": "subagent", "mode": "run", "runTimeoutSeconds": 300,
  "task": "Прочитай ${WS}/craft/CONTRADICTION_MINER_AGENT.md и следуй ему.\nВход: ${WS}/projects/<задача>/01_task.md\nСправочник: ${WS}/knowledge/39_parameters.yaml\nСохрани: ${WS}/projects/<задача>/02_contradiction.md"
})
```

## Principle Selector (Этап 3)
```
sessions_spawn({
  "runtime": "subagent", "mode": "run", "runTimeoutSeconds": 300,
  "task": "Прочитай ${WS}/craft/PRINCIPLE_SELECTOR_AGENT.md и следуй ему.\nВход: ${WS}/projects/<задача>/02_contradiction.md (+ 03_ikr.md, если есть)\nБаза: ${WS}/knowledge/{40_principles.yaml, contradiction_matrix.csv}\nСохрани: ${WS}/projects/<задача>/04_principles.md"
})
```

## Effects Lookup (Этап 3, параллельно с Principle Selector)
```
sessions_spawn({
  "runtime": "subagent", "mode": "run", "runTimeoutSeconds": 300,
  "task": "Прочитай ${WS}/craft/EFFECTS_LOOKUP_AGENT.md и следуй ему.\nВход: ${WS}/projects/<задача>/{01_task,02_contradiction}.md\nБаза эффектов: ${WS}/knowledge/effects_database.json\nСохрани: ${WS}/projects/<задача>/04a_effects.md"
})
```

## Synectic (только при тупике Этапа 4)
```
sessions_spawn({
  "runtime": "subagent", "mode": "run", "runTimeoutSeconds": 300,
  "task": "Прочитай ${WS}/craft/SYNECTIC_AGENT.md и следуй ему.\nВход: ${WS}/projects/<задача>/{02_contradiction,03_ikr,05_concepts}.md\nСохрани: ${WS}/projects/<задача>/05a_synectic.md"
})
```

## Critic (Этап 5)
```
sessions_spawn({
  "runtime": "subagent", "mode": "run", "runTimeoutSeconds": 600,
  "task": "Прочитай ${WS}/craft/CRITIC_AGENT.md и следуй ему.\nВход: ${WS}/projects/<задача>/{05_concepts,02_contradiction,03_ikr}.md\nСохрани: ${WS}/projects/<задача>/06_critique.md"
})
```

## Patent Checker (Этап 5, после критика)
```
sessions_spawn({
  "runtime": "subagent", "mode": "run", "runTimeoutSeconds": 600,
  "task": "Прочитай ${WS}/craft/PATENT_CHECKER_AGENT.md и следуй ему.\nВход: ${WS}/projects/<задача>/{05_concepts,06_critique}.md\nСохрани: ${WS}/projects/<задача>/06a_patent.md"
})
```

## Researcher — долгий внешний ресёрч (асинхронно)
```
sessions_spawn({
  "runtime": "subagent", "mode": "run", "cleanup": "delete",
  "task": "Найди <тема/область> … Сохрани отчёт: projects/<задача>/research/<имя>.md"
})
```
Забор результата — one-shot cron через 25 мин:
```json
{
  "name": "Забор: researcher <задача>",
  "schedule": {"kind": "at", "at": "<сейчас+20мин UTC>"},
  "sessionTarget": "isolated",
  "payload": {"kind": "agentTurn", "message": "Проверь файл projects/<задача>/research/<имя>.md и продолжи задачу <задача> с этапа <N>."},
  "delivery": {"mode": "none"},
  "deleteAfterRun": true
}
```

## Матрица (детерминированно, не через LLM)
```bash
python3 ${WS}/scripts/matrix_lookup.py <improving> <worsening>
python3 ${WS}/scripts/matrix_lookup.py --find "weight"
```

## Локальная адаптация (локальный контур, 2026-09-30)

- Рантайм: AutoClaw (встроенный OpenClaw), канал — webchat; сервер <reference-server> — **референс** (read-only, не трогать без решения владельца).
- **researcher-агента локально нет**: внешний ресёрч — анонимный субагент-ресёрчер; отчёт сохранять в `projects/<задача>/research/<файл>.md`; забор — one-shot cron +25 мин (фолбэк +45 мин); при деградации поиска — обязательная пометка `SOURCES_MISSING`.
- Субагенты: анонимные one-shot (`mode:"run"`, `cleanup:"delete"`); на этом рантайме проходы медленные — таймауты 600 с (тяжёлые роли 900, части DEEP до 1200); при отказе — 1 повтор, затем fallback «делаю сам с пометкой».
- exec: heredoc (`<<`) блокируется safety guard — сложные команды только скриптом через write tool; SSH не использовать без нужды.
- Skills: `science-search`, `patent-search` установлены в `.agents/skills/`; запускать системным `python3` (только stdlib, venv не требуется). Ключи — `.env` воркспейса (права 600).
- Heartbeat: выключен; при включении — задачи из HEARTBEAT.md, ack ≤300 символов, окно тишины 23:00–08:00.
