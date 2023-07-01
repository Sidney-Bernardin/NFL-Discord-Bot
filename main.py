import os

import discord
from discord.ext import commands
from discord.ui import View

from components import PlayerEmbed, YearSelect
import data


intents = discord.Intents()
intents.messages = True
intents.message_content = True

bot: commands.Bot = commands.Bot(
    command_prefix="/",
    intents=intents,
)


@bot.command()
async def stat(ctx: commands.Context, player_name: str) -> None:
    embed: PlayerEmbed = PlayerEmbed(player_name)
    year_select: YearSelect = YearSelect(embed, player_name)

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
