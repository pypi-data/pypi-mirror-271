from aiohttp import ClientSession
from bs4 import BeautifulSoup
from haskellian import Either, Left, Right, either as E
from .errors import DownloadError

DB_KEY = 741703
def slug(db_key: int) -> str:
    return f"/tnr{db_key}.aspx"

CHESS_RESULTS = "https://chess-results.com/"
BLOCKED_MESSAGE = "Note: To reduce the server load by daily scanning of all links (daily 100.000 sites and more) by search engines like Google, Yahoo and Co, all links for tournaments older than 5 days (end-date) are shown after clicking the following button:"

async def download(
  slug: str, params: dict = {}, *,
  base = CHESS_RESULTS,
  blocked_message = BLOCKED_MESSAGE
) -> Either[DownloadError, BeautifulSoup]:
  """Download any chess-results page bypassing the anti-indexing block"""
  async with ClientSession(base) as ses:
    r = await ses.get(slug, params=params)
    page = await r.content.read()
    soup = BeautifulSoup(page, 'html.parser')
    if soup.find(string=blocked_message) is None:
      return Right(soup)
    else:
      input_tag = soup.find(id="__VIEWSTATE")
      if input_tag is None:
        return Left(DownloadError('VIEWSTATE not found'))
      viewstate = E.safe(lambda: input_tag['value']).get_or(None) # type: ignore
      if viewstate is None:
        return Left(DownloadError('VIEWSTATE found but does not have "value" attribute'))
      r2 = await ses.post(slug, params=params, data={
        "__VIEWSTATE": viewstate,
        "cb_alleDetails": "Show+tournament+details"
      })
      page2 = await r2.content.read()
      return Right(BeautifulSoup(page2, 'html.parser'))
    
async def download_main(db_key: int):
    """Main page of a tournament. Bypasses anti-indexing block"""
    url = slug(db_key)
    params = dict(lan=1)
    return await download(url, params)

async def download_round_pairings(db_key: int, round: int):
    """Pairings page. Bypasses anti-indexing block"""
    params = dict(lan=1, rd=round, art=2, turdet="YES")
    url = slug(db_key)
    return await download(url, params)

async def download_pairings(db_key: int):
    params = dict(lan=1, rd=0, art=2, turdet="YES", zeilen=99999)
    url = slug(db_key)
    return await download(url, params)

async def download_schedule(db_key: int):
    params = dict(lan=1, art=14, turdet="YES")
    url = slug(db_key)
    return await download(url, params)