"""
characterSet
===============================================================================
"""

from __future__ import annotations

import logging
import os
from datetime import date
from typing import List, TYPE_CHECKING, Union
import unicodedata2
from fontTools.agl import UV2AGL
from fontTools.ttLib import TTFont
from fontTools.unicodedata import block

from .base import BaseReperoire

if TYPE_CHECKING:
    from pathlib import Path

log = logging.getLogger(__name__)


def unicodename(codepoint: int) -> str:
    try:
        value = int(codepoint)
    except ValueError:
        return ""
    if value < 32:
        return "<Control>"
    try:
        return unicodedata2.name(chr(value))
    except ValueError:
        return ""


def glyphname(codepoint: int) -> str:
    name = UV2AGL.get(codepoint)
    if name and name[:2] not in ("SF", "H1", "H2"):  # don't use the boxdrawings names
        return name
    if codepoint > 0xFFFF:
        return f"u{codepoint:05X}"
    return f"uni{codepoint:04X}"


class CharSet(BaseReperoire):
    """
    Class to represent a Character Set as a set of codepoints (integers)
    """

    itemtype = int

    def __init__(self, iterable=None, name=""):
        if iterable:
            super().__init__(iterable)
        else:
            super().__init__()
        self._check_type_squence(self)
        self.name: str = name
        self.description: str = ""
        year = date.today().year
        self.version = f"Version 1.0 {year}"
        self.copyright = f"(c) {year}"

    def __repr__(self) -> str:
        return f"<CharSet: {self.name}, {len(self)} chars>"

    def hasCodepoint(self, codepoint: int) -> bool:
        return codepoint in self

    def hasCharacter(self, character: str) -> bool:
        return ord(character) in self
    
    def open(self, path: Union[str, Path]) -> None:
        """
        Open a Character Set from a plain text file.
        """
        codepoints = set()
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as charsetFile:
                for line in charsetFile:
                    line = line.strip()
                    if line:
                        if line.startswith("#"):
                            marker = " Name: "
                            markerIndex = line.find(marker)
                            if markerIndex > -1:
                                self.name = line[markerIndex + len(marker) :].strip()
                                continue
                            marker = " Version: "
                            markerIndex = line.find(marker)
                            if markerIndex > -1:
                                self.version = line[markerIndex + len(marker) :].strip()
                                continue
                            marker = " Copyright: "
                            markerIndex = line.find(marker)
                            if markerIndex > -1:
                                self.copyright = line[
                                    markerIndex + len(marker) :
                                ].strip()
                                continue
                        else:
                            parts = line.split(None, 1)
                            if parts:
                                try:
                                    codepoints.add(int(parts[0], 16))
                                except ValueError:
                                    pass
        self.codepoints = codepoints
        if not self.name:
            self.name = os.path.splitext(os.path.basename(path))[0]

    def toString(self, newLine: str = "\n") -> str:
        result = ""
        header = """
# Character Set Definition
#
# Name: {c.name}
# Version: {c.version}
# Copyright: {c.copyright}
# Description: {c.description}

"""
        result += header.format(c=self)
        currentBlock: str = ""
        for codepoint in sorted(self):
            _block = block(chr(codepoint))
            if _block != currentBlock:
                result += f"{newLine}# {_block}{newLine}"
                currentBlock = _block
            result += f"0x{codepoint:04X}\t# {unicodename(codepoint)}{newLine}"
        return result

    def save(self, outPath: str, newLine: str = "\n") -> None:
        """
        Save the Character Set as plain text file.
        """
        with open(outPath, "w", encoding="utf-8") as charsetFile:
            charsetFile.write(self.toString(newLine))

    @property
    def codepoints(self) -> List[int]:
        """
        Ordered list of codepoints (int)
        """
        return list(sorted(self))

    @codepoints.setter
    def codepoints(self, values):
        _values = set(values)
        self.clear()
        self.update(_values)

    @property
    def as_set(self) -> set:
        return set(self)

    @classmethod
    def fromString(cls, string: str) -> CharSet:
        """
        Instantiate a Character Set from a string.
        """
        return cls(ord(c) for c in string)

    @classmethod
    def fromTTFont(cls, font: TTFont) -> CharSet:
        """
        Instantiate a Character Set from a fontTools TTFont font object.
        """
        cmap = font.getBestCmap()
        return cls(cmap.keys())

    @classmethod
    def fromUFO(cls, ufo) -> CharSet:
        """
        Instantiate a Character Set from a UFO font object.
        """
        unicodedata = None
        if hasattr(ufo, "unicodeData"):
            # it's a defcon like UFO
            unicodedata = ufo.unicodeData
        elif hasattr(ufo, "naked"):
            # it's a fontParts like UFO
            naked_ufo = ufo.naked()
            if hasattr(naked_ufo, "unicodeData"):
                unicodedata = naked_ufo.unicodeData
        if unicodedata:
            return cls(unicodedata.keys())
        else:
            log.warning("Can't get Unicode data from UFO: %r", ufo)
        return cls()

    @classmethod
    def fromGSFont(cls, gsFont) -> CharSet:
        """
        Instantiate a Character Set from a GSFont font object (Glyphs App file).
        """
        return cls(
            set(int(g.unicode, 16) for g in gsFont.glyphs if g.unicode is not None)
        )


class __CharSet:
    """
    Class to represent a Character Set
    """

    def __init__(self, name=""):
        self.name: str = name
        self.codepoints: List[int] = []
        self.description: str = ""
        year = date.today().year
        self.version = f"Version 1.0 {year}"
        self.copyright = f"(c) {year}"

    def saveAsEncoding(self, outPath: str, newLine: str = "\n") -> None:
        with open(outPath, "w", encoding="utf-8") as charsetFile:
            charsetFile.write(
                r"%%%%FONTLAB ENCODING: 285613; %s%s" % (self.name, newLine)
            )
            for codepoint in sorted(self.codepoints):
                charsetFile.write(
                    "%s \t# 0x%04X %s%s"
                    % (glyphname(codepoint), codepoint, unicodename(codepoint), newLine)
                )


def __test001():
    charset = CharSet()
    print(charset)
    print((ord(c) for c in "abc"))
    print(list(ord(c) for c in "abc"))
    charset.codepoints = (ord(c) for c in "abc")
    print(charset)
    print(charset.codepoints)


if __name__ == "__main__":
    __test001()
