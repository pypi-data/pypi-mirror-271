"""
glyphRepertoire
===============================================================================
"""
from __future__ import annotations

import os
import re
from datetime import date
from random import randint
from typing import TYPE_CHECKING, List, Sequence, Optional, Any

import unicodedata2
from fontTools.agl import AGL2UV
from glyphsLib.glyphdata import get_glyph

from .base import BaseReperoire

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont
    from fontTools.ttLib import TTFont
    from glyphsLib import GSFont

uni4name = re.compile(r"^uni[0-9A-F]{4}$")
uni5name = re.compile(r"^u[0-9A-F]{5}$")


def getCodepoint(glyphname: str, default: Any = None) -> Optional[int]:
    if uni4name.match(glyphname):
        return int(glyphname[3:], 16)
    if uni5name.match(glyphname):
        return int(glyphname[1:], 16)
    cp = AGL2UV.get(glyphname)
    if cp is not None:
        return cp
    glyph = get_glyph(glyphname)
    if glyph.unicode:
        return int(glyph.unicode, 16)
    return default


class GlyphRepertoire(BaseReperoire):
    """
    Class to represent a Glyph Repertoire as a set of glyph names (strings).
    """

    itemtype = str

    def __init__(self, iterable: Optional[Sequence[str]] = None, name: str = ""):
        if iterable:
            super().__init__(iterable)
        else:
            super().__init__()
        self._check_type_squence(self)
        self.name = name
        # self.glyphnames: List[str] = []
        self.comment = {}
        self.description: str = ""
        year = date.today().year
        self.version = f"Version 1.0 {year}"
        self.copyright = f"(c) {year}"

    def __repr__(self) -> str:
        return f"<GlyphRepertoire: {self.name}, {len(self)} glyphs>"

    @property
    def glyphnames(self) -> List[str]:
        return list(self)

    @staticmethod
    def _makeComment(glyphname: str):
        glyph = get_glyph(glyphname)
        if glyph.unicode:
            return f"(0x{glyph.unicode}) {glyph.description}"
        result = ""
        baseName, extension = glyphname, None
        if not glyphname.startswith(".") and "." in glyphname:
            baseName, extension = glyphname.split(".", 1)
        if extension:
            result = f"{extension} variant of "
        codepoint = getCodepoint(baseName)
        if codepoint is None and baseName != glyphname:
            result += baseName
        elif codepoint is not None:
            result += f"(0x{codepoint:04X}) "
            try:
                result += unicodedata2.name(chr(codepoint))
            except TypeError:
                pass
        return result

    @classmethod
    def fromTTFont(cls, font: TTFont) -> GlyphRepertoire:
        """
        Instantiate a Glyph Repertoire from a fontTools TTFont font object
        """
        try:
            return cls(font.glyphOrder)
        except AttributeError:
            return cls(font.getGlyphOrder())

    @classmethod
    def fromUFO(cls, ufo: BaseFont) -> GlyphRepertoire:
        """
        Instantiate a Glyph Repertoire from a UFO font object.
        """
        return cls(g.name for g in ufo)

    @classmethod
    def fromGSFont(cls, gsFont:GSFont) -> GlyphRepertoire:
        """
        Instantiate a Glyph Repertoire from a GSFont font object (Glyphs App file).
        """
        return cls(g.name for g in gsFont.glyphs)
    

    def save(self, outPath: str, newLine: str = "\n", auto_comment: bool = True):
        """
        Save the Glyph Repertoire as plain text file.
        """
        header = """
# Glyph Repertoire Definition
#
# Name: {c.name}
# Version: {c.version}
# Copyright: {c.copyright}

"""
        if not self.name:
            self.name = os.path.splitext(os.path.basename(outPath))[0]
        with open(outPath, "w", encoding="utf-8") as glyphRepertoireFile:
            glyphRepertoireFile.write(header.format(c=self))
            for glyphname in self.glyphnames:
                default = None
                if auto_comment:
                    default = self._makeComment(glyphname)
                comment = self.comment.get(glyphname, default)
                if comment:
                    glyphRepertoireFile.write(f"{glyphname} # {comment}{newLine}")
                else:
                    glyphRepertoireFile.write(f"{glyphname}{newLine}")

    def saveAsEncoding(
        self, outPath: str, newLine: str = "\n", auto_comment: bool = True
    ):
        """
        Save the Glyph Repertoire as FontLab Encoding file.
        """
        with open(outPath, "w", encoding="utf-8") as encodingFile:
            encodingFile.write(
                f"%%FONTLAB ENCODING: {randint(1000000, 10000000)}; {self.name}{newLine}"
            )
            for i, glyphname in enumerate(self.glyphnames):
                default = None
                if auto_comment:
                    default = self._makeComment(glyphname)
                comment = self.comment.get(glyphname, default)
                if comment:
                    encodingFile.write(f"{glyphname}\t{i}\t% {comment}{newLine}")
                else:
                    encodingFile.write(f"{glyphname}\t{i}{newLine}")

    def open(self, inPath: str) -> None:
        """
        Open a Glyph Repertoire from a plain text file.
        """
        # self.glyphnames = []
        if os.path.isfile(inPath):
            with open(inPath, "r", encoding="utf-8") as glyphRepertoireFile:
                for line in glyphRepertoireFile:
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
                            payload, comment = line, None
                            if "#" in line:
                                payload, comment = line.split("#", 1)
                            if payload:
                                payload = payload.strip()
                            if payload:
                                parts = payload.split(None, 1)
                                if parts:
                                    try:
                                        glyphname = parts[0]
                                        # if glyphname not in self.glyphnames:
                                        self.add(glyphname)
                                        if comment:
                                            self.comment[
                                                glyphname
                                            ] = comment.strip()
                                    except ValueError:
                                        pass
        if not self.name:
            self.name = os.path.splitext(os.path.basename(inPath))[0]
