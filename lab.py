"""Translate half-open annotation spans without changing the underlying text."""

from bisect import bisect_left
from dataclasses import dataclass
from typing import Literal

Unit = Literal["codepoint", "utf8", "utf16"]


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    label: str


class OffsetMap:
    """Index Unicode scalar boundaries once; each reverse lookup is logarithmic."""

    def __init__(self, text: str):
        self.text = text
        self.boundaries = {"codepoint": tuple(range(len(text) + 1))}
        u8, u16 = [0], [0]
        for char in text:
            u8.append(u8[-1] + len(char.encode("utf-8")))
            u16.append(u16[-1] + (2 if ord(char) > 0xFFFF else 1))
        self.boundaries.update(utf8=tuple(u8), utf16=tuple(u16))

    def _index(self, value: int, unit: Unit) -> int:
        points = self.boundaries[unit]
        if type(value) is not int:
            raise ValueError("offset must be an integer")
        index = bisect_left(points, value)
        if index == len(points) or points[index] != value:
            raise ValueError(f"{value} is not a {unit} character boundary")
        return index

    def convert(self, span: Span, source: Unit, target: Unit) -> Span:
        start, end = self._index(span.start, source), self._index(span.end, source)
        if end <= start:
            raise ValueError("expected a nonempty, ordered span")
        points = self.boundaries[target]
        return Span(points[start], points[end], span.label)

    def extract(self, span: Span, unit: Unit) -> str:
        mapped = self.convert(span, unit, "codepoint")
        return self.text[mapped.start : mapped.end]


if __name__ == "__main__":
    mapping = OffsetMap("🧾 Café €42")
    span = Span(7, 10, "TOTAL")
    for unit in ("codepoint", "utf8", "utf16"):
        mapped = mapping.convert(span, "codepoint", unit)
        print(unit, mapped, mapping.extract(mapped, unit))
