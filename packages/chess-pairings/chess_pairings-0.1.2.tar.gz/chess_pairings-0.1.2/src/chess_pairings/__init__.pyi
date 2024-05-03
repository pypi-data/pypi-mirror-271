from .types import Result, Paired, Unpaired, Pairing, RoundPairings, GroupPairings, TournamentPairings
from .chess_results import scrape_pairings
from . import chess_results

__all__ = [
  'Result', 'Paired', 'Unpaired', 'Pairing', 'RoundPairings', 'GroupPairings', 'TournamentPairings',
  'chess_results', 'scrape_pairings',
]