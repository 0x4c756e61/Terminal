#import station
import discord
from discord.ext import commands
import os
intents = discord.Intents().all()


#setup
prefix = "$"
client = commands.Bot(prefix, intents=intents)
# client = discord.Bot()
client.remove_command("help")

@client.event
async def on_connect():
    print("Connected to Discord, loading bot")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Opening terminal", platform='Twitch'))


#load the bot
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="$man CMD • Have help", platform='Twitch'))

#event and commands handler
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Terminal: command not found')
    else:
        print(error)

@client.command(description="Reload the whole bot", usage="$!reset", aliases=["rs"])
async def reset(ctx):
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            client.unload_extension(f'cogs.{file[:-3]}')
            client.load_extension(f'cogs.{file[:-3]}')

#run the bot
try:
    client.run("TOKEN HERE")
except KeyboardInterrupt:
    client.logout()
