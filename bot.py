# bot.py
import os
import random
import discord
import asyncio

from requests.models import Response
import youtube_dl

from discord.ext import commands
import re, requests, subprocess, urllib.parse, urllib.request
from bs4 import BeautifulSoup

from keep_alive import keep_alive

# FOR READING THE VALUES FROM .env FILE USE THIS:
# TOKEN = os.environ['DISCORD_TOKEN']

TOKEN = "ODgzNjkzOTY4MDQ5NzIxMzU1.YTNqJA.F66cHoRBhUkuHC-O-N01OnyiZ58"

FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

help_command = commands.DefaultHelpCommand(no_category='Commands')
bot = commands.Bot(command_prefix='-', help_command=help_command)


@bot.command(name='q', help='Responds with a random quote!')
async def quote(ctx):
    quotes = [
        'Fuck off you big fat cunt!', 'I eat spaghetti!',
        'I’m headin’ west like I’m fuckin’ blowin’ Kanye.',
        'These god damned niggers don’t know their place in white America.',
        'Sonic the Hedgehog',
        'You wouldn\'t happen to have a chili dog on you, would you?'
    ]

    response = random.choice(quotes)
    await ctx.send(response)


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


@bot.command(name="rr", help='Try it if you’re brave!')
async def rick_roll(ctx):
    await play_file(ctx, "./Sounds/rickroll.mp3")


@bot.command(name="rand", help='Plays random sound!')
async def random_sound(ctx):
    paths = os.listdir("./Sounds")
    await play_file(ctx, "./Sounds/" + random.choice(paths))


@bot.command(name="fart", help='Plays a fart!')
async def fart(ctx):
    paths = os.listdir("./SoundEffects/farts")
    await play_file_no_disconnect(
        ctx, "./SoundEffects/farts/" + random.choice(paths))


@bot.command(name="ah", help='Air Horn for you’re mama jokes')
async def air_horn(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/airhorn.mp3")


@bot.command(name="bonk", help='For when horny')
async def bonk(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/bonk.mp3")


@bot.command(name="mine", help='Minecraft ouchy moment')
async def minecraft_ouch(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/minecrafthit.mp3")


@bot.command(name="uwu", help='Don’t use this please')
async def uwu(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/uwu.mp3")


@bot.command(name="fortnite", help='Plays the fortnite sound effect')
async def fortnite(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/fortnite.mp3")


@bot.command(name="kiss", help='IF U THINK...')
async def you_are_dead_wrong(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/youaredeadwrong.mp3")


@bot.command(name="good", help='Good Pussy')
async def good_pussy(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/goodpussy.mp3")


@bot.command(name="god", help='God is dead OwO')
async def god(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/godowo.mp3")


@bot.command(name="gta", help='GTA Mission Passed')
async def gta(ctx):
    await play_file_no_disconnect(ctx, "./SoundEffects/gta.mp3")


@bot.command(name="bye", help='Leaves voice chat')
async def leave_chat(ctx):
    await play_file(ctx, "./SoundEffects/goodbye.mp3")


@bot.command(name="pic", help='Sends a beautiful picture')
async def pic(ctx):
    await ctx.send(file=discord.File('./Pictures/sonic2.png'))


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


keep_alive()
bot.run(TOKEN)
