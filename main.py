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


@bot.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError) -> None:
    original_err = getattr(err, "original", err)

    if (
        type(original_err) == data.PlayerNotFound
        or type(original_err) == commands.MissingRequiredArgument
    ):
        await ctx.send(original_err.args[0])
        return

    raise err


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
        logging.error("Couldn't file environment variable 'TOKEN'")
        exit()

    bot.run(token, log_handler=None, root_logger=True)
