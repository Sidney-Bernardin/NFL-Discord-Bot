import requests
from selectolax.parser import HTMLParser, Node


NFL_URL = "https://www.nfl.com"
NFL_PICTURE_URL = "https://static.www.nfl.com/image/private/t_player_profile_landscape_2x/f_auto/league"


class PlayerNotFound(Exception):
    def __init__(self, player_name):
        super().__init__(f"Couldn't find player {player_name}")


def parse_page(url: str) -> HTMLParser:
    """Returns the page's content as an HTMLParser."""

    res = requests.get(url)
    res.raise_for_status()
    return HTMLParser(res.text)


def table_to_dict(table: Node, prefix: str = "") -> dict:
    """Returns a dictionary that contains data from the table."""

    ret: dict = {}

    # Get the th tags from the table.
    heads: list[Node] = table.css("thead tr th")[1:]

    # Create a dictionary for each tr.
    for tr in table.css("tbody tr"):
        row_key = prefix + tr.css("td")[0].text(strip=True)
        ret[row_key] = {}

        # Put each td's content into the current tr's dictionary.
        for i, td in enumerate(tr.css("td")[1:]):
            # If the corresponding th was already used, combine the data.
            if heads[i].text(strip=True) in ret[row_key]:
                ret[row_key][heads[i].text(strip=True)] += f" : {td.text(strip=True)}"
            else:
                ret[row_key][heads[i].text(strip=True)] = td.text(strip=True)

    return ret


def get_player_info(player_name: str) -> dict:
    """Returns basic info of the player from the NFL website."""

    doc: HTMLParser = parse_page(f"{NFL_URL}/players/{player_name}")

    # Get the img tag for the player's picture from the document.
    if len(imgs := doc.css("main img")) == 0:
        raise PlayerNotFound(player_name)
    img: Node = imgs[1]

    return {
        "name": img.attrs.get("alt"),
        "picture": f"{NFL_PICTURE_URL}/{img.attrs.get('src', '').split('/')[-1]}",
    }


def get_career_stat_sheet(player_name: str) -> dict:
    """Returns the players career stats from the NFL website."""

    doc: HTMLParser = parse_page(f"{NFL_URL}/players/{player_name}/stats")

    # Get the tables from the document.
    if len(tables := doc.css("table")) == 0:
        raise PlayerNotFound(player_name)

    # Return the Career Stats table as a dictionary.
    return table_to_dict(tables[-1])


def get_week_stat_sheet(player_name, year: str) -> dict:
    """Returns the year's weekly stats for the player, from the NFL website."""

    doc: HTMLParser = parse_page(f"{NFL_URL}/players/{player_name}/stats/logs/{year}")

    # Get the tables from the document.
    if len(tables := doc.css("table")) == 0:
        raise PlayerNotFound(player_name)

    # If a Preseason table is present, remove it.
    if tables[0].parent.parent.css("h3")[0].text(strip=True) == "Preseason":
        tables.pop(0)

    # Combine the table's content into a dictionary.
    ret: dict = {}
    prefix: str = "Week "
    for i, table in enumerate(tables):
        ret = ret | table_to_dict(table, prefix)
        prefix = "(post) Week "

    return ret
