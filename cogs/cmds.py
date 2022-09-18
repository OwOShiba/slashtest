import discord
import ffmpeg
import discord.utils
import asyncio
import traceback
import sys
from discord import member
from discord.ext.commands import has_permissions, MissingPermissions
from github import Github
from discord_slash import SlashCommand
from discord_slash import cog_ext
from discord.ext import commands
from discord_slash import error
from discord_slash.utils import manage_commands # Allows us to manage the command settings.

g = Github("9b952db489f8ce8319b31b2c826cc2fdfffffd0e")
repo = g.get_repo("OwOShiba/slashtest")
rgb = discord.Color.from_rgb(0,255,110)

guild_ids = [755813698920120320]

class Cmds(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @cog_ext.cog_slash(
      name="hello",
      description="Greets the bot",
      guild_ids=guild_ids
    )
    async def _hello(self, ctx):
      await ctx.send(f"Hello, {ctx.author.mention}!")

    @cog_ext.cog_slash(
      name="help",
      description="Displays a list of commands.",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "Section",
        description = "The section you would like to see commands for",
        option_type = 3,
        required = False,
        choices = ["Misc", "Music", "Economy"]
      )],
    )
    async def _help(self, ctx, section:str=None):
      if section is None:
        embed=discord.Embed(title="Help Sections", color=rgb)
        embed.add_field(value="** **", name="`Misc` \n`Music` \n`Economy`", inline=True)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/815934504396783687/819329684671692800/slashpfp.png")
        await ctx.send(embed=embed)
      elif section == "Misc" or "misc" or "Misc." or "misc.":
        embed = discord.Embed(title='Misc. Commands:', description='**Hello** ~ Simply greets the bot \n**Help** ~ Displays this message \n**Issue** ~ Creates an issue for the github repository. \n**Reload [ADMIN]** ~ Reloads a cog. \n**Suggest** ~ Adds a suggestion for Shiba to view.', color=rgb)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/815934504396783687/819329684671692800/slashpfp.png")
        await ctx.send(embed=embed)
      elif section == "Music" or "music":
        embed = discord.Embed(title='Music Commands:', description='**Join** ~ Joins your current voice-chat \n**Leave** ~ Leaves the voice-chat \n**Play** ~ Plays the specified sound \n**Sounds** ~ Displays a list of sounds', color=rgb)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/815934504396783687/819329684671692800/slashpfp.png")
        await ctx.send(embed=embed)
      elif section == "Economy" or "economy":
        embed = discord.Embed(title='Economy Commands:', description="**Balance** ~ Displays yours or another user's current balance \n**Pay** ~ Transfer some of your money to another user \n**Give [ADMIN]** ~ Gives a user a set amount of money \n**Remove [ADMIN]** ~ Removes a set amount of money from a user", color=rgb)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/815934504396783687/819329684671692800/slashpfp.png")
        await ctx.send(embed=embed)
      else:
        embed=discord.Embed(title="Help Sections", color=rgb)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/815934504396783687/819329684671692800/slashpfp.png")
        embed.add_field(value="** **", name="`Misc` \n`Music` \n`Economy`", inline=True)
        await ctx.send(embed=embed)


    @cog_ext.cog_slash(
      name="issue",
      description="Creates an issue on the repository.",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "Title",
        description = "Title of the issue",
        option_type = 3,
        required = True
      ),
      manage_commands.create_option(
        name = "Description",
        description = "Description of the issue",
        option_type = 3,
        required = True
      )]
    )

    async def _issue(self, ctx, title: str, body: str):
      repo.create_issue(title=f"{title}", body=f"{body}      Created by {ctx.author}")
      embed = discord.Embed(title='Issue Created', description=f'{title} \n** **  \n{body}', color=rgb)
      embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author}')
      embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/815934504396783687/819354446064386098/githnub.png')
      await ctx.send(embed=embed)

    @cog_ext.cog_slash(
      name="suggest",
      description="Creates an issue on the repository.",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "Suggestion",
        description = "Suggestion",
        option_type = 3,
        required = True
      )]
    )

    async def _suggest(self, ctx, suggestion: str):
      label = repo.get_label("suggestion")
      repo.create_issue(title=f"Suggestion from {ctx.author}", body=f"{suggestion}", labels=[label], assignee="OwOShiba")
      embed = discord.Embed(title=f'Suggestion Created', description=f'** **  \n{suggestion}', color=rgb)
      embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author}')
      embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/660118447644082177/819227201266122772/suggestion.png')
      await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Cmds(bot))
	print('Commands have loaded')