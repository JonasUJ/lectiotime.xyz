import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from schedule import Piece, Schedule
from lectiologin import getSession

URI_TEMPLATE = "https://www.lectio.dk/lectio/{schoolid}/SkemaNy.aspx?type=elev&elevid={elevid}&week={week}"

timestamps_re = re.compile(
    r'(?P<note>[\w\d \(\)\.]*)??\n?(?P<date>\d{1,2}\/\d{1,2}-\d{4}) (?P<start>\d\d:\d\d) til (?P<end>\d\d:\d\d)', flags=re.MULTILINE | re.DOTALL)
extra_attr_re = re.compile(r'\n(\w+): ([\w\d \(\)\.,]+)')
name_re = re.compile(r'Eleven (?P<name>[\w ]+),.*')
id_re = re.compile(r'elevid=(?P<id>\d+)')


def getHTML(session, uri):
    resp = session.get(uri)
    return resp.text


def getDatetime(date, time) -> datetime:
    day = date.split("/")[0]

    if len(day) == 1:
        day = "0" + day

    month, year = date.split("/")[1].split("-")

    if len(month) == 1:
        month = "0" + month

    return datetime.strptime(f"{day}/{month}/{year} {time}", "%d/%m/%Y %H:%M")


def getPiece(elem) -> Piece:
    data = elem.get("data-additionalinfo")
    times = timestamps_re.search(data)

    if not times:
        return

    extras = extra_attr_re.findall(data)

    start = getDatetime(times.group("date"), times.group("start"))
    end = getDatetime(times.group("date"), times.group("end"))

    return Piece(start=start, end=end, **dict(extras))


def getSchedule(schoolid: str, user: str, pwd: str, offset=timedelta(0)) -> Schedule:

    session = getSession(
        schoolid = schoolid,
        user = user,
        pwd = pwd
    )

    elevid = id_re.search(session.get(f'https://lectio.dk/lectio/{schoolid}/forside.aspx').text).group('id')

    html = getHTML(
        session,
        URI_TEMPLATE.format(
            schoolid = schoolid,
            elevid = elevid,
            week = (datetime.now() + offset).strftime("%V%Y")
        )
    )

    soup = BeautifulSoup(html, "html.parser")

    pieces = []
    schedule_pieces = soup.find_all(lambda tag: tag.name == "a" and "s2skemabrik" in tag.get(
        "class", "") and "s2bgbox" in tag.get("class", ""))

    for schedule_piece in schedule_pieces:
        piece = getPiece(schedule_piece)
        if piece:
            pieces.append(piece)

    name = name_re.match(
        soup.find("div", class_="maintitle").contents[0]).group("name")

    return Schedule(name, *pieces, offset=offset)
