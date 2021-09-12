"""Conversion time module"""

from fractions import Fraction

from .status import Status


class Convert:
    """Collection of methods to perform time conversion"""

    @classmethod
    def ts2f(cls, ts: str, fps: Fraction, /) -> int:
        """
        Convert a timestamp hh:mm:ss.xxxx in number of frames

        :param ts:          Timestamp
        :param fps:         Framerate Per Second
        :return:            Frames
        """
        s = cls.ts2seconds(ts)
        f = cls.seconds2f(s, fps)
        return f

    @classmethod
    def f2ts(cls, f: int, fps: Fraction, /, *, precision: int = 3) -> str:
        """
        Convert frames in timestamp hh:mm:ss.xxxx

        :param f:           Frames
        :param fps:         Framerate Per Second
        :param precision:   Precision number, defaults to 3
        :return:            Timestamp
        """
        s = cls.f2seconds(f, fps)
        ts = cls.seconds2ts(s, precision=precision)
        return ts

    @classmethod
    def seconds2ts(cls, s: float, /, *, precision: int = 3) -> str:
        """
        Convert seconds in timestamp hh:mm:ss.xxx

        :param s:           Seconds
        :param precision:   Precision number, defaults to 3
        :return:            Timestamp
        """
        m = s // 60
        s %= 60
        h = m // 60
        m %= 60
        return cls.composets(h, m, s, precision=precision)

    @classmethod
    def f2assts(cls, f: int, fps: Fraction, /) -> str:
        """
        Convert frames to .ass timestamp hh:mm:ss.xx properly
        by removing half of one frame per second of the specified framerate

        :param f:           Frames
        :param fps:         Framerate Per Second
        :return:            ASS timestamp
        """
        s = cls.f2seconds(f, fps)
        s -= fps ** -1 * 0.5
        ts = cls.seconds2ts(max(0, s), precision=3)
        return ts[:-1]

    @classmethod
    def assts2f(cls, assts: str, fps: Fraction, /) -> int:
        """
        Convert .ass timestamp hh:mm:ss.xx to frames properly
        by adding half of one frame per second of the specified framerate

        :param assts:       ASS timestamp
        :param fps:         Framerate Per Second
        :return:            Frames
        """
        s = cls.ts2seconds(assts)
        if s > 0:
            s += fps ** -1 * 0.5
        return cls.seconds2f(s, fps)

    @staticmethod
    def f2seconds(f: int, fps: Fraction, /) -> float:
        """
        Convert frames to seconds

        :param f:           Frames
        :param fps:         Framerate Per Second
        :return:            Seconds
        """
        if f == 0:
            return 0.0

        t = round(float(10 ** 9 * f * fps ** -1))
        s = t / 10 ** 9
        return s

    @staticmethod
    def ts2seconds(ts: str, /) -> float:
        """
        Convert timestamp hh:mm:ss.xxxx to seconds

        :param ts:          Timestamp
        :return:            Seconds
        """
        h, m, s = map(float, ts.split(':'))
        return h * 3600 + m * 60 + s

    @staticmethod
    def seconds2f(s: float, fps: Fraction, /) -> int:
        """
        Convert seconds to frames

        :param s:           Seconds
        :param fps:         Framerate Per Second
        :return:            Frames
        """
        return round(s * fps)

    @staticmethod
    def composets(h: float, m: float, s: float, /, *, precision: int = 3) -> str:
        """
        Make a timestamp based on given hours, minutes and seconds

        :param h:           Hours
        :param m:           Minutes
        :param s:           Seconds
        :param precision:   Precision number, defaults to 3
        :return:            Timestamp
        """
        if precision == 0:
            out = f"{h:02.0f}:{m:02.0f}:{round(s):02}"
        elif precision == 3:
            out = f"{h:02.0f}:{m:02.0f}:{s:06.3f}"
        elif precision == 6:
            out = f"{h:02.0f}:{m:02.0f}:{s:09.6f}"
        elif precision == 9:
            out = f"{h:02.0f}:{m:02.0f}:{s:012.9f}"
        else:
            Status.fail(f'composets: the precision {precision} must be a multiple of 3 (including 0)')
        return out
