# Anukreon Sim API (v2)

Minimal NBA Monte Carlo API (FastAPI) suitable for Render deployment.

## Local dev
```bash
pip install -r requirements.txt
cp .env.example .env  # tweak ALLOW_ORIGINS etc. as needed
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/health

### Endpoint
`POST /api/sim/nba`
```json
{
  "off_home": 116, "def_home": 111, "pace_home": 97.5,
  "off_away": 113, "def_away": 112, "pace_away": 99.0,
  "total_line": 226.5, "spread_home_line": -4.5, "n": 20000
}
```

### Example cURL
```bash
curl -X POST http://127.0.0.1:8000/api/sim/nba \
 -H "Content-Type: application/json" \
 -d '{"off_home":116,"def_home":111,"pace_home":97.5,"off_away":113,"def_away":112,"pace_away":99.0,"total_line":226.5,"spread_home_line":-4.5,"n":20000}'
```

## Testing

Run the lightweight pytest suite to confirm the simulator returns the required
keys before pushing changes or deploying:

```bash
pytest -q
```

## Render

Connect repo, set build/start from Procfile.
Optionally use render.yaml for blueprint.
Add custom domain e.g. api-v2.anukreon.com (CNAME to Render).

---

## 🧪 Post-build Checklist for Codex
1. Run locally:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
2. `GET /health` → `{ "ok": true }`
3. `POST /api/sim/nba` with the README body returns JSON with all required keys.
4. Add basic GitHub Action later (optional) to run tests.

## 📝 Git Commit Plan (suggested)
- `chore: init FastAPI project scaffold`
- `feat: add NBA Monte Carlo engine`
- `feat: /api/sim/nba endpoint + health route`
- `chore: add Procfile, render.yaml, README`
- `test: add basic sim test`

---

### Next tasks (queue for Codex after deploy)
- Add `/api/ev` helper (probability + American odds → EV per 1u)
- Add `/api/sim/nfl` team-rating sim
- Add APScheduler job (cron) to snapshot sims hourly (SQLite)
