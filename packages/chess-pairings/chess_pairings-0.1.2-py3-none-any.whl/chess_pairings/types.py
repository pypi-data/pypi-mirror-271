from typing import Literal, TypeAlias, Sequence, Mapping
from pydantic import BaseModel

Result = Literal["1-0", "draw", "0-1", "+-", "-+"]

class Paired(BaseModel):
    white: str
    black: str
    white_no: int | None = None
    white_elo: int | None = None
    black_no: int | None = None
    black_elo: int | None = None
    result: Result | None = None
    tag: Literal['paired']

class Unpaired(BaseModel):
    player: str
    reason: str
    tag: Literal['unpaired']
    
Pairing: TypeAlias = Paired | Unpaired
RoundPairings: TypeAlias = Sequence[Pairing]
GroupPairings: TypeAlias = Sequence[RoundPairings]
TournamentPairings: TypeAlias = Mapping[str, GroupPairings]
"""Group -> Round -> Board -> Pairing"""