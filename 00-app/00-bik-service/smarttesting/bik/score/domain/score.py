from dataclasses import dataclass
from functools import cache


@dataclass
class Score:
    _points: int

    @classmethod
    @cache
    def zero(cls) -> "Score":
        return Score(0)

    @property
    def points(self) -> int:
        return self._points

    def __add__(self, other: "Score") -> "Score":
        return Score(self._points + other._points)

    def __str__(self) -> str:
        return f"<Score (points={self._points})>"

    __repr__ = __str__
