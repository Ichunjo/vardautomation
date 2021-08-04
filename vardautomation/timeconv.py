"""Conversion time module"""

from fractions import Fraction

from .status import Status


class Convert:
    """Collection of static method to perform time conversion"""
    @classmethod
    def ts2f(cls, ts: str, fps: Fraction, /) -> int:
        s = cls.ts2seconds(ts)
        f = cls.seconds2f(s, fps)
        return f

    @classmethod
    def f2ts(cls, f: int, fps: Fraction, /, *, precision: int = 3) -> str:
        s = cls.f2seconds(f, fps)
        ts = cls.seconds2ts(s, precision=precision)
        return ts

    @classmethod
    def seconds2ts(cls, s: float, /, *, precision: int = 3) -> str:
        m = s // 60
        s %= 60
        h = m // 60
        m %= 60
        return cls.composets(h, m, s, precision=precision)

    @classmethod
    def f2assts(cls, f: int, fps: Fraction, /) -> str:
        s = cls.f2seconds(f, fps)
        s -= fps ** -1 * 0.5
        ts = cls.seconds2ts(max(0, s), precision=3)
        return ts[:-1]

    @staticmethod
    def f2seconds(f: int, fps: Fraction, /) -> float:
        if f == 0:
            return 0.0

        t = round(float(10 ** 9 * f * fps ** -1))
        s = t / 10 ** 9
        return s

    @staticmethod
    def ts2seconds(ts: str, /) -> float:
        h, m, s = map(float, ts.split(':'))
        return h * 3600 + m * 60 + s

    @staticmethod
    def seconds2f(s: float, fps: Fraction, /) -> int:
        return round(s * fps)

    @staticmethod
    def composets(h: float, m: float, s: float, /, *, precision: int = 3) -> str:
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
