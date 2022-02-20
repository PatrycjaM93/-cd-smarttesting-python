from dataclasses import dataclass

from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.domain.score import Score


@dataclass(frozen=True)
class ScoreCalculatedEvent:
    pesel: Pesel
    score: Score
