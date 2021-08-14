"""Chapterisation module"""

__all__ = ['Chapter', 'Chapters', 'OGMChapters', 'MatroskaXMLChapters',
           'MplsChapters', 'MplsReader',
           'IfoChapters', 'IfoReader']

import os
import random
from abc import ABC, abstractmethod
from fractions import Fraction
from pprint import pformat
from shutil import copyfile
from typing import (List, NamedTuple, NoReturn, Optional, Sequence, Type,
                    Union, cast)

from lxml import etree
from pyparsebluray import mpls
from pyparsedvd import vts_ifo

from .language import UNDEFINED, Lang
from .status import Status
from .timeconv import Convert
from .types import AnyPath, Element, ElementTree
from .utils import recursive_dict
from .vpathlib import VPath


class Chapter(NamedTuple):
    """Chapter object"""
    name: str
    start_frame: int
    end_frame: Optional[int]
    lang: Lang = UNDEFINED


class Chapters(ABC):
    """Abtract chapters interface"""
    chapter_file: VPath

    def __init__(self, chapter_file: AnyPath) -> None:
        """Chapter file path as parameter"""
        self.chapter_file = VPath(chapter_file)
        super().__init__()

    def __str__(self) -> str:
        return pformat(recursive_dict(self), indent=1, width=200, sort_dicts=False)

    @abstractmethod
    def create(self, chapters: List[Chapter], fps: Fraction) -> Union[None, NoReturn]:
        """Create a chapter"""

    @abstractmethod
    def set_names(self, names: Sequence[Optional[str]]) -> Union[None, NoReturn]:
        """Change chapter names."""

    @abstractmethod
    def to_chapters(self, fps: Fraction, lang: Optional[Lang]) -> List[Chapter]:
        """Convert the Chapters object to a list of chapter"""

    def copy(self, destination: AnyPath) -> None:
        """Copy source chapter to destination and change target of chapter_file to the destination one."""
        destination = VPath(destination)
        copyfile(self.chapter_file.resolve(), destination.resolve())
        self.chapter_file = destination
        Status.info(
            f'{self.__class__.__name__}: Chapter file sucessfully copied from: '
            + f'"{self.chapter_file.resolve().to_str()}" to "{destination.resolve().to_str()}"'
        )

    def create_qpfile(self, qpfile: AnyPath, fps: Fraction) -> None:
        """Create a qp file from the current Chapters object"""
        qpfile = VPath(qpfile)

        keyf = [chap.start_frame for chap in self.to_chapters(fps, None)]

        qpfile.write_text('\n'.join(f"{f} K" for f in sorted(keyf)), encoding='utf-8')

        Status.info(f'{self.__class__.__name__}: Qpfile sucessfully created at: "{qpfile.resolve().to_str()}"')

    def _logging(self, action: str) -> None:
        Status.info(
            f'{self.__class__.__name__}: Chapter file sucessfully {action} at: '
            + f'"{self.chapter_file.resolve().to_str()}"'
        )


class OGMChapters(Chapters):
    """OGMChapters object"""

    def __init__(self, chapter_file: AnyPath) -> None:
        super().__init__(chapter_file)
        self.chapter_file = self.chapter_file.with_suffix('.txt')

    def create(self, chapters: List[Chapter], fps: Fraction) -> None:
        """Create a txt chapter file."""

        if not (par := self.chapter_file.parent).exists():
            par.mkdir(parents=True, exist_ok=True)

        with self.chapter_file.open('w') as file:
            for i, chapter in enumerate(chapters, start=1):
                file.writelines([f'CHAPTER{i:02.0f}={Convert.f2ts(chapter.start_frame, fps)}\n',
                                 f'CHAPTER{i:02.0f}NAME={chapter.name}\n'])
        self._logging('created')

    def set_names(self, names: Sequence[Optional[str]]) -> None:
        data = self._get_data()
        names = list(names)

        times = data[::2]
        old = data[1::2]

        if len(names) > len(old):
            Status.fail(f'{self.__class__.__name__}: too many names!', exception=ValueError)
        if len(names) < len(old):
            names += [None] * (len(old) - len(names))

        new = [f'CHAPTER{i+1:02.0f}NAME={names[i]}\n' if names[i] is not None else chapname
               for i, chapname in enumerate(old)]

        self.chapter_file.write_text('\n'.join([val for tup in zip(times, new) for val in tup]))

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

        self.chapter_file.write_text('\n'.join([val for tup in zip(newchaptimes, chapnames) for val in tup]))

        self._logging('shifted')

    def to_chapters(self, fps: Fraction, lang: Optional[Lang]) -> List[Chapter]:
        """Convert OGM Chapters to a list of Chapter"""
        data = self._get_data()

        chaptimes = data[::2]
        chapnames = data[1::2]

        chapters = [
            Chapter(
                name=chapname.split('=')[1],
                start_frame=Convert.ts2f(chaptime.split('=')[1], fps),
                end_frame=None,
                lang=lang if lang is not None else UNDEFINED
            )
            for chaptime, chapname in zip(chaptimes, chapnames)
        ]

        return chapters

    def _get_data(self) -> List[str]:
        with self.chapter_file.open('r') as file:
            data = file.readlines()
        return data



class MatroskaXMLChapters(Chapters):
    """MatroskaXMLChapters object """
    fps: Fraction

    __ED_ENTRY = 'EditionEntry'
    __ED_UID = 'EditionUID'

    __CHAP_ATOM = 'ChapterAtom'
    __CHAP_START = 'ChapterTimeStart'
    __CHAP_END = 'ChapterTimeEnd'
    __CHAP_UID = 'ChapterUID'
    __CHAP_DISP = 'ChapterDisplay'
    __CHAP_NAME = 'ChapterString'
    __CHAP_IETF = 'ChapLanguageIETF'
    __CHAP_ISO639 = 'ChapterLanguage'

    __DOCTYPE = '<!-- <!DOCTYPE Tags SYSTEM "matroskatags.dtd"> -->'

    def __init__(self, chapter_file: AnyPath) -> None:
        super().__init__(chapter_file)
        self.chapter_file = self.chapter_file.with_suffix('.xml')

    def create(self, chapters: List[Chapter], fps: Fraction) -> None:
        """Create a xml chapter file."""
        self.fps = fps

        root = etree.Element('Chapters')

        edit_entry = etree.SubElement(root, self.__ED_ENTRY)
        etree.SubElement(edit_entry, self.__ED_UID).text = str(random.getrandbits(64))

        # Append chapters
        for chap in [self._make_chapter_xml(c) for c in chapters]:
            edit_entry.append(chap)

        if not (par := self.chapter_file.parent).exists():
            par.mkdir(parents=True, exist_ok=True)

        self.chapter_file.write_bytes(
            etree.tostring(root, encoding='utf-8', xml_declaration=True,
                           pretty_print=True, doctype=self.__DOCTYPE)
        )

        self._logging('created')

    def set_names(self, names: Sequence[Optional[str]]) -> None:
        tree = self._get_tree()
        names = list(names)

        olds = tree.xpath(f'/Chapters/{self.__ED_ENTRY}/{self.__CHAP_ATOM}/{self.__CHAP_DISP}/{self.__CHAP_NAME}')

        if len(names) > len(olds):
            Status.fail(f'{self.__class__.__name__}: too many names!', exception=ValueError)
        if len(names) < len(olds):
            names += [None] * (len(olds) - len(names))

        for new, old in zip(names, olds):
            old.text = new

        with self.chapter_file.open('wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, with_comments=True)

        self._logging('updated')

    def shift_times(self, frames: int, fps: Fraction) -> None:
        """Shift times by given number of frames."""
        tree = self._get_tree()

        shifttime = Convert.f2seconds(frames, fps)


        timestarts = tree.xpath(f'/Chapters/{self.__ED_ENTRY}/{self.__CHAP_ATOM}/{self.__CHAP_START}')
        timeends = tree.xpath(f'/Chapters/{self.__ED_ENTRY}/{self.__CHAP_ATOM}/{self.__CHAP_END}')

        for t_s in timestarts:
            if isinstance(t_s.text, str):
                t_s.text = Convert.seconds2ts(max(0, Convert.ts2seconds(t_s.text) + shifttime), precision=9)

        for t_e in timeends:
            if isinstance(t_e.text, str) and t_e.text != '':
                t_e.text = Convert.seconds2ts(max(0, Convert.ts2seconds(t_e.text) + shifttime), precision=9)


        with self.chapter_file.open('wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, with_comments=True)

        self._logging('shifted')

    def to_chapters(self, fps: Fraction, lang: Optional[Lang] = None) -> List[Chapter]:
        """Convert XML Chapters to a list of Chapter"""
        tree = self._get_tree()

        timestarts = tree.xpath(f'/Chapters/{self.__ED_ENTRY}/{self.__CHAP_ATOM}/{self.__CHAP_START}')


        timeends: List[Optional[Element]] = []
        timeends += tree.xpath(f'/Chapters/{self.__ED_ENTRY}/{self.__CHAP_ATOM}/{self.__CHAP_END}')
        if len(timeends) != len(timestarts):
            timeends += [None] * (len(timestarts) - len(timeends))


        names: List[Optional[Element]] = []
        names += tree.xpath(f'/Chapters/{self.__ED_ENTRY}/{self.__CHAP_ATOM}/{self.__CHAP_DISP}/{self.__CHAP_NAME}')
        if len(names) != len(timestarts):
            names += [None] * (len(timestarts) - len(names))


        ietfs: List[Optional[Element]] = []
        ietfs += tree.xpath(f'/Chapters/{self.__ED_ENTRY}/{self.__CHAP_ATOM}/{self.__CHAP_DISP}/{self.__CHAP_IETF}')
        if len(ietfs) != len(timestarts):
            ietfs += [None] * (len(timestarts) - len(ietfs))


        chapters: List[Chapter] = []
        for name, timestart, timeend, ietf in zip(names, timestarts, timeends, ietfs):

            if name is not None and isinstance(name.text, str):
                nametxt = name.text
            else:
                nametxt = ''

            if isinstance(timestart.text, str):
                start_frame = Convert.ts2f(timestart.text, fps)
            else:
                Status.fail(
                    f'{self.__class__.__name__}: timestart.text is not a str, wtf are u doin',
                    exception=ValueError
                )

            end_frame: Optional[int] = None
            try:
                end_frame = Convert.ts2f(timeend.text, fps)  # type: ignore
            except AttributeError:
                pass


            if lang is None:
                if ietf is not None and isinstance(ietf.text, str):
                    lng = Lang.make(ietf.text)
                else:
                    lng = UNDEFINED
            else:
                lng = lang


            chapter = Chapter(name=nametxt, start_frame=start_frame, end_frame=end_frame, lang=lng)
            chapters.append(chapter)

        return chapters

    def _make_chapter_xml(self, chapter: Chapter) -> Element:

        atom = etree.Element(self.__CHAP_ATOM)

        etree.SubElement(atom, self.__CHAP_START).text = Convert.f2ts(chapter.start_frame, self.fps, precision=9)
        if chapter.end_frame:
            etree.SubElement(atom, self.__CHAP_END).text = Convert.f2ts(chapter.end_frame, self.fps, precision=9)

        etree.SubElement(atom, self.__CHAP_UID).text = str(random.getrandbits(64))

        disp = etree.SubElement(atom, self.__CHAP_DISP)
        etree.SubElement(disp, self.__CHAP_NAME).text = chapter.name
        etree.SubElement(disp, self.__CHAP_IETF).text = chapter.lang.ietf
        etree.SubElement(disp, self.__CHAP_ISO639).text = chapter.lang.iso639

        return atom

    def _get_tree(self) -> ElementTree:
        try:
            return cast(ElementTree, etree.parse(self.chapter_file.to_str()))
        except OSError as oserr:
            Status.fail(f'{self.__class__.__name__}: xml file not found!', exception=FileNotFoundError, chain_err=oserr)


class MplsChapters(Chapters):
    """MplsChapters object"""
    m2ts: VPath
    chapters: List[Chapter]
    fps: Fraction

    def create(self, chapters: List[Chapter], fps: Fraction) -> NoReturn:
        Status.fail(f'{self.__class__.__name__}: Can\'t create a mpls file!', exception=NotImplementedError)

    def set_names(self, names: Sequence[Optional[str]]) -> NoReturn:
        Status.fail(f'{self.__class__.__name__}: Can\'t change name from a mpls file!', exception=NotImplementedError)

    def to_chapters(self, fps: Optional[Fraction] = None, lang: Optional[Lang] = None) -> List[Chapter]:
        if not hasattr(self, 'chapters') or not hasattr(self, 'fps'):
            self.chapters = []
        return self.chapters


class IfoChapters(Chapters):
    """IfoChapters object"""
    chapters: List[Chapter]
    fps: Fraction

    def create(self, chapters: List[Chapter], fps: Fraction) -> NoReturn:
        Status.fail(f'{self.__class__.__name__}: Can\'t create an ifo file!', exception=NotImplementedError)

    def set_names(self, names: Sequence[Optional[str]]) -> NoReturn:
        Status.fail(f'{self.__class__.__name__}: Can\'t change name from an ifo file!', exception=NotImplementedError)

    def to_chapters(self, fps: Optional[Fraction] = None, lang: Optional[Lang] = None) -> List[Chapter]:
        if not hasattr(self, 'chapters') or not hasattr(self, 'fps'):
            self.chapters = []
        return self.chapters


class MplsReader:
    """Mpls reader"""
    bd_folder: VPath

    mpls_folder: VPath
    m2ts_folder: VPath

    lang: Lang
    default_chap_name: str

    class MplsFile(NamedTuple):
        mpls_file: VPath
        mpls_chapters: List[MplsChapters]

    def __init__(self, bd_folder: AnyPath = VPath(), lang: Lang = UNDEFINED, default_chap_name: str = 'Chapter') -> None:
        """Initialise a MplsReader.
           All parameters are optionnal if you just want to use the `parse_mpls` method.

        Args:
            bd_folder (AnyPath, optional):
                A valid bluray folder path should contain a BDMV and CERTIFICATE folders.
                Defaults to VPath().

            lang (Language, optional):
                Language to be set. Defaults to UNDEFINED.

            default_chap_name (str, optional):
                Prefix used as default name for the generated chapters.
                Defaults to 'Chapter'.
        """
        self.bd_folder = VPath(bd_folder)

        self.mpls_folder = self.bd_folder / 'BDMV/PLAYLIST'
        self.m2ts_folder = self.bd_folder / 'BDMV/STREAM'

        self.lang = lang
        self.default_chap_name = default_chap_name

    def get_playlist(self) -> List[MplsFile]:
        """Returns a list of all the mpls files contained in the folder specified in the constructor."""
        mpls_files = sorted(self.mpls_folder.glob('*.mpls'))

        return [
            self.MplsFile(mpls_file=mpls_file,
                          mpls_chapters=self.parse_mpls(mpls_file))
            for mpls_file in mpls_files
        ]

    def write_playlist(self, output_folder: Optional[AnyPath] = None, *,
                       chapters_obj: Type[Chapters] = MatroskaXMLChapters) -> None:
        """Extract and write the playlist folder.

        Args:
            output_folder (Optional[AnyPath], optional):
                Will write in the mpls folder if not specified.
                Defaults to None.

            chapters_obj (Type[Chapters], optional):
                Defaults to MatroskaXMLChapters.
        """
        playlist = self.get_playlist()

        if not output_folder:
            output_folder = self.mpls_folder
        else:
            output_folder = VPath(output_folder)

        for mpls_file in playlist:
            for mpls_chapters in mpls_file.mpls_chapters:

                # Some mpls_chapters don't necessarily have attributes mpls_chapters.chapters or mpls_chapters.fps
                chapters = mpls_chapters.to_chapters()

                if chapters:
                    chaps = chapters_obj(output_folder / f'{mpls_file.mpls_file.stem}_{mpls_chapters.m2ts.stem}')
                    chaps.create(chapters, mpls_chapters.fps)


    def parse_mpls(self, mpls_file: AnyPath) -> List[MplsChapters]:
        """Parse a mpls file and return a list of chapters that were in the mpls file."""
        mpls_file = VPath(mpls_file)
        with mpls_file.open('rb') as file:
            header = mpls.load_movie_playlist(file)

            file.seek(header.playlist_start_address, os.SEEK_SET)
            playlist = mpls.load_playlist(file)

            if not playlist.play_items:
                Status.fail(f'{self.__class__.__name__}: There is no play items in this file!', exception=ValueError)

            file.seek(header.playlist_mark_start_address, os.SEEK_SET)
            playlist_mark = mpls.load_playlist_mark(file)
            if (plsmarks := playlist_mark.playlist_marks) is not None:
                marks = plsmarks
            else:
                Status.fail(f'{self.__class__.__name__}: There is no playlist marks in this file!', exception=ValueError)

        mpls_chaps: List[MplsChapters] = []

        for i, playitem in enumerate(playlist.play_items):

            # Create a MplsChapters and add its linked mpls
            mpls_chap = MplsChapters(mpls_file)

            # Add the m2ts name
            if (name := playitem.clip_information_filename) and \
                    (ext := playitem.clip_codec_identifier):
                mpls_chap.m2ts = self.m2ts_folder / f'{name}.{ext}'.lower()

            # Sort the chapters/marks linked to the current item
            linked_marks = [mark for mark in marks if mark.ref_to_play_item_id == i]

            # linked_marks could be empty
            if linked_marks:
                # Extract the offset
                assert playitem.intime
                offset = min(playitem.intime, linked_marks[0].mark_timestamp)

                # Extract the fps and store it
                if playitem.stn_table and playitem.stn_table.prim_video_stream_entries \
                        and (fps_n := playitem.stn_table.prim_video_stream_entries[0][1].framerate):
                    try:
                        mpls_chap.fps = mpls.FRAMERATE[fps_n]
                    except AttributeError as attr_err:
                        Status.fail(f'{self.__class__.__name__}: Unknown framerate!', exception=ValueError, chain_err=attr_err)
                else:
                    Status.fail(f'{self.__class__.__name__}: No STNTable in playitem!', exception=AttributeError)

                # Finally extract the chapters
                mpls_chap.chapters = self._mplschapters_to_chapters(linked_marks, offset, mpls_chap.fps)

            # And add to the list
            mpls_chaps.append(mpls_chap)

        return mpls_chaps


    def _mplschapters_to_chapters(self, marks: List[mpls.playlist_mark.PlaylistMark], offset: int, fps: Fraction) -> List[Chapter]:
        return [
            Chapter(
                name=f'{self.default_chap_name} {i:02.0f}',
                start_frame=Convert.seconds2f((mark.mark_timestamp - offset) / 45000, fps),
                end_frame=None,
                lang=self.lang
            )
            for i, mark in enumerate(marks, start=1)
        ]


class IfoReader:
    """Mpls reader"""
    dvd_folder: VPath

    ifo_folder: VPath

    lang: Lang
    default_chap_name: str

    def __init__(self, dvd_folder: AnyPath = VPath(), lang: Lang = UNDEFINED, default_chap_name: str = 'Chapter') -> None:
        """Initialise a IfoReader.
           All parameters are optionnal if you just want to use the `parse_ifo` method.

        Args:
            dvd_folder (AnyPath, optional):
                A valid dvd folder path should contain at least a VIDEO_TS folder.
                Defaults to VPath().

            lang (Language, optional):
                Language to be set. Defaults to UNDEFINED.

            default_chap_name (str, optional):
                Prefix used as default name for the generated chapters.
                Defaults to 'Chapter'.
        """
        self.dvd_folder = VPath(dvd_folder)

        self.ifo_folder = self.dvd_folder / 'VIDEO_TS'

        self.lang = lang
        self.default_chap_name = default_chap_name

    def write_programs(self, output_folder: Optional[AnyPath] = None, *,
                       chapters_obj: Type[Chapters] = MatroskaXMLChapters, ifo_file: str = 'VTS_01_0.IFO') -> None:
        """Extract and write the programs from the IFO file to XML chapters files.

        Args:
            output_folder (Optional[AnyPath], optional):
                Will write in the IFO folder if not specified.
                Defaults to None.

            chapters_obj (Type[Chapters], optional):
                Defaults to MatroskaXMLChapters.

            ifo_file (str, optional):
                Name of the ifo file. Defaults to VTS_01_0.IFO.
        """
        ifo_chapters = self.parse_ifo(self.ifo_folder / ifo_file)

        if not output_folder:
            output_folder = self.ifo_folder
        else:
            output_folder = VPath(output_folder)

        for i, ifo_chapter in enumerate(ifo_chapters):

            # Some ifo_chapter don't necessarily have attributes ifo_chapter.chapters
            chapters = ifo_chapter.to_chapters()

            if chapters:
                chaps = chapters_obj(output_folder / f'{ifo_file}_{i:02.0f}')
                chaps.create(chapters, ifo_chapter.fps)


    def parse_ifo(self, ifo_file: AnyPath) -> List[IfoChapters]:
        """Parse a mpls file and return a list of chapters that were in the ifo file."""
        ifo_file = VPath(ifo_file)

        with ifo_file.open('rb') as file:
            pgci = vts_ifo.load_vts_pgci(file)

        ifo_chaps: List[IfoChapters] = []
        for program in pgci.program_chains:

            # Create a IfoChapters and add its linked ifo
            ifo_chap = IfoChapters(ifo_file)

            # Extract the fps and store it
            dvd_fpss = [pb_time.fps for pb_time in program.playback_times]
            if all(dvd_fpss[0] == dvd_fps for dvd_fps in dvd_fpss):
                ifo_chap.fps = vts_ifo.FRAMERATE[dvd_fpss[0]]
            else:
                Status.fail(f'{self.__class__.__name__}: No VFR allowed!', exception=ValueError)

            # Add a zero PlaybackTime and the duration which is the last chapter
            playback_times = [vts_ifo.vts_pgci.PlaybackTime(dvd_fpss[0], 0, 0, 0, 0)]
            playback_times += program.playback_times + [program.duration]

            # Finally extract the chapters
            ifo_chap.chapters = self._ifochapters_to_chapters(playback_times, ifo_chap.fps)

            # And add to the list
            ifo_chaps.append(ifo_chap)

        return ifo_chaps


    def _ifochapters_to_chapters(self, pb_times: List[vts_ifo.vts_pgci.PlaybackTime], fps: Fraction) -> List[Chapter]:
        if (fpsnum := int(fps.numerator / 1000)) == 0:
            raw_fps = fps.numerator
        else:
            raw_fps = fpsnum

        pb_frames = [
            pb_time.frames + (pb_time.hours * 3600 + pb_time.minutes * 60 + pb_time.seconds) * raw_fps
            for pb_time in pb_times
        ]

        pb_frames = [
            pb_frame + sum(pb_frames[:-(len(pb_frames) - i)])
            for i, pb_frame in enumerate(pb_frames[:-1])
        ]

        return [
            Chapter(
                name=f'{self.default_chap_name} {i:02.0f}',
                start_frame=pb_frame,
                end_frame=pb_frames[i],
                lang=self.lang
            )
            for i, pb_frame in enumerate(pb_frames[:-1], start=1)
        ]
