import { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const creatures = ['bat','beetle','cockroach','fly','frog','scorpion','spider','toad']

type Game = {
  id: string; status: string; human_hand: string[]; bot_hand_count: number;
  history: any[]; winner?: string | null; last_result?: any
}
export default function App() {
  const [game, setGame] = useState<Game | null>(null)
  const [selected, setSelected] = useState(0)
  const [claim, setClaim] = useState('cockroach')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [solve, setSolve] = useState<any>(null)

  async function createGame() {
    setError('')
    const res = await fetch(`${API}/games`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({})})
    if (!res.ok) { setError('Could not create a game. Is the API running?'); return }
    setGame(await res.json())
  }
  async function offer() {
    if (!game) return
    setBusy(true); setError('')
    try {
      const res = await fetch(`${API}/games/${game.id}/actions`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'offer', card_index:selected, claim})})
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Action failed')
      setGame(data.game)
    } catch(e:any) { setError(e.message) } finally { setBusy(false) }
  }
  async function train() {
    setBusy(true); setError('')
    try {
      const res = await fetch(`${API}/solves`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({iterations:10000})})
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Training failed')
      setSolve(data)
    } catch(e:any) { setError(e.message) } finally { setBusy(false) }
  }
  useEffect(() => { createGame() }, [])

  return <main className="shell">
    <header><div className="brand"><span className="mark">N</span><div><h1>NashPlay</h1><p>GAME THEORY · BLUFFING AI</p></div></div><span className="live">● LOCAL DEMO</span></header>
    <section className="hero"><div><p className="eyebrow">IMPERFECT INFORMATION GAME</p><h2>Read the claim.<br/><em>Challenge the bluff.</em></h2><p className="sub">A two-player bluffing-card game with a baseline bot and a separate CFR research solver.</p></div><div className="hero-card"><span>♠</span><strong>STRATEGY<br/>MEETS<br/>UNCERTAINTY</strong><small>01 / NASHPLAY</small></div></section>
    {error && <div className="error">{error}</div>}
    {!game ? <button onClick={createGame}>Start game</button> : <section className="game">
      <div className="section-head"><div><p className="eyebrow">MATCH ROOM</p><h3>Human vs Bot</h3></div><span className={`status ${game.status}`}>{game.status}</span></div>
      <div className="opponent"><div className="avatar">AI</div><div><b>Strategy Bot</b><small>{game.bot_hand_count} hidden cards</small></div><div className="back-cards"><i>?</i><i>?</i><i>?</i></div></div>
      {game.last_result && <div className="result"><b>Last round</b><span>{game.last_result.outcome.replaceAll('_',' ')} · claimed {game.last_result.claim} · revealed {game.last_result.revealed_card}</span></div>}
      <div className="table"><div className="table-label">YOUR TURN — SELECT A CARD AND MAKE A CLAIM</div><div className="hand">{game.human_hand.map((c,i)=><button className={`playing-card ${selected===i?'selected':''}`} key={i} onClick={()=>setSelected(i)}><small>CREATURE</small><b>{c}</b><span>✦</span></button>)}</div>
      <div className="controls"><label>Claim a creature<select value={claim} onChange={e=>setClaim(e.target.value)}>{creatures.map(c=><option key={c}>{c}</option>)}</select></label><button className="primary" disabled={busy || game.status!=='active' || !!game.current_offer} onClick={offer}>Offer card to bot ↗</button></div></div>
      {game.status==='completed' && <div className="result"><b>Game completed</b><span>Winner: {game.winner}</span><button onClick={createGame}>New game</button></div>}
      <div className="history"><b>Round history</b>{game.history.length===0?<p>No rounds played yet.</p>:game.history.slice().reverse().map((h,i)=><div key={i}><span>Round {game.history.length-i}</span><span>{h.claim} → {h.decision} → {h.revealed_card}</span><strong>{h.outcome.replaceAll('_',' ')}</strong></div>)}</div>
    </section>}
    <section className="solver"><div><p className="eyebrow">RESEARCH MODULE</p><h3>Kuhn Poker CFR trainer</h3><p>Run a small imperfect-information regret-minimization experiment. This solver is separate from the Cockroach-style game bot.</p></div><button onClick={train} disabled={busy}>Train 10,000 iterations</button>{solve && <div className="solve-result">Training completed · {solve.information_sets} information sets · job {solve.job_id.slice(0,8)}</div>}</section>
    <footer><span>NASHPLAY / INDEPENDENT EDUCATIONAL IMPLEMENTATION</span><span>FastAPI · React · CFR</span></footer>
  </main>
}
