import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from schedule import Piece, Schedule

URI_TEMPLATE = "https://www.lectio.dk/lectio/{school_id}/SkemaNy.aspx?type=elev&elevid={elev_id}&week={week}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
}

timestamps_re = re.compile(
    r'(?P<note>[\w\d \(\)\.]*)??\n?(?P<date>\d{1,2}\/\d{1,2}-\d{4}) (?P<start>\d\d:\d\d) til (?P<end>\d\d:\d\d)', flags=re.MULTILINE | re.DOTALL)
extra_attr_re = re.compile(r'\n(\w+): ([\w\d \(\)\.,]+)')
name_re = re.compile(r'Eleven (?P<name>[\w ]+),.*')


def getHTML(uri):
    with requests.get(uri, headers=headers) as resp:
        response = resp.text
    return response


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


def getSchedule(elev_id: str, school_id: str, offset=timedelta(0)) -> Schedule:

    html = getHTML(URI_TEMPLATE.format(
        school_id = school_id,
        elev_id = elev_id,
        week = (datetime.now() + offset).strftime("%V%Y")
    ))

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

def exists(elev_id: str, school_id: str) -> bool:
    html = getHTML(URI_TEMPLATE.format(
        school_id = school_id,
        elev_id = elev_id,
        week = datetime.now().strftime("%V%Y")
    ))

    soup = BeautifulSoup(html, "html.parser")

    return not soup.find("title").contents[0].strip().startswith("Der opstod en fejl")