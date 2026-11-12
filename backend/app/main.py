from __future__ import annotations
import json, os, sqlite3, uuid, random
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .game.engine import new_game, offer_card, resolve_offer, bot_decision, Game, CREATURES

DATA_PATH = Path(os.getenv("DATABASE_PATH", "./data/nashplay.sqlite3"))
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

def db():
    conn = sqlite3.connect(DATA_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS games (
        id TEXT PRIMARY KEY, status TEXT NOT NULL, state_json TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    return conn

def save_game(g: Game):
    payload = {k: getattr(g, k) for k in ("id","status","deck","human_hand","bot_hand","current_offer","history","winner","last_result")}
    with db() as conn:
        conn.execute("""INSERT INTO games(id,status,state_json) VALUES(?,?,?)
            ON CONFLICT(id) DO UPDATE SET status=excluded.status,state_json=excluded.state_json,updated_at=CURRENT_TIMESTAMP""",
            (g.id, g.status, json.dumps(payload)))

def load_game(game_id: str) -> Optional[Game]:
    with db() as conn:
        row = conn.execute("SELECT state_json FROM games WHERE id=?", (game_id,)).fetchone()
    if not row:
        return None
    d = json.loads(row["state_json"])
    return Game(**d)

app = FastAPI(title="NashPlay API", version="0.1.0", description="Independent bluffing-game and game-theory research project")
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class CreateGame(BaseModel):
    seed: Optional[int] = None

class OfferRequest(BaseModel):
    action: str = Field(description="'offer' or 'resolve'")
    card_index: Optional[int] = None
    claim: Optional[str] = None
    decision: Optional[str] = None

@app.get("/healthz")
def health():
    return {"status": "ok", "service": "nashplay-api"}

@app.post("/games")
def create_game(req: CreateGame):
    game = new_game(req.seed)
    save_game(game)
    return game.public()

@app.get("/games/{game_id}")
def get_game(game_id: str):
    game = load_game(game_id)
    if not game:
        raise HTTPException(404, "Game not found")
    return game.public()

@app.post("/games/{game_id}/actions")
def game_action(game_id: str, req: OfferRequest):
    game = load_game(game_id)
    if not game:
        raise HTTPException(404, "Game not found")
    try:
        if req.action == "offer":
            if req.card_index is None or req.claim is None:
                raise ValueError("card_index and claim are required")
            result = offer_card(game, req.card_index, req.claim)
            # Bot immediately chooses a response; reveal is returned to the player.
            decision = bot_decision(req.claim, game.bot_hand)
            result["bot_decision"] = decision
            result["resolution"] = resolve_offer(game, decision)
        elif req.action == "resolve":
            if req.decision is None:
                raise ValueError("decision is required")
            result = resolve_offer(game, req.decision)
        else:
            raise ValueError("Unknown action")
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    save_game(game)
    return {"result": result, "game": game.public()}

@app.get("/games/completed/latest")
def latest_completed():
    with db() as conn:
        row = conn.execute("SELECT state_json FROM games WHERE status='completed' ORDER BY updated_at DESC LIMIT 1").fetchone()
    return json.loads(row["state_json"]) if row else None

# Local synchronous training endpoint; intentionally bounded to keep API requests responsive.
SOLVES = {}
class SolveRequest(BaseModel):
    iterations: int = Field(default=10000, ge=100, le=200000)

@app.post("/solves")
def start_solve(req: SolveRequest):
    from .solver.kuhn_cfr import KuhnCFR
    job_id = str(uuid.uuid4())
    solver = KuhnCFR()
    strategy = solver.train(req.iterations)
    SOLVES[job_id] = {"status": "completed", "iterations": req.iterations, "information_sets": len(strategy), "strategy": strategy}
    return {"job_id": job_id, **{k:v for k,v in SOLVES[job_id].items() if k != "strategy"}}

@app.get("/solves/{job_id}")
def get_solve(job_id: str):
    if job_id not in SOLVES:
        raise HTTPException(404, "Solve job not found in this API process")
    return SOLVES[job_id]
