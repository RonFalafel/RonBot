# bot.py
import os
import random
import discord
from discord.ext import commands
import asyncio

# from requests.models import Response
import youtube_dl

from discord.ext import commands
import re, requests, subprocess, urllib.parse, urllib.request
from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()

# FOR READING THE VALUES FROM .env FILE USE THIS:
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

intents = discord.Intents().all()
help_command = commands.DefaultHelpCommand(no_category='Commands')
bot = commands.Bot(command_prefix='-', help_command=help_command, intents=intents)

@bot.command(name="play", help='Plays the song that you asked for!')
async def play(ctx, *args):
    music_name = ' '.join(args)
    await ctx.send("Searching \"" + music_name + "\"")
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" +
                                       query_string)

    search_results = re.findall(r"watch\?v=(\S{11})",
                                formatUrl.read().decode())
    response = requests.get("https://www.youtube.com/watch?v=" +
                            "{}".format(search_results[0]))
    clip = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])

    inspect = BeautifulSoup(response.content, "html.parser")

    yt_title = inspect.find_all("meta", property="og:title")

    for concatMusic1 in yt_title:
        pass

    await ctx.send("Now playing \"" + concatMusic1['content'] +
                   "\" at the address \"" + clip + "\"")

    ydl_opts = {
      'format': 'bestaudio',
      'cookiefile': './youtube.com_cookies.txt'
      }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(clip, download=False)
        URL = info['formats'][0]['url']

    # Gets voice channel of message author
    author_channel = ctx.author.voice
    if author_channel != None:
        voice_channel = author_channel.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client
            vc.stop()
        vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send(str(ctx.author.name) + " is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()

@bot.command(name="bye", help='Leaves voice chat')
async def leave_chat(ctx):
    await play_file(ctx, "./SoundEffects/goodbye.mp3")

async def play_file(ctx, path):
    # Gets voice channel of message author
    author_channel = ctx.author.voice
    if author_channel != None:
        voice_channel = author_channel.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client
            vc.pause()
        vc.play(discord.FFmpegPCMAudio(source=path))
        # Sleep while audio is playing.
        while vc.is_playing():
            await asyncio.sleep(.1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + " is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()

async def play_file_no_disconnect(ctx, path):
    # Gets voice channel of message author
    author_channel = ctx.author.voice
    if author_channel != None:
        voice_channel = author_channel.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client
            vc.pause()
        vc.play(discord.FFmpegPCMAudio(source=path))
    else:
        await ctx.send(str(ctx.author.name) + " is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()

@bot.event #print that the bot is ready to make sure that it actually logged on
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)

bot.run(TOKEN)

