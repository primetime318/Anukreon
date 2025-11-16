from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.sim_nba import simulate_nba

router = APIRouter(prefix="/api/sim", tags=["sim"])


class NBASimIn(BaseModel):
    off_home: float = Field(..., description="Home OffRtg (pts/100)")
    def_home: float = Field(..., description="Home DefRtg (lower is better)")
    pace_home: float = Field(..., description="Home pace (possessions)")

    off_away: float = Field(..., description="Away OffRtg")
    def_away: float = Field(..., description="Away DefRtg")
    pace_away: float = Field(..., description="Away pace")

    total_line: float | None = None
    spread_home_line: float | None = None   # e.g., -4.5 if home favored by 4.5
    n: int = 20000


@router.post("/nba")
def nba_sim(body: NBASimIn):
    return simulate_nba(**body.model_dump())
