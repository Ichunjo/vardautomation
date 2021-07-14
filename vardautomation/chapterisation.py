"""Chapterisation module"""

__all__ = ['Language', 'Chapter', 'Chapters', 'OGMChapters', 'MatroskaXMLChapters',
           'create_qpfile',
           'FRENCH', 'ENGLISH', 'JAPANESE', 'UNDEFINED']

import os
import random
from abc import ABC, abstractmethod
from fractions import Fraction
from typing import List, NamedTuple, NoReturn, Optional, Sequence, Set, cast

from langcodes import Language as L
from lxml import etree
from prettyprinter import doc, pretty_call, pretty_repr, register_pretty
from prettyprinter.prettyprinter import PrettyContext

from .colors import Colors
from .timeconv import Convert


class Language:
    """Language"""
    name: str
    ietf: str
    iso639: str

    def __init__(self, lang: L) -> None:
        self.name = lang.autonym()
        self.ietf = str(lang)
        self.iso639 = lang.to_alpha3(variant='B')

    def __repr__(self) -> str:
        @register_pretty(Language)
        def _repr(value: object, ctx: PrettyContext) -> doc.Doc:
            dic = vars(value)
            return pretty_call(ctx, Language, dic)

        return pretty_repr(self)


FRENCH = Language(L.make('fr'))
ENGLISH = Language(L.make('en'))
JAPANESE = Language(L.make('ja'))
UNDEFINED = Language(L.make())



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

    def __repr__(self) -> str:
        @register_pretty(Chapters)
        def _repr(value: object, ctx: PrettyContext) -> doc.Doc:
            dic = vars(value)
            return pretty_call(ctx, Chapters, dic)

        return pretty_repr(self)

    @abstractmethod
    def create(self, chapters: List[Chapter], fps: Fraction) -> None:
        """Create a chapter"""

    @abstractmethod
    def set_names(self, names: List[Optional[str]]) -> None:
        """Change chapter names."""

    def copy(self, destination: str) -> None:
        """Copy source chapter to destination."""
        os.system(f'copy "{self.chapter_file}" "{destination}"')

    def _logging(self, action: str) -> None:
        print(f'{Colors.INFO}Chapter file sucessfully {action} at: {self.chapter_file}{Colors.RESET}\n')


class OGMChapters(Chapters):
    """OGMChapters object"""

    def create(self, chapters: List[Chapter], fps: Fraction) -> None:
        """Create a txt chapter file."""

        with open(self.chapter_file, 'w') as file:
            for i, chapter in enumerate(chapters):
                file.writelines([f'CHAPTER{i:02.0f}={Convert.f2ts(chapter.start_frame, fps)}\n',
                                 f'CHAPTER{i:02.0f}NAME={chapter.name}\n'])
        self._logging('created')

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

        self._logging('updated')

    def shift_times(self, frames: int, fps: Fraction) -> None:
        """Shift times by given number of frames."""
        data = self._get_data()

        shifttime = Convert.f2seconds(frames, fps)

        chaptimes = data[::2]
        chapnames = data[1::2]

        newchaptimes = [
            f'{chaptime.split("=")[0]}={Convert.seconds2ts(max(0, Convert.ts2seconds(chaptime.split("=")[1]) + shifttime))}\n'
            for chaptime in chaptimes
        ]

        with open(self.chapter_file, 'w') as file:
            file.writelines([val for tup in zip(newchaptimes, chapnames) for val in tup])

        self._logging('shifted')

    def ogm_to_chapters(self, fps: Fraction, lang: Language = UNDEFINED) -> List[Chapter]:
        """Convert OGM Chapters to a list of Chapter"""
        data = self._get_data()

        chaptimes = data[::2]
        chapnames = data[1::2]

        chapters = [
            Chapter(chapname.split('=')[1], Convert.ts2f(chaptime.split('=')[1], fps), lang=lang)
            for chaptime, chapname in zip(chaptimes, chapnames)
        ]

        return chapters

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

    doctype = '<!-- <!DOCTYPE Tags SYSTEM "matroskatags.dtd"> -->'

    def create(self, chapters: List[Chapter], fps: Fraction) -> None:
        """Create a xml chapter file."""
        self.fps = fps

        root = etree.Element('Chapters')

        edit_entry = etree.SubElement(root, self.ed_entry)
        etree.SubElement(edit_entry, self.ed_uid).text = str(random.getrandbits(64))

        # Append chapters
        for chap in [self._make_chapter_xml(c) for c in chapters]:
            edit_entry.append(chap)

        with open(self.chapter_file, 'wb') as file:
            file.write(etree.tostring(
                root, encoding='utf-8', xml_declaration=True,
                pretty_print=True, doctype=self.doctype)
            )

        self._logging('created')

    def set_names(self, names: List[Optional[str]]) -> None:
        tree = self._get_tree()

        olds = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_disp}/{self.chap_name}')
        olds = cast(List[etree._Element], olds)  # noqa: PLW0212

        if len(names) > len(olds):
            raise ValueError('set_names: too many names!')
        if len(names) < len(olds):
            names += [None] * (len(olds) - len(names))

        for new, old in zip(names, olds):
            old.text = new

        with open(self.chapter_file, 'wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, with_comments=True)

        self._logging('updated')

    def shift_times(self, frames: int, fps: Fraction) -> None:
        """Shift times by given number of frames."""
        tree = self._get_tree()

        shifttime = Convert.f2seconds(frames, fps)


        timestarts = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_start}')
        timestarts = cast(List[etree._Element], timestarts)  # noqa: PLW0212

        timeends = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_end}')
        timeends = cast(List[etree._Element], timeends)  # noqa: PLW0212

        for t_s in timestarts:
            if isinstance(t_s.text, str):
                t_s.text = Convert.seconds2ts(max(0, Convert.ts2seconds(t_s.text) + shifttime), precision=9)

        for t_e in timeends:
            if isinstance(t_e.text, str) and t_e.text != '':
                t_e.text = Convert.seconds2ts(max(0, Convert.ts2seconds(t_e.text) + shifttime), precision=9)


        with open(self.chapter_file, 'wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, with_comments=True)

        self._logging('shifted')

    def xml_to_chapters(self, fps: Fraction, lang: Optional[Language] = None) -> List[Chapter]:
        """Convert XML Chapters to a list of Chapter"""
        tree = self._get_tree()

        timestarts = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_start}')
        timestarts = cast(List[etree._Element], timestarts)  # noqa: PLW0212


        timeends = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_end}')
        timeends = cast(List[Optional[etree._Element]], timeends)  # noqa: PLW0212
        if len(timeends) != len(timestarts):
            timeends += [None] * (len(timestarts) - len(timeends))


        names = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_disp}/{self.chap_name}')
        names = cast(List[Optional[etree._Element]], names)  # noqa: PLW0212
        if len(names) != len(timestarts):
            names += [None] * (len(timestarts) - len(names))


        ietfs = tree.xpath(f'/Chapters/{self.ed_entry}/{self.chap_atom}/{self.chap_disp}/{self.chap_ietf}')
        ietfs = cast(List[Optional[etree._Element]], ietfs)  # noqa: PLW0212
        if len(ietfs) != len(timestarts):
            ietfs += [None] * (len(timestarts) - len(ietfs))


        chapters: List[Chapter] = []
        for name, timestart, timeend, ietf in zip(names, timestarts, timeends, ietfs):

            name = name.text if isinstance(name.text, str) else ''

            if isinstance(timestart.text, str):
                start_frame = Convert.ts2f(timestart.text, fps)
            else:
                raise ValueError()

            try:
                end_frame = Convert.ts2f(timeend.text, fps)  # type: ignore
            except AttributeError:
                end_frame = None

            if not lang and isinstance(ietf.text, str):
                lang = Language(L.make(ietf.text))
            else:
                assert lang

            chapter = Chapter(name=name, start_frame=start_frame, end_frame=end_frame, lang=lang)
            chapters.append(chapter)

        return chapters


    def _make_chapter_xml(self, chapter: Chapter) -> etree._Element:  # noqa: PLW0212

        atom = etree.Element(self.chap_atom)


        etree.SubElement(atom, self.chap_start).text = Convert.f2ts(chapter.start_frame, self.fps, precision=9)
        if chapter.end_frame:
            etree.SubElement(atom, self.chap_end).text = Convert.f2ts(chapter.end_frame, self.fps, precision=9)

        etree.SubElement(atom, self.chap_uid).text = str(random.getrandbits(64))


        disp = etree.SubElement(atom, self.chap_disp)
        etree.SubElement(disp, self.chap_name).text = chapter.name
        etree.SubElement(disp, self.chap_ietf).text = chapter.lang.ietf
        etree.SubElement(disp, self.chap_iso639).text = chapter.lang.iso639


        return atom


    def _get_tree(self) -> etree._ElementTree:  # noqa: PLW0212
        return etree.parse(self.chapter_file)


def create_qpfile(qpfile: str,
                  frames: Optional[Sequence[int]] = None, *,
                  chapters: Optional[List[Chapter]] = None) -> None:
    """Create a qp file from a list of Chapter or frames"""
    keyf: Set[int] = set()
    if chapters:
        for chap in chapters:
            keyf.add(chap.start_frame)
    elif frames:
        keyf = set(frames)

    with open(qpfile, "w", encoding='utf-8') as qp:  # noqa: PLC0103
        qp.writelines([f"{f} K\n" for f in sorted(keyf)])
