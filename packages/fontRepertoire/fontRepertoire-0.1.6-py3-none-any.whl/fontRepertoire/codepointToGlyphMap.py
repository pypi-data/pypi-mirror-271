"""
codepointToGlyphMap
===============================================================================
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, List, Mapping, MutableSet, Optional, Union

from .characterSet import CharSet, unicodename
from .glyphRepertoire import GlyphRepertoire

if TYPE_CHECKING:
    from defcon import Font as defconUFO
    from fontParts.base import BaseFont as fontPartsUFO
    from fontTools.ttLib import TTFont
    from fontTools.ttLib.tables._c_m_a_p import CmapSubtable, table__c_m_a_p
    from ufoLib2 import Font as ufoLib2UFO
    from glyphsLib import GSFont, GSGlyph

log = logging.getLogger(__name__)


class CodepointToGlyphMap(dict):
    """
    Class to represent a codepoint (integer) to glyph name (string) mapping.
    """

    def __init__(self, mapping: Optional[Mapping[int, str]] = None, name: str = ""):
        self.name: str = name
        self.version: str = ""
        self.copyright: str = ""
        if mapping:
            assert all(isinstance(k, int) for k in mapping.keys())
            assert all(isinstance(v, str) for v in mapping.values())
            super().__init__(mapping)
        else:
            super().__init__()

    def __repr__(self) -> str:
        return f"<CodepointToGlyphMap: {self.name}, {len(self)} chars>"

    def __setitem__(self, __key: int, __value: str) -> None:
        assert isinstance(__key, int)
        assert isinstance(__value, str)
        return super().__setitem__(__key, __value)

    def clear(self) -> None:
        self.name = ""
        self.version = ""
        self.copyright = ""
        return super().clear()

    def update(self, other: Mapping[int, str]) -> None:
        assert all(isinstance(k, int) for k in other.keys())
        assert all(isinstance(v, str) for v in other.values())
        super().update(other)

    @classmethod
    def fromFile(cls, path: str) -> CodepointToGlyphMap:
        """
        Instantiate a CodepointToGlyphMap from a plain text file.
        """
        result = cls()
        result.open(path)
        return result

    @classmethod
    def fromTTFont(cls, font: TTFont) -> CodepointToGlyphMap:
        """
        Instantiate a CodepointToGlyphMap from a fontTools TTFont font object.
        """
        return cls(font.getBestCmap())

    @classmethod
    def fromUFO(
        cls, ufo: Union[defconUFO, fontPartsUFO, ufoLib2UFO]
    ) -> CodepointToGlyphMap:
        """
        Instantiate a CodepointToGlyphMap from a UFO font object.
        """
        unicodedata = None
        if hasattr(ufo, "unicodeData"):
            # it's a defcon like UFO
            unicodedata = ufo.unicodeData
        elif hasattr(ufo, "naked"):
            # it's a fontParts like UFO
            naked_ufo:defconUFO = ufo.naked()
            if hasattr(naked_ufo, "unicodeData"):
                unicodedata = naked_ufo.unicodeData
        if unicodedata:
            return cls(unicodedata)
        log.warning("Can't get Unicode data from UFO: %r", ufo)
        return cls()

    @classmethod
    def fromGSFont(cls, gsFont:GSFont) -> CodepointToGlyphMap:
        """
        Instantiate a CodepointToGlyphMap from a GSFont font object (Glyphs App file).
        """
        unicodedata = {}
        glyph:GSGlyph
        for glyph in gsFont.glyphs:
            if not glyph.unicodes:
                continue
            for unicode in glyph.unicodes:
                codepoint = int(unicode, 16)
                if codepoint in unicodedata:
                    continue
                unicodedata[codepoint] = glyph.name
        if unicodedata:
            return cls(unicodedata)
        log.warning("Can't get Unicode data from GSFont: %r", gsFont)
        return cls()

    @property
    def codepoints(self) -> List[int]:
        """
        Ordered list of codepoints (int)
        """
        return list(sorted(self.keys()))

    @property
    def charSet(self) -> CharSet:
        """
        Codepoints of the CodepointToGlyphMap as CharSet
        """
        return CharSet(self.keys())

    @property
    def glyphRepertoire(self) -> GlyphRepertoire:
        """
        Glyph names  of the CodepointToGlyphMap as `GlyphRepertoire`
        """
        return GlyphRepertoire(self.values())

    def hasCodepoint(self, codepoint: int) -> bool:
        """
        :return: True if a mapping for the given codepoint exists, False otherwise.
        """
        return codepoint in self

    def hasCharacter(self, character: str) -> bool:
        """
        :return: True if a mapping for the given character exists, False otherwise.
        """
        return ord(character) in self

    def buildReversed(self) -> Dict[str, MutableSet[int]]:
        """
        Builds a reverse mapping dictionary.
        The values are sets of Unicode codepoints.
        """
        result = {}
        for codepoint, name in self.items():
            result.setdefault(name, set()).add(codepoint)
        return result

    def updateTTFont(self, font: TTFont) -> None:
        """
        Update the cmap table of the font with this codepoint to
        glyph name mapping.

        :param font: The font to work with
        """
        try:
            glyphOrder = font.glyphOrder
        except AttributeError:
            glyphOrder = font.getGlyphOrder()
        mapping = {k: v for k, v in self.items() if v in glyphOrder}
        mapping_lo = {k: v for k, v in mapping.items() if k <= 0xFFFF}
        need_mapping_hi = False
        mapping_hi = {k: v for k, v in mapping.items() if k > 0xFFFF}
        if mapping_hi:
            need_mapping_hi = True
            log.debug("mapping_hi: %r", mapping_hi)
        found_mapping_hi = False
        cmap: table__c_m_a_p = font["cmap"]
        cmapTable: CmapSubtable
        for cmapTable in (t for t in cmap.tables if t.isUnicode()):
            cmapTable.cmap.update(mapping_lo)
            if cmapTable.format == 12:
                cmapTable.cmap.update(mapping_hi)
                found_mapping_hi = True
        if need_mapping_hi and not found_mapping_hi:
            # does this realy cover all cases?
            new_tables = []
            new_table: CmapSubtable
            for cmapTable in (t for t in cmap.tables if t.format == 4):
                new_table = cmapTable.newSubtable(12)
                new_table.platformID = cmapTable.platformID
                new_table.language = cmapTable.language
                if cmapTable.platformID == 0 and cmapTable.platEncID == 3:
                    new_table.platEncID = 4
                elif cmapTable.platformID == 3 and cmapTable.platEncID == 1:
                    new_table.platEncID = 10
                new_table.cmap = dict(cmapTable.cmap)
                new_table.cmap.update(mapping_hi)
                new_tables.append(new_table)
            for new_table in new_tables:
                cmap.tables.append(new_table)

    def updateUFO(self, ufo: Union[defconUFO, fontPartsUFO, ufoLib2UFO]) -> None:
        reversedMap = self.buildReversed()
        for glyphName, codepoints in reversedMap.items():
            if glyphName in ufo:
                ufo[glyphName].unicodes = list(sorted(codepoints))

    def open(self, inpath) -> None:
        """
        Open a CodepointToGlyphMap from a plain text file.
        """
        self.clear()
        with open(inpath, "r", encoding="utf-8") as inFile:
            name_found = False
            version_found = False
            copyright_found = False
            for i, line in enumerate(inFile, 1):
                line = line.strip()
                if line:
                    if line.startswith("#"):
                        if not name_found:
                            marker = " Name: "
                            markerIndex = line.find(marker)
                            if markerIndex > -1:
                                self.name = line[markerIndex + len(marker) :].strip()
                                name_found = True
                                continue
                        if not version_found:
                            marker = " Version: "
                            markerIndex = line.find(marker)
                            if markerIndex > -1:
                                self.version = line[markerIndex + len(marker) :].strip()
                                version_found = True
                                continue
                        if not copyright_found:
                            marker = " Copyright: "
                            markerIndex = line.find(marker)
                            if markerIndex > -1:
                                self.copyright = line[
                                    markerIndex + len(marker) :
                                ].strip()
                                copyright_found = True
                                continue
                    else:
                        line = line.split("#", 1)[0].strip()
                        if not line:
                            continue
                        parts = line.split(None, 1)
                        if len(parts) != 2:
                            log.warning("found invalid data in line %d: %s", i, line)
                            continue
                        codePointStr, glyphName = parts
                        try:
                            codePoint = int(codePointStr, 16)
                        except ValueError:
                            log.warning(
                                "found invalid data in line %d: can't convert '%s' to integer",
                                i,
                                codePointStr,
                            )
                        if codePoint in self:
                            log.warning(
                                "found duplicate codepoint '%s' in line %d - ignored",
                                codePointStr,
                                i,
                            )
                            continue
                        self[codePoint] = glyphName

    def save(self, outPath: str, newLine: str = "\n") -> None:
        """
        Save CodepointToGlyphMap to a plain text file.
        """
        with open(outPath, "w", encoding="utf-8") as outFile:
            outFile.write(f"# Codepoint to Glyph Name Mapping{newLine}")
            outFile.write(f"#{newLine}")
            if self.name:
                outFile.write(f"#  Name: {self.name}{newLine}")
            if self.version:
                outFile.write(f"#  Version: {self.version}{newLine}")
            if self.copyright:
                outFile.write(f"#  Copyright: {self.copyright}{newLine}")
            outFile.write(f"{newLine}")
            for codepoint, glyphname in sorted(self.items()):
                outFile.write(
                    f"0x{codepoint:04X}\t{glyphname}\t# {unicodename(codepoint)}{newLine}"
                )


def test001():
    from fontTools.ttLib import TTFont

    font = TTFont(
        r"\\VSERVER1\Vendors\H und M\HM Slussen\00 Urdaten\2024.03.07 from Matilda\HMSlussen-v2.200\ttf\HMSlussenHeadlinePPT-ExtendedSemibold.ttf"
    )
    cmap = CodepointToGlyphMap.fromTTFont(font)
    cmap.save(
        r"\\VSERVER1\Vendors\H und M\HM Slussen\00 Urdaten\2024.03.07 from Matilda\HMSlussen-v2.200\ttf\HMSlussenHeadlinePPT-ExtendedSemibold.cmap.txt"
    )


if __name__ == "__main__":
    test001()
