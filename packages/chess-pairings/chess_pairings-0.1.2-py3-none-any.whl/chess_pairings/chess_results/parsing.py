from typing import Iterable
from dataclasses import dataclass
import re
from bs4 import BeautifulSoup, Tag
from haskellian import Either, Left, Right, IsLeft, iter as I, Iter, either as E
from chess_pairings import Result, Paired, Unpaired, Pairing
from .errors import ParsingError

def parse_result(result: str) -> Result | None:
  """Parse result string from chessresults page
  - `'1 - 0' -->` white victory
  - `'0 - 1' -->` black victory
  - `'"½ - ½"' -->` draw
  - `'+ - -' -->` white victory by forfeit
  - `'- - +' -->` black victory by forfeit
  - any other --> None
  """
  match result:
    case "1 - 0":
      return "1-0"
    case "0 - 1":
      return "0-1"
    case "½ - ½":
      return "draw"
    case "+ - -":
      return "+-"
    case "- - +":
      return "-+"

@dataclass
class Columns:
  white: int
  black: int
  result: int
  white_no: int | None = None
  white_elo: int | None = None
  black_no: int | None = None
  black_elo: int | None = None

@dataclass
class Row:
  white: str
  black: str
  result: str
  white_no: str | None = None
  white_elo: str | None = None
  black_no: str | None = None
  black_elo: str | None = None

def parse_columns(soup: BeautifulSoup) -> Either[ParsingError, Columns]:
  for row in soup.find_all('tr'):
    try:
      headers = [th.get_text(strip=True) for th in row.find_all("th", recursive=False)]
      if headers != []:
        white = I.find_idx(lambda x: x == "Name", headers)
        black = I.find_last_idx(lambda x: x == "Name", headers)
        result = I.find_idx(lambda x: x == "Result", headers)
        white_no = I.find_idx(lambda x: x == "No.", headers)
        white_elo = I.find_idx(lambda x: x == "Rtg", headers)
        black_no = I.find_last_idx(lambda x: x == "No.", headers)
        black_elo = I.find_last_idx(lambda x: x == "Rtg", headers)
        if white is not None and black is not None and result is not None:
          return Right(Columns(white, black, result, white_no, white_elo, black_no, black_elo))
    except:
      ...
  return Left(ParsingError('Unable to find headers'))

@I.lift
def extract_round(table: Tag, columns: Columns) -> Iterable[Row]:
  rows = table.find_all('tr', class_=["CRng1", "CRng2", "CRg1", "CRg2"])
  for row in rows:
    try:
      cols = list(row.find_all("td"))
      col_text = lambda i: cols[i].get_text(strip=True)
      yield Row(
        white=col_text(columns.white), black=col_text(columns.black), result=col_text(columns.result),
        white_no=col_text(columns.white_no) if columns.white_no is not None else None,
        white_elo=col_text(columns.white_elo) if columns.white_elo is not None else None,
        black_no=col_text(columns.black_no) if columns.black_no is not None else None,
        black_elo=col_text(columns.black_elo) if columns.black_elo is not None else None,
      )
    except:
      ...

def safe_int(s) -> int | None:
  return E.safe(lambda: int(s)).get_or(None)

def parse_row(row: Row) -> Pairing:
  if row.black_no == '':
    return Unpaired(player=row.white, reason=row.black, tag='unpaired')
  else:
    return Paired(
      result=parse_result(row.result), white=row.white, black=row.black,
      white_no=safe_int(row.white_no), white_elo=safe_int(row.white_elo),
      black_no=safe_int(row.black_no), black_elo=safe_int(row.black_elo),
      tag='paired'
    )
  
def parse_rounds(soup: BeautifulSoup) -> Either[ParsingError, list[list[Pairing]]]:
  try:
    rounds: dict[int, list[Pairing]] = {}
    columns = parse_columns(soup).unsafe()
    headings = soup.find_all(string=re.compile("^Round ."))

    for h in headings:
      rnd = int(h.get_text(strip=True).split(" ")[1])
      table = h.find_next("table")
      pairs = extract_round(table, columns).map(parse_row).sync()
      if any(isinstance(p, Paired) for p in pairs):
        rounds[rnd] = pairs

    sorted_rounds = Iter(rounds.items()).sort(lambda kv: kv[0]).map(lambda kv: kv[1]).sync()
    return Right(sorted_rounds)

  except IsLeft as e:
    return Left(e.value)