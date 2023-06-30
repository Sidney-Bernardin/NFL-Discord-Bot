import discord
from discord.ui import View, Select

import data


class PlayerEmbed(discord.Embed):
    info: dict

    def __init__(self, player_name: str):
        self.info = data.get_player_info(player_name)

        super().__init__(
            title=self.info["name"],
            color=discord.Colour.blue(),
        )

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

    def __init__(self, embed: PlayerEmbed, player_name, year: str):
        self.embed = embed
        self.player_name = player_name
        self.year = year

        stats: dict = data.get_game_stats(player_name, year)

        super().__init__(
            placeholder="Select Game",
            options=[
                discord.SelectOption(
                    label=f"{sub_season} - Week {week} ({week_stats['OPP']})",
                    value=f"{sub_season},{week}",
                )
                for sub_season, sub_season_stats in stats.items()
                for week, week_stats in sub_season_stats.items()
            ],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert isinstance(self.view, View)

        selection: list[str] = self.values[0].split(",")
        sub_season: str = selection[0]
        week: str = selection[1]

        stats: dict = data.get_game_stats(self.player_name, self.year)

        self.embed.load_dict(stats[sub_season][week])
        self.embed.set_footer(text=f"Stats for {self.year}, {sub_season}, week {week}")

        await interaction.response.edit_message(
            embed=self.embed,
            view=self.view,
        )


class YearSelect(Select):
    embed: PlayerEmbed
    player_name: str

    def __init__(self, embed: PlayerEmbed, player_name: str):
        self.embed = embed
        self.player_name = player_name

        stats: dict = data.get_career_stats(player_name)

        super().__init__(
            placeholder="Select Year",
            options=[
                discord.SelectOption(
                    label=f"{year} ({year_stats['TEAM']})",
                    value=year,
                )
                for year, year_stats in stats.items()
            ],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert isinstance(self.view, View)

        year: str = self.values[0]
        stats: dict = data.get_career_stats(self.player_name)

        self.embed.load_dict(stats[year])
        self.embed.set_footer(text=f"Stats for {year}")

        if len((children := self.view.children)) > 1:
            self.view.remove_item(children[1])

        self.view.add_item(GameSelect(self.embed, self.player_name, year))

        await interaction.response.edit_message(
            embed=self.embed,
            view=self.view,
        )
