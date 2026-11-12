# NashPlay — Cockroach Poker AI (independent implementation)

An independently written, educational full-stack implementation inspired by the *feature set* of BugPoker:
- Human vs bot bluffing-card gameplay (two-player simplified Cockroach Poker rules)
- FastAPI REST API with turn validation
- SQLite persistence for games and actions
- A separate Counterfactual Regret Minimization (CFR) trainer for Kuhn Poker, with exploitability-style evaluation hooks
- React + TypeScript + Vite frontend
- Docker Compose development setup
- Pytest tests and GitHub Actions CI

> This is a new implementation, not a copy of another repository. It does not include the original author's code, strategy checkpoint, assets, AWS account configuration, or deployment secrets. The included CFR trainer solves Kuhn Poker as a standalone research module; it is not represented as a trained Cockroach Poker equilibrium policy.

## Requirements
- Docker Desktop (recommended), or Python 3.11+ and Node.js 20+

## Run with Docker
```bash
cp .env.example .env
docker compose up --build
```
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/healthz

## Run backend locally
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run frontend locally
```bash
cd frontend
npm install
npm run dev
```

## Run tests
```bash
cd backend
pip install -r requirements.txt
pytest -q
```

## Train the research CFR solver
```bash
cd backend
python -m app.solver.train --iterations 100000
```
This writes `backend/data/kuhn_strategy.json`. It is a small imperfect-information Kuhn Poker solver intended to demonstrate regret minimization, not a Cockroach Poker strategy checkpoint.

## API
- `GET /healthz`
- `POST /games`
- `GET /games/{game_id}`
- `POST /games/{game_id}/actions`
- `GET /games/completed/latest`
- `POST /solves` — enqueue a background CFR training job (local process implementation)
- `GET /solves/{job_id}`

## Game rules (simplified two-player mode)
The human offers a hidden card and names a creature. The bot chooses accept or challenge. If the bot accepts, the bot receives the card; if it challenges, the card is revealed and the liar receives it. Four cards of one creature or all cards of a creature in a player's hand ends the game. This simplified ruleset is deliberately documented so the implementation is testable and understandable.

## Project structure
```text
backend/
  app/
    game/       game state, rules, bot policy
    solver/     standalone Kuhn Poker CFR implementation
    main.py     REST API and persistence
  tests/
frontend/
  src/
infra/
.github/workflows/
```

## Security
Copy `.env.example` to `.env`. Never commit real credentials, cloud account identifiers, private keys, or production database URLs. No AWS resources are provisioned by this project.
