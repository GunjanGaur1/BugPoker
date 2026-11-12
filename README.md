# BugPoker

BugPoker is a full-stack bluffing card game application where a human player competes against an AI-controlled opponent using simplified Cockroach Poker rules.

The project combines a React + TypeScript frontend with a FastAPI backend and implements game-state management, turn validation, strategic bot decisions, and persistent game sessions. It also includes a standalone Counterfactual Regret Minimization (CFR) research module demonstrating strategy optimization for imperfect-information games using Kuhn Poker.

## Features

### Human-vs-Bot Gameplay
- Interactive two-player bluffing card game.
- Hidden-card offers and creature declarations.
- Bot decisions for accepting or challenging offers.
- Game-state validation and winner detection.
- Automated bot decision-making using a heuristic policy.

### Game Backend and Persistence
- FastAPI REST API for game lifecycle management.
- Turn validation and game-action processing.
- SQLite-backed game persistence.
- Game history and completed-game summaries.
- Structured API endpoints for gameplay operations.

### AI and Strategy Research
- Standalone Counterfactual Regret Minimization implementation.
- Kuhn Poker imperfect-information game solver.
- Regret accumulation and average strategy computation.
- Strategy training through configurable iterations.
- Exploitability-style evaluation hooks.

### Frontend Experience
- React and TypeScript application.
- Interactive gameplay interface.
- Real-time game-state updates through API requests.
- Player action controls and game result displays.
- Responsive frontend architecture.

## Tech Stack

**Frontend**
- React
- TypeScript
- Vite
- CSS

**Backend**
- Python
- FastAPI
- Pydantic
- REST APIs

**Storage**
- SQLite

**AI and Algorithms**
- Counterfactual Regret Minimization (CFR)
- Imperfect-Information Games
- Kuhn Poker
- Heuristic-Based Decision Making

**Development and Testing**
- Docker
- Docker Compose
- Pytest
- GitHub Actions

## Architecture Overview

**Frontend Layer**

React application responsible for rendering the game interface, handling player interactions, and communicating with backend APIs.

**Backend API**

FastAPI application responsible for game creation, state management, action validation, bot decisions, and persistence.

**Game Engine**

Implements simplified Cockroach Poker mechanics, including hidden-card offers, accept/challenge decisions, card resolution, and terminal-state detection.

**Strategy Research Module**

Independent CFR implementation for Kuhn Poker, demonstrating regret minimization and average strategy computation in imperfect-information environments.

**Persistence Layer**

SQLite-backed storage for game sessions, actions, and completed-game information.

## Local Setup

### Docker (Recommended)

```bash
cp .env.example .env
docker compose up --build
```

Frontend: http://localhost:5173

Backend: http://localhost:8000

API Documentation: http://localhost:8000/docs

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

### Train the CFR Research Solver

```bash
cd backend
python -m app.solver.train --iterations 100000
```

## Project Structure

```text
BugPoker/
├── backend/
│   ├── app/
│   │   ├── game/
│   │   ├── solver/
│   │   └── main.py
│   └── tests/
├── frontend/
│   └── src/
├── docs/
├── .github/
├── docker-compose.yml
├── Makefile
└── README.md
```

## Future Improvements
- Monte Carlo CFR for Cockroach Poker.
- Information-set state abstraction.
- Trained strategy integration into the gameplay bot.
- Advanced strategy evaluation and benchmarking.
- Asynchronous training infrastructure using Celery and Redis.
- PostgreSQL-backed persistence and cloud deployment.
