import os

import discord
from discord.ext import commands
from discord.ui import View, Select

import data


intents = discord.Intents()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


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
            options=[discord.SelectOption(label=week) for week in stats.keys()],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        assert isinstance(self.view, View)

        week: str = self.values[0]
        stats: dict = data.get_game_stats(self.player_name, self.year)

        self.embed.load_dict(stats[week])
        self.embed.set_footer(text=f"Stats for week {week}, {self.year}")

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
            options=[discord.SelectOption(label=year) for year in stats.keys()],
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


@bot.command()
async def stat(ctx: commands.Context) -> None:
    embed: PlayerEmbed = PlayerEmbed("saquon-barkley")
    year_select: YearSelect = YearSelect(embed, "saquon-barkley")

    view: View = View()
    view.add_item(year_select)

    await ctx.send(
        ephemeral=True,
        embed=embed,
        view=view,
    )


if __name__ == "__main__":
    if (token := os.environ.get("TOKEN")) == None:
        raise EnvironmentError("Environment variable 'TOKEN' is required")

    bot.run(token)
