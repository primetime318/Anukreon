"""NBA simulation utilities."""
from __future__ import annotations

from random import Random
from typing import Dict, Optional

try:  # pragma: no cover - exercised implicitly when numpy is installed
    import numpy as np  # type: ignore
except ImportError:  # pragma: no cover
    np = None  # type: ignore


def _simulate_with_numpy(
    off_home: float,
    def_home: float,
    pace_home: float,
    off_away: float,
    def_away: float,
    pace_away: float,
    total_line: Optional[float],
    spread_home_line: Optional[float],
    n: int,
) -> Dict[str, float | int]:
    rng = np.random.default_rng(42)  # type: ignore[call-arg]

    poss = rng.normal(loc=(pace_home + pace_away) / 2.0, scale=2.0, size=n)

    home_eff = 0.6 * off_home + 0.4 * (100 - def_away)
    away_eff = 0.6 * off_away + 0.4 * (100 - def_home)

    home_pts = poss * rng.normal(loc=home_eff / 100.0, scale=0.025, size=n)
    away_pts = poss * rng.normal(loc=away_eff / 100.0, scale=0.025, size=n)

    shock = rng.normal(0, 2.5, size=n)
    home_pts = home_pts + 0.35 * shock
    away_pts = away_pts + 0.35 * shock

    diff = (home_pts - away_pts).tolist()
    totals = (home_pts + away_pts).tolist()

    return _build_output(home_pts.tolist(), away_pts.tolist(), diff, totals, total_line, spread_home_line, n)


def _simulate_with_python(
    off_home: float,
    def_home: float,
    pace_home: float,
    off_away: float,
    def_away: float,
    pace_away: float,
    total_line: Optional[float],
    spread_home_line: Optional[float],
    n: int,
) -> Dict[str, float | int]:
    rng = Random(42)

    mean_pace = (pace_home + pace_away) / 2.0
    poss = [rng.gauss(mean_pace, 2.0) for _ in range(n)]

    home_eff = 0.6 * off_home + 0.4 * (100 - def_away)
    away_eff = 0.6 * off_away + 0.4 * (100 - def_home)

    home_pts = [p * rng.gauss(home_eff / 100.0, 0.025) for p in poss]
    away_pts = [p * rng.gauss(away_eff / 100.0, 0.025) for p in poss]

    shocks = [rng.gauss(0.0, 2.5) for _ in range(n)]
    home_pts = [h + 0.35 * s for h, s in zip(home_pts, shocks)]
    away_pts = [a + 0.35 * s for a, s in zip(away_pts, shocks)]

    diff = [h - a for h, a in zip(home_pts, away_pts)]
    totals = [h + a for h, a in zip(home_pts, away_pts)]

    return _build_output(home_pts, away_pts, diff, totals, total_line, spread_home_line, n)


def _build_output(
    home_pts: list[float],
    away_pts: list[float],
    diff: list[float],
    totals: list[float],
    total_line: Optional[float],
    spread_home_line: Optional[float],
    n: int,
) -> Dict[str, float | int]:
    out: Dict[str, float | int] = {
        "home_win_pct": float(sum(d > 0 for d in diff) / n),
        "away_win_pct": float(sum(d < 0 for d in diff) / n),
        "avg_home": float(_mean(home_pts)),
        "avg_away": float(_mean(away_pts)),
        "fair_spread_home": float(-_mean(diff)),
        "fair_total": float(_mean(totals)),
        "n_sims": int(n),
    }

    if total_line is not None:
        out["p_over_total"] = float(sum(total > total_line for total in totals) / n)
        out["p_under_total"] = float(sum(total < total_line for total in totals) / n)

    if spread_home_line is not None:
        out["p_home_cover"] = float(sum(d >= spread_home_line for d in diff) / n)
        out["p_away_cover"] = float(sum(-d >= -spread_home_line for d in diff) / n)

    return out


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def simulate_nba(
    off_home: float,
    def_home: float,
    pace_home: float,
    off_away: float,
    def_away: float,
    pace_away: float,
    total_line: Optional[float] = None,
    spread_home_line: Optional[float] = None,
    n: int = 20000,
) -> Dict[str, float | int]:
    """Run a possession-based Monte Carlo simulation for an NBA matchup."""
    if n <= 0:
        raise ValueError("Simulation count must be positive")

    if np is not None:  # pragma: no branch
        return _simulate_with_numpy(
            off_home,
            def_home,
            pace_home,
            off_away,
            def_away,
            pace_away,
            total_line,
            spread_home_line,
            n,
        )

    return _simulate_with_python(
        off_home,
        def_home,
        pace_home,
        off_away,
        def_away,
        pace_away,
        total_line,
        spread_home_line,
        n,
    )
