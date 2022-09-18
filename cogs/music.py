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

class Music(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @cog_ext.cog_slash(
      name="play",
      description="Plays a sound.",
      guild_ids=guild_ids,
      options = [manage_commands.create_option(
        name = "Sound",
        description = "Sound",
        option_type = 3,
        required = True,
        choices = ["chingchong", "hold", "music", "music2", "nom", "regice", "regirock", "registeel", "rickroll", "smack", "woo", "porch"]
      )],

    )
    async def _play(self, ctx, sound: str):
      achannel = ctx.author.voice.channel
      sounds = ["chingchong", "hold", "music", "music2", "nom", "regice", "regirock", "registeel", "rickroll", "smack", "woo", "porch"]
      if sound.lower() in sounds:
        if not isinstance(channel, discord.VoiceChannel):
          server = ctx.guild
          channel = discord.utils.get_channel(achannel)

          voice = discord.utils.get(channel, guild=server)

          if voice is None:
            await ctx.guild.change_voice_state(channel=channel, self_deaf=True) 
            await channel.connect()
            vc = discord.utils.get(channel, guild=server)
            vc.play(discord.FFmpegPCMAudio(source=f"sounds/{sound}.mp3"), after=lambda e: print(f'Played {sound}.mp3'))
            vc.source.volume = 0.06
            print(f"finished connect to: {channel.id}")
          elif channel.id != achannel.id:
            await ctx.guild.change_voice_state(channel=channel, self_deaf=True) 
            await voice.move_to(channel)
            vc = discord.utils.get(channel, guild=server)
            vc.play(discord.FFmpegPCMAudio(source=f"sounds/{sound}.mp3"), after=lambda e: print(f'Played {sound}.mp3'))
            vc.source.volume = 0.06
        else:
          vc = discord.utils.get(channel, guild=server)
          vc.play(discord.FFmpegPCMAudio(source=f"sounds/{sound}.mp3"), after=lambda e: print(f'Played {sound}.mp3'))
          vc.source.volume = 0.06
      else:
          ctx.send('That sound does not exist, use /sounds for a list.')


    @cog_ext.cog_slash(
        name="join",
        description="Joins a voice channel.",
        guild_ids=guild_ids
      )
      
    async def _join(self, ctx):
          if ctx.author.voice.channel is None:
              ctx.send("You are not in a voice-chat.")
          else:
              channel = ctx.author.voice.channel
              await channel.connect()
              await ctx.guild.change_voice_state(channel=channel, self_deaf=True) 

    @cog_ext.cog_slash(
      name="sounds",
      description="Displays a list of sounds.",
      guild_ids=guild_ids
    )
    async def _sounds(self, ctx):
      	embed = discord.Embed(title='List of sounds:', description='**Porch** \n**Hold** \n**Music** \n**Music2** \n**ChingChong** \n**Nom** \n**Regice** \n**Regirock** \n**Registeel** \n**RickRoll** \n**Smack** \n**Woo**', color=rgb)
      	await ctx.send(embed=embed)


    @cog_ext.cog_slash(
      name="leave",
      description="Leaves the current voice channel.",
      guild_ids=guild_ids,
    )
    async def _leave(self, ctx):
      server = ctx.guild
      voice = discord.utils.get(self.bot.voice_clients, guild=server)
      if voice is None:
        ctx.send('I am not currently in a voice-chat.')
      else:
        await voice.disconnect()

def setup(bot):
	bot.add_cog(Music(bot))
	print('Music has loaded')