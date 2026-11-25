import pytest

from lab import OffsetMap, Span


@pytest.mark.parametrize("text", ["ASCII", "ä🧾€", "e\u0301", "中文"])
def test_round_trip_at_every_boundary(text):
    mapping = OffsetMap(text)
    for i in range(len(text)):
        source = Span(i, i + 1, "X")
        for unit in ("utf8", "utf16"):
            converted = mapping.convert(source, "codepoint", unit)
            assert mapping.extract(converted, unit) == text[i]
            assert mapping.convert(converted, unit, "codepoint") == source


@pytest.mark.parametrize("unit", ["utf8", "utf16"])
def test_mid_character_offset_is_rejected(unit):
    with pytest.raises(ValueError, match="boundary"):
        OffsetMap("🧾").convert(Span(0, 1, "X"), unit, "codepoint")


@pytest.mark.parametrize("span", [Span(0, 0, "X"), Span(1, 0, "X"), Span(-1, 1, "X")])
def test_invalid_ranges(span):
    with pytest.raises(ValueError):
        OffsetMap("X").extract(span, "utf16")
