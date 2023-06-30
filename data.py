import requests
from selectolax.parser import HTMLParser, Node


NFL_URL = "https://www.nfl.com"
NFL_PICTURE_URL = "https://static.www.nfl.com/image/private/t_player_profile_landscape_2x/f_auto/league"


def parse_site(url: str) -> HTMLParser:
    res = requests.get(url)
    res.raise_for_status()
    return HTMLParser(res.text)


def scrape_table(table: Node) -> dict:
    heads: list[Node] = table.css("thead tr th")[1:]
    stats: dict = {}

    for tr in table.css("tbody tr"):
        assert (row_key := tr.css_first("td")) != None
        stats[row_key.text()] = {}

        for i, td in enumerate(tr.css("td")[1:]):
            stats[row_key.text()][heads[i].text()] = td.text()

    return stats


def get_player_info(player_name: str) -> dict:
    document = parse_site(f"{NFL_URL}/players/{player_name}")

    img: Node = document.css("img.img-responsive")[3]

    return {
        "name": img.attrs.get("alt"),
        "picture": f"{NFL_PICTURE_URL}/{img.attrs.get('src', '').split('/')[-1]}",
    }


def get_career_stats(player_name: str) -> dict:
    document = parse_site(f"{NFL_URL}/players/{player_name}/stats")

    table: Node = document.css("table")[-1]

    return scrape_table(table)


def get_game_stats(player_name, year) -> dict:
    document = parse_site(f"{NFL_URL}/players/{player_name}/stats/logs/{year}")

    table: Node = document.css("table")[-1]

    return scrape_table(table)
