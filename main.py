import discord
import ffmpeg
import discord.utils
import asyncio
import traceback
import sys
import os
from discord import member
from discord.ext.commands import has_permissions, MissingPermissions
from github import Github
from discord_slash import SlashCommand
from discord_slash import cog_ext
from discord.ext import commands
from discord_slash.utils import manage_commands # Allows us to manage the command settings.
from dotenv import load_dotenv

load_dotenv('.env')


client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

g = Github("9b952db489f8ce8319b31b2c826cc2fdfffffd0e")
repo = g.get_repo("OwOShiba/slashtest")

guild_ids = [755813698920120320]

initial_extensions = ['cogs.cmds',
					            'cogs.fun',
                      'cogs.music',
                      'cogs.hypixel']

for extension in initial_extensions:
		client.load_extension(extension)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="porn"))
    print("Bot is ready!")

@slash.slash(
  name="reload",
  description="Reloads a cog.",
  guild_ids=guild_ids,
  options = [manage_commands.create_option(
    name = "Cog",
    description = "Cog",
    option_type = 3,
    required = True,
    choices = ["cmds", "fun", "music", "hypixel", "all"]
  )]
)

async def _reload(ctx, cog: str):
  cogname = cog.capitalize()
  if cogname == "All":
    for extension in initial_extensions:
      try:
        client.unload_extension(f"{extension}")
        client.load_extension(f"{extension}")
      except Exception as e:
        await ctx.send(e)
    await ctx.send(f'All cogs have been reloaded.')
  elif cogname == "Cmds" or "Fun":
    try:
      client.unload_extension(f"cogs.{cog}")
      client.load_extension(f"cogs.{cog}")
      await ctx.send(f'The cog **{cogname}** was reloaded.')
    except Exception as e:
        await ctx.send(e)

client.run(os.environ.get("MY_TOKEN"))
