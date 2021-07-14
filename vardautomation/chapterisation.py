"""Chapterisation module"""

__all__ = ['Language', 'Chapter', 'Chapters', 'OGMChapters', 'MatroskaXMLChapters',
           'FRENCH', 'ENGLISH', 'JAPANESE', 'UNDEFINED']

import os
import random
from abc import ABC, abstractmethod
from fractions import Fraction
from typing import List, NamedTuple, Optional, cast

from lxml import etree

from .colors import Colors


class Language(NamedTuple):
    """Language"""
    name: str
    ietf: str
    iso639: str


FRENCH = Language('French', 'fr', 'fre')
ENGLISH = Language('English', 'en', 'eng')
JAPANESE = Language('Japanese', 'jp', 'jpn')
UNDEFINED = Language('Undefined', 'und', 'und')


class Chapter(NamedTuple):
    """Chapter object"""
    name: str
    start_frame: int
    end_frame: Optional[int] = None
    lang: Language = UNDEFINED


class Chapters(ABC):
    """Abtract chapters interface"""
    chapter_file: str

    def __init__(self, chapter_file: str) -> None:
        """Chapter file path as parameter"""
        self.chapter_file = chapter_file
        super().__init__()

    @abstractmethod
    def create(self, chapters: List[Chapter], fps: Fraction) -> None:
        """Create a chapter"""

    @abstractmethod
    def set_names(self, names: List[Optional[str]]) -> None:
        """Change chapter names."""

    def copy(self, destination: str) -> None:
        """Copy source chapter to destination."""
        os.system(f'copy "{self.chapter_file}" "{destination}"')

    def _f2seconds(self, f: int, fps: Fraction, /) -> float:  # noqa
        if f == 0:
            s = 0.0  # noqa

        t = round(float(10 ** 9 * f * fps ** -1))  # noqa
        s = t / 10 ** 9  # noqa
        return s

    def _f2ts(self, f: int, fps: Fraction, /, *, precision: int = 3) -> str:  # noqa
        s = self._f2seconds(f, fps)  # noqa
        ts = self._seconds2ts(s, precision=precision)  # noqa
        return ts

    def _ts2seconds(self, ts: str, /) -> float:  # noqa
        h, m, s = map(float, ts.split(':'))  # noqa
        return h * 3600 + m * 60 + s

    def _seconds2ts(self, s: float, /, *, precision: int = 3) -> str:  # noqa
        m = s // 60  # noqa
        s %= 60  # noqa
        h = m // 60  # noqa
        m %= 60  # noqa

        return self._compose_ts(h, m, s, precision=precision)

    @staticmethod
    def _compose_ts(h: float, m: float, s: float, /, *, precision: int = 3) -> str:
        if precision == 0:  # noqa
            return f"{h:02.0f}:{m:02.0f}:{round(s):02}"
        elif precision == 3:
            return f"{h:02.0f}:{m:02.0f}:{s:06.3f}"
        elif precision == 6:
            return f"{h:02.0f}:{m:02.0f}:{s:09.6f}"
        elif precision == 9:
            return f"{h:02.0f}:{m:02.0f}:{s:012.9f}"
        else:
            raise ValueError('precision must be <= 9 and >= 0')


class OGMChapters(Chapters):
    """OGMChapters object"""

    def create(self, chapters: List[Chapter], fps: Fraction) -> None:
        """Create a txt chapter file."""

        with open(self.chapter_file, 'w') as file:
            for i, chapter in enumerate(chapters):
                file.writelines([f'CHAPTER{i:02.0f}={self._f2ts(chapter.start_frame, fps)}\n',
                                 f'CHAPTER{i:02.0f}NAME={chapter.name}\n'])
        print(Colors.INFO)
        print(f'Chapter file sucessfuly created at: {self.chapter_file}')
        print(f'{Colors.RESET}\n')

    def set_names(self, names: List[Optional[str]]) -> None:
        data = self._get_data()

        times = data[::2]
        old = data[1::2]

        if len(names) > len(old):
            raise ValueError('set_names: too many names!')
        if len(names) < len(old):
            names += [None] * (len(old) - len(names))

        new = [f'CHAPTER{i+1:02.0f}NAME={names[i]}\n' if names[i] is not None else chapname
               for i, chapname in enumerate(old)]

        with open(self.chapter_file, 'w') as file:
            file.writelines([val for tup in zip(times, new) for val in tup])

        print(Colors.INFO)
        print(f'Chapter names sucessfuly updated at: {self.chapter_file}')
        print(f'{Colors.RESET}\n')

    def shift_times(self, frames: int, fps: Fraction) -> None:
        """Shift times by given number of frames."""
        data = self._get_data()

        shifttime = self._f2seconds(frames, fps)

        chaptimes = data[::2]
        chapnames = data[1::2]

        newchaptimes = [
            f'{chaptime.split("=")[0]}={self._seconds2ts(max(0, self._ts2seconds(chaptime.split("=")[1]) + shifttime))}\n'
            for chaptime in chaptimes
        ]

        with open(self.chapter_file, 'w') as file:
            file.writelines([val for tup in zip(newchaptimes, chapnames) for val in tup])

        print(Colors.INFO)
        print(f'Chapter names sucessfuly shifted at: {self.chapter_file}')
        print(f'{Colors.RESET}\n')

    def _get_data(self) -> List[str]:
        with open(self.chapter_file, 'r') as file:
            data = file.readlines()
        return data


class MatroskaXMLChapters(Chapters):
    """MatroskaXMLChapters object """
    fps: Fraction
    timecodes: List[float]

    ed_entry = 'EditionEntry'
    ed_uid = 'EditionUID'

    chap_atom = 'ChapterAtom'
    chap_start = 'ChapterTimeStart'
    chap_end = 'ChapterTimeEnd'
    chap_uid = 'ChapterUID'
    chap_disp = 'ChapterDisplay'
    chap_name = 'ChapterString'
    chap_ietf = 'ChapLanguageIETF'
    chap_iso639 = 'ChapterLanguage'

    doctype = '<!DOCTYPE Tags SYSTEM "matroskatags.dtd">'

    def create(self, chapters: List[Chapter], fps: Fraction) -> None:
        """Create a xml chapter file."""
        self.fps = fps

        root = etree.Element('Chapters')

        edit_entry = etree.SubElement(root, self.ed_entry)
        etree.SubElement(edit_entry, self.ed_uid).text = str(random.getrandbits(64))

        # Append chapters
        for chap in [self._make_chapter_xml(c) for c in chapters]:
            root.append(chap)

        with open(self.chapter_file, 'wb') as file:
            file.write(etree.tostring(
                root, 'utf-8', xml_declaration=True, pretty_print=True, doctype=self.doctype)
            )

        print(Colors.INFO)
        print(f'Chapter file sucessfuly created at: {self.chapter_file}')
        print(f'{Colors.RESET}\n')

    def set_names(self, names: List[Optional[str]]) -> None:
        tree = self._get_tree()

        olds = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_disp}/{self.chap_name}')
        olds = cast(List[etree._Element], olds)

        if len(names) > len(olds):
            raise ValueError('set_names: too many names!')
        if len(names) < len(olds):
            names += [None] * (len(olds) - len(names))

        for new, old in zip(names, olds):
            old.text = new

        with open(self.chapter_file, 'wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, with_comments=True)

        print(Colors.INFO)
        print(f'Chapter names sucessfuly updated at: {self.chapter_file}')
        print(f'{Colors.RESET}\n')


    def shift_times(self, frames: int, fps: Fraction) -> None:
        """Shift times by given number of frames."""
        shifttime = self._f2seconds(frames, fps)


        tree = self._get_tree()

        timestarts = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_start}')
        timestarts = cast(List[etree._Element], timestarts)

        timeends = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_end}')
        timeends = cast(List[etree._Element], timeends)

        for t_s in timestarts:
            if isinstance(t_s.text, str):
                t_s.text = self._seconds2ts(max(0, self._ts2seconds(t_s.text) + shifttime), precision=9)

        for t_e in timeends:
            if isinstance(t_e.text, str) and t_e.text != '':
                t_e.text = self._seconds2ts(max(0, self._ts2seconds(t_e.text) + shifttime), precision=9)



        with open(self.chapter_file, 'wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, with_comments=True)

        print(Colors.INFO)
        print(f'Chapter names sucessfuly shifted at: {self.chapter_file}')
        print(f'{Colors.RESET}\n')


    def _make_chapter_xml(self, chapter: Chapter) -> etree._Element:

        atom = etree.Element(self.chap_atom)


        etree.SubElement(atom, self.chap_start).text = self._f2ts(chapter.start_frame, self.fps, precision=9)
        if chapter.end_frame:
            etree.SubElement(atom, self.chap_end).text = self._f2ts(chapter.end_frame, self.fps, precision=9)

        etree.SubElement(atom, self.chap_uid).text = str(random.getrandbits(64))


        disp = etree.SubElement(atom, self.chap_disp)
        etree.SubElement(disp, self.chap_name).text = chapter.name
        etree.SubElement(disp, self.chap_ietf).text = chapter.lang.ietf
        etree.SubElement(disp, self.chap_iso639).text = chapter.lang.iso639


        return atom


    def _get_tree(self) -> etree._ElementTree:
        return etree.parse(self.chapter_file)
