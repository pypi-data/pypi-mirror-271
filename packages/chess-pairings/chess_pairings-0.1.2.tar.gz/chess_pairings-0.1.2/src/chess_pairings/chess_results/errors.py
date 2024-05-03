from typing import Literal, TypeAlias
from dataclasses import dataclass

@dataclass
class DownloadError:
  detail: str | None = None
  reason: Literal['download-error'] = 'download-error'

@dataclass
class ParsingError:
  detail: str | None = None
  reason: Literal['parsing-error'] = 'parsing-error'

ScrapingError: TypeAlias = DownloadError | ParsingError