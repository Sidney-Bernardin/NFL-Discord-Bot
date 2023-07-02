from datetime import date

import discord
from discord.ui import View, Select

import data


class PlayerEmbed(discord.Embed):
    info: dict

    def __init__(self, player_name: str):
        self.info = data.get_player_info(player_name)
        super().__init__(title=self.info["name"], color=discord.Color.green())
        self.set_thumbnail(url=self.info["picture"])

    def load_dict(self, d: dict) -> None:
        self.clear_fields()
        for k, v in d.items():
            inline = k != "TEAM"
            self.add_field(name=k, value=v, inline=inline)


class GameSelect(Select):
    embed: PlayerEmbed
    player_name: str
    year: str
    stats: dict

    def __init__(self, embed: PlayerEmbed, player_name, year: str):
        self.embed = embed
        self.player_name = player_name
        self.year = year
        self.stats = data.get_game_stats(player_name, year)

        super().__init__(
            placeholder="Select Game",
            options=[
                discord.SelectOption(
                    label=f"{week} ({stats['OPP']})",
                    value=week,
                )
                for week, stats in self.stats.items()
            ],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert isinstance(self.view, View)

        selection: str = self.values[0]

        self.embed.load_dict(self.stats[selection])
        self.embed.set_footer(text=f"Stats for {self.year} {selection}")

        await interaction.response.edit_message(
            embed=self.embed,
            view=self.view,
        )


class YearSelect(Select):
    embed: PlayerEmbed
    player_name: str
    stats: dict

    def __init__(self, embed: PlayerEmbed, player_name: str):
        self.embed = embed
        self.player_name = player_name
        self.stats = data.get_career_stats(player_name)

        super().__init__(
            placeholder="Select Year",
            options=[
                discord.SelectOption(
                    label=f"{year} ({stats['TEAM']})",
                    value=year,
                )
                for year, stats in self.stats.items()
            ],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert isinstance(self.view, View)

        selection: str = self.values[0]

        self.embed.load_dict(self.stats[selection])
        self.embed.set_footer(text=f"Stats for {selection}")

        if len(children := self.view.children) > 1:
            self.view.remove_item(children[1])

        self.view.add_item(GameSelect(self.embed, self.player_name, selection))

        await interaction.response.edit_message(
            embed=self.embed,
            view=self.view,
        )
