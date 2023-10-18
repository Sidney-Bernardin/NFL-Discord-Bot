from datetime import date

import discord
from discord.ui import View, Select

import data


class PlayerEmbed(discord.Embed):
    """Displays a player's info and stats."""

    info: dict

    def __init__(self, player_name: str) -> None:
        self.info = data.get_player_info(player_name)

        # Initialize the Embed with the player's name and picture.
        super().__init__(title=self.info["name"], color=discord.Color.green())
        self.set_thumbnail(url=self.info["picture"])

    def set_stats(self, stats: dict) -> None:
        """Adds a new field for each of the stats."""

        self.clear_fields()
        for name, value in stats.items():
            inline = name != "TEAM"
            self.add_field(name=name, value=value, inline=inline)


class WeekSelect(Select):
    """
    Sets the PlayerEmbed's fields to the stats of the selected week from the
    player's year.
    """

    embed: PlayerEmbed
    player_name: str
    year: str
    stat_sheet: dict

    def __init__(self, embed: PlayerEmbed, player_name, year: str) -> None:
        self.embed = embed
        self.player_name = player_name
        self.year = year
        self.stat_sheet = data.get_week_stat_sheet(player_name, year)

        super().__init__(
            placeholder="Select Game",
            # Create an option for each of the stat-sheet's weeks.
            options=[
                discord.SelectOption(
                    label=f"{week} ({stats['OPP']})",
                    value=week,
                )
                for week, stats in self.stat_sheet.items()
            ],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert isinstance(self.view, View)

        # Get the selected week.
        selection: str = self.values[0]

        # Update the PlayerEmbed's fields.
        self.embed.set_stats(self.stat_sheet[selection])
        self.embed.set_footer(text=f"Stats for {self.year} {selection}")

        await interaction.response.edit_message(
            embed=self.embed,
            view=self.view,
        )


class YearSelect(Select):
    """
    Sets the PlayerEmbed's fields to the stats from the selected year of the
    player's NFL career. And adds a new GameSelect to the View.
    """

    embed: PlayerEmbed
    player_name: str
    stat_sheet: dict

    def __init__(self, embed: PlayerEmbed, player_name: str) -> None:
        self.embed = embed
        self.player_name = player_name
        self.stat_sheet = data.get_career_stat_sheet(player_name)

        super().__init__(
            placeholder="Select Year",
            # Create an option for each of the stat-sheet's years.
            options=[
                discord.SelectOption(
                    label=f"{year} ({stats['TEAM']})",
                    value=year,
                )
                for year, stats in self.stat_sheet.items()
            ],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert isinstance(self.view, View)

        # Get the selected year.
        selection: str = self.values[0]

        # Update the PlayerEmbed's fields.
        self.embed.set_stats(self.stat_sheet[selection])
        self.embed.set_footer(text=f"Stats for {selection}")

        # If the View has a GameSelect, remove it so that it can be replaced
        # with a new one.
        if len(children := self.view.children) > 1:
            self.view.remove_item(children[1])

        # Create a new GameSelect for the player and their selected year.
        self.view.add_item(WeekSelect(self.embed, self.player_name, selection))

        await interaction.response.edit_message(
            embed=self.embed,
            view=self.view,
        )
