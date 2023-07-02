import os
import logging
import logging.handlers

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
bot.remove_command("help")


@bot.group(invoke_without_command=True)
async def help(ctx: commands.Context) -> None:
    embed: discord.Embed = discord.Embed(title="Usage")
    embed.add_field(name="Help Syntax", value="/help [command]", inline=False)
    embed.add_field(name="Commands", value="stat")
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError) -> None:
    original_err = getattr(err, "original", err)

    if (
        type(original_err) == data.PlayerNotFound
        or type(original_err) == commands.MissingRequiredArgument
    ):
        await ctx.send(
            embed=discord.Embed(
                title=original_err.args[0],
                color=discord.Color.red(),
            )
        )
        return

    raise err


@bot.command()
async def stat(ctx: commands.Context, player_name: str) -> None:
    embed: PlayerEmbed = PlayerEmbed(player_name)
    year_select: YearSelect = YearSelect(embed, player_name)

    view: View = View()
    view.add_item(year_select)

    await ctx.send(
        embed=embed,
        view=view,
    )


@help.command(name="stat")
async def help_stat(ctx: commands.Context):
    embed: discord.Embed = discord.Embed(
        title="Using the 'stat' command",
        description="Gets the stats for an active NFL player.",
    )
    embed.add_field(name="Syntax", value="/stat <player_name>")
    await ctx.send(embed=embed)


if __name__ == "__main__":
    formatter = logging.Formatter(
        "({asctime}) [{levelname}] {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    file_handler = logging.handlers.RotatingFileHandler(
        filename="debug.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            stream_handler,
            file_handler,
        ],
    )

    if (token := os.environ.get("TOKEN")) == None:
        logging.error("Couldn't find environment variable 'TOKEN'")
        exit()

    bot.run(token, log_handler=None, root_logger=True)
