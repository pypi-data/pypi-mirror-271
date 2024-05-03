from haskellian import Either
from chess_pairings import GroupPairings
from . import download_pairings, parse_rounds, ScrapingError

async def scrape_pairings(db_key: int) -> Either[ScrapingError, GroupPairings]:
  return (await download_pairings(db_key)).bind(parse_rounds)