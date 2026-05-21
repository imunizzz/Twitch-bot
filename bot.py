from discord.ext import commands
from dotenv import load_dotenv

import subprocess
import threading
import aiofiles
import discord
import asyncio
import aiohttp
import random
import ctypes
import re
import os

LOAD ENV

load_dotenv()

WINDOWS TITLE

if os.name == "nt":
ctypes.windll.kernel32.SetConsoleTitleW('zoom')

ENV VARIABLES

token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX", "/")

chat_channel = int(os.getenv("CHAT_CHANNEL", "0"))
bots_channel = int(os.getenv("BOTS_CHANNEL", "0"))

administrators = []

admin_ids = os.getenv("ADMIN_IDS", "")

if admin_ids:
administrators = [
int(x.strip())
for x in admin_ids.split(",")
if x.strip().isdigit()
]

DISCORD

intents = discord.Intents().all()

bot = commands.Bot(
command_prefix=prefix,
case_insensitive=True,
intents=intents
)

bot.remove_command('help')

QUEUE

queue = []

WORKER

def zoom():
while True:
try:
task, arg1, arg2 = queue.pop(0).split('-')

if os.name != "nt":  
            process = f'./{task}'  
        else:  
            process = task  

        subprocess.run([process, arg1, arg2])  

    except Exception:  
        pass

threading.Thread(target=zoom, daemon=True).start()

READY

@bot.event
async def on_ready():

print(f'Servers: {len(bot.guilds)}')  

for guild in bot.guilds:  
    print(guild.name)  

print()  

while True:  

    members = sum(  
        [guild.member_count for guild in bot.guilds]  
    )  

    activity = discord.Activity(  
        type=discord.ActivityType.watching,  
        name=f'{members} users!'  
    )  

    await bot.change_presence(activity=activity)  

    await asyncio.sleep(60)

MEMBER JOIN

@bot.event
async def on_member_join(member):

channel = await bot.fetch_channel(bots_channel)  

await channel.send(  
    f'Welcome to **zoom**, {member.mention}.\n'  
    f'Type `/help` to get started!'  
)

ERROR HANDLER

@bot.event
async def on_command_error(ctx, error: Exception):

if ctx.channel.id == bots_channel:  

    if isinstance(error, commands.CommandOnCooldown):  

        embed = discord.Embed(  
            color=16379747,  
            description=f'{error}'  
        )  

        await ctx.send(embed=embed)  

    elif isinstance(error, commands.MissingRequiredArgument):  

        embed = discord.Embed(  
            color=16379747,  
            description='You are missing arguments required to run this command!'  
        )  

        await ctx.send(embed=embed)  

        ctx.command.reset_cooldown(ctx)  

    elif 'You do not own this bot.' in str(error):  

        embed = discord.Embed(  
            color=16379747,  
            description='You do not have permission to run this command!'  
        )  

        await ctx.send(embed=embed)  

    else:  
        print(str(error))  

else:  

    try:  
        await ctx.message.delete()  
    except:  
        pass

HELP

@bot.command()
async def help(ctx):

print(f'{ctx.author} | {ctx.author.id} -> /help')  

if ctx.channel.type != discord.ChannelType.private:  

    embed = discord.Embed(color=16379747)  

    embed.add_field(  
        name='Help',  
        value='`/help`',  
        inline=True  
    )  

    embed.add_field(  
        name='Open Ticket',  
        value='`/ticket`',  
        inline=True  
    )  

    embed.add_field(  
        name='Close Ticket',  
        value='`/close`',  
        inline=True  
    )  

    embed.add_field(  
        name='Tasks',  
        value='`/tasks`',  
        inline=True  
    )  

    embed.add_field(  
        name='Twitch Followers',  
        value='`/tfollow (channel)`',  
        inline=True  
    )  

    embed.add_field(  
        name='⭐ Twitch Spam',  
        value='`/tspam (channel) (message)`',  
        inline=True  
    )  

    embed.add_field(  
        name='Roblox Followers',  
        value='`/rfollow (user id)`',  
        inline=True  
    )  

    embed.add_field(  
        name='Roblox Templates',  
        value='`/rget (asset id)`',  
        inline=True  
    )  

    await ctx.send(embed=embed)

TICKET

@bot.command()
async def ticket(ctx):

print(f'{ctx.author} | {ctx.author.id} -> /ticket')  

if ctx.channel.type != discord.ChannelType.private:  

    channels = [str(x) for x in bot.get_all_channels()]  

    if f'ticket-{ctx.author.id}' in str(channels):  

        embed = discord.Embed(  
            color=16379747,  
            description='You already have a ticket open!'  
        )  

        await ctx.send(embed=embed)  

    else:  

        ticket_channel = await ctx.guild.create_text_channel(  
            f'ticket-{ctx.author.id}'  
        )  

        await ticket_channel.set_permissions(  
            ctx.guild.get_role(ctx.guild.id),  
            send_messages=False,  
            read_messages=False  
        )  

        await ticket_channel.set_permissions(  
            ctx.author,  
            send_messages=True,  
            read_messages=True,  
            add_reactions=True,  
            embed_links=True,  
            attach_files=True,  
            read_message_history=True,  
            external_emojis=True  
        )  

        embed = discord.Embed(  
            color=16379747,  
            description='Please enter the reason for this ticket, type `/close` if you want to close this ticket.'  
        )  

        await ticket_channel.send(  
            f'{ctx.author.mention}',  
            embed=embed  
        )  

        await ctx.message.delete()

CLOSE

@bot.command()
async def close(ctx):

print(f'{ctx.author} | {ctx.author.id} -> /close')  

if ctx.channel.type != discord.ChannelType.private:  

    if ctx.channel.name == f'ticket-{ctx.author.id}':  

        await ctx.channel.delete()  

    elif ctx.author.id in administrators and 'ticket' in ctx.channel.name:  

        await ctx.channel.delete()  

    else:  

        embed = discord.Embed(  
            color=16379747,  
            description='You do not have permission to run this command!'  
        )  

        await ctx.send(embed=embed)

TASKS

@bot.command()
async def tasks(ctx):

print(f'{ctx.author} | {ctx.author.id} -> /tasks')  

if ctx.channel.type != discord.ChannelType.private:  

    if ctx.channel.id == bots_channel:  

        embed = discord.Embed(  
            color=16379747,  
            description=f'`{len(queue)}` tasks in the queue!'  
        )  

        await ctx.send(embed=embed)  

    else:  
        await ctx.message.delete()

START BOT

bot.run(token)
