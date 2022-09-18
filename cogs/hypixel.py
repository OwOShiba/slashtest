import discord
import ffmpeg
import discord.utils
import asyncio
import traceback
import sys
import requests
import skyblock
import os
import json
import math
import levels
import datetime
from discord import member
from discord.ext.commands import has_permissions, MissingPermissions
from discord_slash import SlashCommand
from discord_slash import cog_ext
from discord.ext import commands
from discord_slash import error
from discord_slash.utils import manage_commands # Allows us to manage the command settings.

guild_ids = [755813698920120320]
apikey = "15c87812-c73b-4aef-98e5-f12c424a67fe"


class Hypixel(commands.Cog):
    def __init__(self, bot):
      self.bot = bot


    @cog_ext.cog_slash(
      name="profile",
      description="Displays your hypixel profile",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "Username",
        description = "The username of the player you are searching.",
        option_type = 3,
        required = True
      )]
    )

    async def _profile(self, ctx, username: str=None):
        data = requests.get(f"https://api.hypixel.net/player?key={apikey}&name={username}").json()
        if data["player"] is None:
            ctx.send('Please provide a valid username.')
        else:
            rank = levels.getRank(username, apikey)
            uuid = data["player"]["uuid"]
            karma = data["player"]["karma"]

            if data["player"]["lastLogout"] < data["player"]["lastLogin"]:
                online = "Online"
            else:
                online = "Offline"

            if online == "Online":
              rgb = discord.Color.from_rgb(0,255,110)
            else:
              rgb = discord.Color.from_rgb(255,66,66)

            realflog = data["player"]["firstLogin"]/1000
            reallog = data["player"]["lastLogin"]/1000
            exp = data["player"]["networkExp"]
            lvl = levels.getLevel(exp)
            join = datetime.datetime.fromtimestamp(realflog)
            login = datetime.datetime.fromtimestamp(reallog)
            

            embed=discord.Embed(title=f"[{rank}]  {username}", description="** **", color=rgb)
            embed.set_author(name="Hypixel Profile")
            embed.set_thumbnail(url=f"https://mc-heads.net/body/{uuid}/250")
            embed.add_field(name="** **", value=f"`UUID: {uuid}`", inline=True)
            embed.add_field(name="** **", value=f"`Karma: {karma}`", inline=True)
            embed.add_field(name="** **", value=f"`Status: {online}`", inline=True)
            embed.add_field(name="** **", value=f"`Network Level: {lvl}`", inline=True)
            embed.add_field(name="** **", value=f"`Joined: {join}`", inline=True)
            embed.add_field(name="** **", value=f"`Last Login: {login}`", inline=True)
            await ctx.send(embed=embed)


    @cog_ext.cog_slash(
      name="skyblock",
      description="Displays your skyblock profile",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "Username",
        description = "The username of the player you are searching.",
        option_type = 3,
        required = True
      )]
    )

    async def _skyblock(self, ctx, username:str):
      ctx.send(f'Sorry, this command is not currently completed. \n`Username: {username}`')


    @cog_ext.cog_slash(
      name="auction",
      description="Displays an auction for an item below a certain price",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "Item",
        description = "The item you want notification for.",
        option_type = 3,
        required = True
      ),
      manage_commands.create_option(
        name = "Price",
        description = "The price to search below.",
        option_type = 4,
        required = True)]
    )

    async def _auction(self, ctx, item: str, price: int):
      ctx.send(f'Sorry, this command is not currently finished. \n`Item: {item}` \n`Price: {price}`')
      




def setup(bot):
	bot.add_cog(Hypixel(bot))
	print('Hypixel has loaded')