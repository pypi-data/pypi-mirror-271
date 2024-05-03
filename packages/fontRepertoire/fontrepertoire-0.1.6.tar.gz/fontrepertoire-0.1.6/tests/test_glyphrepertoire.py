import string
import pytest
from fontRepertoire.glyphRepertoire import GlyphRepertoire


def test_glyphrepertoire_TypeError1():
    with pytest.raises(TypeError) as e_info:
        GlyphRepertoire((1, 2, 3))


def test_charset_contains():
    glyphrepertoire = GlyphRepertoire(c for c in "abc")
    assert "a" in glyphrepertoire
    assert "x" not in glyphrepertoire


def test_charset_len():
    glyphrepertoire = GlyphRepertoire(c for c in "abc")
    assert len(glyphrepertoire) == 3


def test_subset():
    glyphrepertoire = GlyphRepertoire(c for c in "abc")
    ascii_lower = GlyphRepertoire(c for c in string.ascii_lowercase)
    assert glyphrepertoire.issubset(ascii_lower)
    assert glyphrepertoire <= ascii_lower


def test_superset():
    glyphrepertoire = GlyphRepertoire(c for c in "abc")
    ascii_lower = GlyphRepertoire(c for c in string.ascii_lowercase)
    assert ascii_lower.issuperset(glyphrepertoire)
    assert ascii_lower >= glyphrepertoire
