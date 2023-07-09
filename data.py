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

    # Get the th tags from the table.
    heads: list[Node] = table.css("thead tr th")[1:]

    ret: dict = {}

    for tr in table.css("tbody tr"):
        # Create a dictionary for the tr.
        row_key = prefix + tr.css("td")[0].text()
        ret[row_key] = {}

        for i, td in enumerate(tr.css("td")[1:]):
            # If the corresponding th was already used, combine the data.
            if heads[i].text() in ret[row_key]:
                ret[row_key][heads[i].text()] += f" : {td.text()}"
            else:
                ret[row_key][heads[i].text()] = td.text()

    return ret


def get_player_info(player_name: str) -> dict:
    """Returns basic info of the player from the NFL website."""

    document = parse_page(f"{NFL_URL}/players/{player_name}")

    # Get the img tag for the player's picture from the document.
    img: Node = document.css("img.img-responsive")[3]

    return {
        "name": img.attrs.get("alt"),
        "picture": f"{NFL_PICTURE_URL}/{img.attrs.get('src', '').split('/')[-1]}",
    }


def get_career_stat_sheet(player_name: str) -> dict:
    """Returns the players career stats from the NFL website."""

    # Parse the player's page.
    document = parse_page(f"{NFL_URL}/players/{player_name}/stats")

    # Get the table tags from the document.
    if len(tables := document.css("table")) == 0:
        raise PlayerNotFound(player_name)

    # Return the Career Stats table as a dictionary.
    return table_to_dict(tables[-1])


def get_week_stat_sheet(player_name, year: str) -> dict:
    """Returns the year's weekly stats for the player, from the NFL website."""

    document = parse_page(f"{NFL_URL}/players/{player_name}/stats/logs/{year}")

    # Get the table tags from the document.
    if len(tables := document.css("table")) == 0:
        raise PlayerNotFound(player_name)

    # If a Preseason table is present, remove it.
    if tables[0].parent.parent.css("h3")[0].text() == "Preseason":
        tables.pop(0)

    ret: dict = {}

    # Combine the tables into a dictionary.
    prefix: str = "Week "
    for i, table in enumerate(tables):
        ret = ret | table_to_dict(table, prefix)
        prefix = "(post) Week "

    return ret
