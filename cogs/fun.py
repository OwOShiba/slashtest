import discord
import ffmpeg
import discord.utils
import asyncio
import traceback
import sqlite3
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
guild_ids = [755813698920120320]
rgb = discord.Color.from_rgb(0,255,110)

db = sqlite3.connect('money.db')
SQL = db.cursor()
START_BALANCE = 100.00
C_NAME = "Coins"

class Fun(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @cog_ext.cog_slash(
      name="balance",
      description="Displays your balance",
      guild_ids=guild_ids
    )
    async def _balance(self, ctx):
        USER_ID = ctx.author.id
        USER_NAME = str(ctx.author)
        SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
        SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = SQL.fetchone()

        if result_userID is None:
            SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
            db.commit()

        SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        result_userbal = SQL.fetchone()
        await ctx.send(f"{ctx.author.mention} has a balance of {result_userbal[0]} {C_NAME}")

    @cog_ext.cog_slash( 
      name="pay",
      description="Transfers some money to another user.",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "User",
        description = "Person to give money to",
        option_type = 6,
        required = True
      ),manage_commands.create_option(
        name = "Amount",
        description = "Amount of money to pay them",
        option_type = 4,
        required = True
        )]
    )

    async def _pay(self, ctx, other: discord.Member, amount: int):
        USER_ID = ctx.author.id
        USER_NAME = str(ctx.author)
        OTHER_ID = other.id
        OTHER_NAME = str(other)

        SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
        SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = SQL.fetchone()
        SQL.execute(f'select user_id from Accounts where user_id="{OTHER_ID}"')
        result_otherID = SQL.fetchone()

        if result_userID is None:
            SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
            db.commit()
        if result_otherID is None:
            SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (OTHER_NAME, OTHER_ID, START_BALANCE))
            db.commit()

        SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        result_userbal = SQL.fetchone()
        if amount > int(result_userbal[0]):
            await ctx.send(f"{ctx.author.mention} does not have that many {C_NAME}")
            return

        SQL.execute('update Accounts set balance = balance - ? where user_id = ?', (amount, USER_ID))
        db.commit()
        SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (amount, OTHER_ID))
        db.commit()

        await ctx.send(f"{ctx.author.mention} sent {other.mention} {amount} {C_NAME}")

    @cog_ext.cog_slash( 
      name="baltop",
      description="Displays the users with top 5 balance.",
      guild_ids=guild_ids
    )

    async def _baltop(self, ctx):
        SQL.execute(f"select user_name, balance from Accounts order by balance desc")
        result_top10 = SQL.fetchmany(2)

        embed = discord.Embed(
            color = rgb
        )

        embed.set_author(name="Top 10 bank accounts")
        embed.add_field(name="#1", value=f"User: {result_top10[0][0]} Bal: {result_top10[0][1]}", inline=False)
        embed.add_field(name="#2", value=f"User: {result_top10[1][0]} Bal: {result_top10[1][1]}", inline=False)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash( 
      name="give",
      description="Gives money to a user.",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "User",
        description = "Person to give money to",
        option_type = 6,
        required = True
      ),manage_commands.create_option(
        name = "Amount",
        description = "Amount of money to give them",
        option_type = 4,
        required = True
        )]
    )

    async def _give(self, ctx, other: discord.Member, amount: int):
        OTHER_ID = other.id
        OTHER_NAME = str(other)

        SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
        SQL.execute(f'select user_id from Accounts where user_id="{OTHER_ID}"')
        result_otherID = SQL.fetchone()

        if result_otherID is None:
            SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (OTHER_NAME, OTHER_ID, START_BALANCE))
            db.commit()

        SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (amount, OTHER_ID))
        db.commit()

        await ctx.send(f"Gave {other.mention} {amount} {C_NAME}")

    @cog_ext.cog_slash( 
      name="remove",
      description="Removes money from a user.",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "User",
        description = "The person to remove from",
        option_type = 6,
        required = True
      ),manage_commands.create_option(
        name = "Amount",
        description = "Amount of money to remove",
        option_type = 4,
        required = True
        )]
    )

    async def _give(self, ctx, other: discord.Member, amount: int):
        OTHER_ID = other.id
        OTHER_NAME = str(other)

        SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
        SQL.execute(f'select user_id from Accounts where user_id="{OTHER_ID}"')
        result_otherID = SQL.fetchone()

        if result_otherID is None:
            SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (OTHER_NAME, OTHER_ID, START_BALANCE))
            db.commit()

        SQL.execute('update Accounts set balance = balance - ? where user_id = ?', (amount, OTHER_ID))
        db.commit()

        await ctx.send(f"Removed {amount} {C_NAME} from {other.mention}")


def setup(bot):
	bot.add_cog(Fun(bot))
	print('Fun has loaded')