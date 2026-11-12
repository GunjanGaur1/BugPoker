# Architecture

```text
React + TypeScript
       |
       | HTTP / JSON
       v
FastAPI API
  |          |
  v          v
Game       CFR research
engine     module (Kuhn Poker)
  |
  v
SQLite persistence
```

## Boundaries
- `game/engine.py`: deterministic rules and state transitions.
- `main.py`: HTTP validation, persistence, and API composition.
- `solver/kuhn_cfr.py`: isolated imperfect-information CFR research implementation.
- `frontend/src`: browser UI and API calls.

## Known limitations
- The shipped bot uses a transparent heuristic baseline, not the CFR strategy file.
- Game rules are a documented two-player simplification, not full multiplayer Cockroach Poker.
- The `/solves` route runs synchronously and stores job results in process memory. A production iteration should move this to a durable queue and persistent solve records.
- SQLite is used for easy local startup; a later PostgreSQL adapter can replace it.
- No production deployment or cloud infrastructure is configured.
