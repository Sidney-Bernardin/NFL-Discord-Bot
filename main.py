import discord
from discord.ext import commands
from discord.ui import View

from config import config
import data
from components import PlayerEmbed, YearSelect


# Create intents for the bot.
intents = discord.Intents()
intents.messages = True
intents.message_content = True

# Create the bot.
bot: commands.Bot = commands.Bot(
    command_prefix=config["PREFIX"],
    intents=intents,
)
bot.remove_command("help")


@bot.group(invoke_without_command=True)
async def help(ctx: commands.Context) -> None:
    """Responds with an Embed that contains help info."""

    embed: discord.Embed = discord.Embed(title="Usage")
    embed.add_field(name="Help Syntax", value="/help [command]", inline=False)
    embed.add_field(name="Commands", value="stat")

    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError) -> None:
    """
    Responds with an Embed that contains the error. If the error isn't
    expected, it's raised instead.
    """

    ORIGINAL_ERR = getattr(err, "original", err)
    EXPECTED = [data.PlayerNotFound, commands.MissingRequiredArgument]

    # Check if the original error is expected.
    if type(ORIGINAL_ERR) not in EXPECTED:
        raise err

    # Create an Embed containing the error message.
    embed: discord.Embed = discord.Embed(
        title=ORIGINAL_ERR.args[0],
        color=discord.Color.red(),
    )

    await ctx.send(embed=embed)


@bot.command()
async def stat(ctx: commands.Context, player_name: str) -> None:
    """
    Responds with an Embed containing the player's stats, and with Selects for
    specifying specific stats.
    """

    embed: PlayerEmbed = PlayerEmbed(player_name)
    year_select: YearSelect = YearSelect(embed, player_name)

    view: View = View()
    view.add_item(year_select)

    await ctx.send(embed=embed, view=view)


@help.command(name="stat")
async def help_stat(ctx: commands.Context):
    """Responds with an Embed that contains help info for the stat command."""

    embed: discord.Embed = discord.Embed(
        title="Using the 'stat' command",
        description="Gets the stats for an active NFL player.",
    )
    embed.add_field(name="Syntax", value="/stat <player_name>")

    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(config["TOKEN"], log_handler=None, root_logger=True)
