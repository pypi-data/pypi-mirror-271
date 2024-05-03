import string
import pytest
from fontRepertoire.characterSet import CharSet


def test_codepoints_TypeError1():
    with pytest.raises(TypeError) as e_info:
         CharSet("abc")


def test_codepoints_TypeError2():
    with pytest.raises(TypeError):
        CharSet(["a", "b"])


def test_charset_repr():
    charset = CharSet.fromString("abc")
    assert repr(charset) == "<CharSet: , 3 chars>"


def test_charset_contains():
    charset = CharSet.fromString("abc")
    assert ord("a") in charset
    assert ord("x") not in charset


def test_charset_len():
    charset = CharSet.fromString("abc")
    assert len(charset) == 3


def test_charset_hasCodepoint():
    charset = CharSet.fromString("abc")
    assert charset.hasCodepoint(ord("a"))


def test_charset_hasCharacter():
    charset = CharSet.fromString("abc")
    assert charset.hasCharacter("a")


def test_subset():
    charset = CharSet.fromString("abc")
    ascii_lower = CharSet.fromString(string.ascii_lowercase)
    assert charset.issubset(ascii_lower)
    assert charset <= ascii_lower


def test_superset():
    charset = CharSet.fromString("abc")
    ascii_lower = CharSet.fromString(string.ascii_lowercase)
    assert ascii_lower.issuperset(charset)
    assert ascii_lower >= charset


def test_and():
    abc = CharSet.fromString("abc")
    bcd = CharSet.fromString("bcd")
    bc = CharSet.fromString("bc")
    abc_bcd = abc & bcd
    assert isinstance(abc_bcd, CharSet)
    assert abc_bcd == bc


def test_or():
    abc = CharSet.fromString("abc")
    xyz = CharSet.fromString("xyz")
    abc_xyz = abc | xyz
    assert isinstance(abc_xyz, CharSet)
    assert abc_xyz == abc | xyz
    assert abc_xyz == abc | set(ord(c) for c in "xyz")
    with pytest.raises(TypeError):
        abc | set(c for c in "xyz")


def test_sub():
    abc = CharSet.fromString("abc")
    bcd = CharSet.fromString("bcd")
    abc_bcd = abc - bcd
    assert isinstance(abc_bcd, CharSet)
    assert abc_bcd == CharSet.fromString("a")


def test_update_1():
    charset = CharSet.fromString("abc")
    charset |= set(ord(c) for c in "xyz")
    assert isinstance(charset, CharSet)
    assert charset == set(ord(c) for c in "abc") | set(ord(c) for c in "xyz")
    with pytest.raises(TypeError):
        charset |= set(c for c in "xyz")


def test_update_2():
    charset = CharSet.fromString("abc")
    charset.update(ord(c) for c in "xyz")
    assert isinstance(charset, CharSet)
    assert charset == set(ord(c) for c in "abc") | set(ord(c) for c in "xyz")
    with pytest.raises(TypeError):
        charset |= set(c for c in "xyz")
