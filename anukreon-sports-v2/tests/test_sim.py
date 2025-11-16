from app.sim_nba import simulate_nba


def test_sim_outputs_keys():
    out = simulate_nba(
        off_home=116,
        def_home=111,
        pace_home=97.5,
        off_away=113,
        def_away=112,
        pace_away=99.0,
        total_line=226.5,
        spread_home_line=-4.5,
        n=1000,
    )
    for key in [
        "home_win_pct",
        "away_win_pct",
        "avg_home",
        "avg_away",
        "fair_spread_home",
        "fair_total",
        "n_sims",
        "p_over_total",
        "p_under_total",
        "p_home_cover",
        "p_away_cover",
    ]:
        assert key in out
