from enum import Enum
from pprint import pformat
from datetime import datetime, timedelta


class DayStatus(Enum):
    BEFORE = 0
    DURING = 1
    BREAK = 2
    AFTER = 3
    WEEKEND = 4


class TimePeriod:

    start = None
    end = None

    def duration(self) -> timedelta:
        return self.end - self.start

    def startSameDay(self, other) -> bool:
        return self.start.date() == other.start.date()

    def isOnDay(self, day) -> bool:
        return self.start.date() == day

    def __gt__(self, other):
        if type(other) is type(self):
            return self.end > other.end
        if type(other) is datetime:
            return self.end > other
        raise NotImplementedError()

    def __lt__(self, other):
        if type(other) is type(self):
            return self.end < other.end
        if type(other) is datetime:
            return self.end < other
        raise NotImplementedError()


class Piece(TimePeriod):

    def __init__(self, start: datetime, end: datetime, **extra):
        self.start = start
        self.end = end
        self.extra = extra

    def isAt(self, time: datetime) -> bool:
        return self.start < time < self.end

    def json(self):
        return dict(start=self.start, end=self.end, **self.extra)


    def __bool__(self):
        return True

    def __contains__(self, other):
        if type(other) is datetime:
            return self.isAt(other)
        raise NotImplementedError()

    def __repr__(self):
        return f"Piece(start={self.start}, end={self.end}, **{pformat(self.extra)})"

    def __eq__(self, other):
        if type(other) is type(self):
            return self.start == other.start and self.end == other.end
        raise NotImplementedError()


class Schedule(TimePeriod):

    def __init__(self, name: str, *pieces, offset=timedelta(0)):
        self.name = name
        self._pieces = list(pieces)
        self._pieces.sort()
        self.offset = offset

        try:
            self.start = min(self._pieces).start
            self.end = max(self._pieces).end
        except ValueError:
            self.start = datetime.now() + self.offset
            self.end = datetime.now() + self.offset


    def pieceNow(self) -> (DayStatus, Piece):
        return self.pieceAt(datetime.now() + self.offset)

    def pieceAt(self, time: datetime) -> (DayStatus, Piece):
        next_piece = self._pieces[0]

        for piece in self._pieces:
            if time in piece:
                return DayStatus.DURING, piece
            elif piece.start - time < next_piece.start - time:
                next_piece = piece

        return self.schoolStatus(), next_piece

    def today(self):
        date = (datetime.now() + self.offset).date()
        day = list(filter(lambda p: p.isOnDay(date), self._pieces))
        day.sort()
        return day

    def schoolStatus(self):
        now = datetime.now() + self.offset
        today = self.today()

        if len(today) == 0:
            return DayStatus.WEEKEND
        if now < today[0]:
            return DayStatus.BEFORE
        if now > today[-1]:
            return DayStatus.AFTER
        for piece in today:
            if now in piece:
                return DayStatus.DURING
        return DayStatus.BREAK

    def json(self):
        json = {
            "name": self.name,
            "schoolstatus": self.schoolStatus().value,
            "start": self.start,
            "end": self.end 
        }
        for i, p in enumerate(self._pieces):
            json[str(i)] = p.json()
        return json

    def jsonToday(self):
        today = self.today()

        if len(today) == 0:
            return {
                "start": datetime.now() + self.offset,
                "end": datetime.now() + self.offset,
                "name": self.name,
                "schoolstatus": DayStatus.WEEKEND.value
            }

        json = {
            "name": self.name,
            "schoolstatus": self.schoolStatus().value,
            "start": today[0].start,
            "end": today[-1].end 
        }
        for i, p in enumerate(today):
            json[str(i)] = p.json()
        return json

    def __repr__(self):
        return f"Schedule(name={self.name}, *{pformat(self._pieces)})"

    def __getitem__(self, item):
        for piece in self._pieces:
            if item == piece:
                return piece

    def __setitem__(self, item, value):
        for i, piece in enumerate(self._pieces):
            if item == piece:
                self._pieces[i] = item
