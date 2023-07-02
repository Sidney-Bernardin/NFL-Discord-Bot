import requests
from selectolax.parser import HTMLParser, Node


NFL_URL = "https://www.nfl.com"
NFL_PICTURE_URL = "https://static.www.nfl.com/image/private/t_player_profile_landscape_2x/f_auto/league"


class PlayerNotFound(Exception):
    def __init__(self, player_name):
        super().__init__(f"Couldn't find player {player_name}")


def parse_site(url: str) -> HTMLParser:
    res = requests.get(url)
    res.raise_for_status()
    return HTMLParser(res.text)


def scrape_table(table: Node, prefix: str = "") -> dict:
    heads: list[Node] = table.css("thead tr th")[1:]
    stats: dict = {}

    for tr in table.css("tbody tr"):
        row_key = prefix + tr.css("td")[0].text()
        stats[row_key] = {}

        for i, td in enumerate(tr.css("td")[1:]):
            if heads[i].text() in stats[row_key]:
                stats[row_key][heads[i].text()] += f" : {td.text()}"
            else:
                stats[row_key][heads[i].text()] = td.text()

    return stats


def get_player_info(player_name: str) -> dict:
    document = parse_site(f"{NFL_URL}/players/{player_name}")

    img: Node = document.css("img.img-responsive")[3]

    return {
        "name": img.attrs.get("alt"),
        "picture": f"{NFL_PICTURE_URL}/{img.attrs.get('src', '').split('/')[-1]}",
    }


def get_career_stats(player_name: str) -> dict:
    URI: str = f"{NFL_URL}/players/{player_name}/stats"
    document = parse_site(URI)

    if len(tables := document.css("table")) == 0:
        raise PlayerNotFound(player_name)

    return scrape_table(tables[-1])


def get_game_stats(player_name, year: str) -> dict:
    document = parse_site(f"{NFL_URL}/players/{player_name}/stats/logs/{year}")

    if len(tables := document.css("table")) == 0:
        raise PlayerNotFound(player_name)

    if tables[0].parent.parent.css("h3")[0].text() == "Preseason":
        tables.pop(0)

    ret: dict = {}

    prefix: str = "Week "
    for i, table in enumerate(tables):
        ret = ret | scrape_table(table, prefix)
        prefix = "(post) Week "

    return ret
