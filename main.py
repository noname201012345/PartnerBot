import discord
from discord.ext import commands
import json
import requests
import base64
from dotenv import load_dotenv
import os
import math
import asyncio
from wereComm import wereComm
from MultiChat import MultiChat

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

client = commands.Bot(command_prefix='p.', intents=intents,help_command=None)

rtoken = os.getenv("rtoken")
header = {"Authorization": "Bearer {}".format(rtoken)}
link="https://api.github.com/repos/noname201012345/PartnerBot/contents/"

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

@client.command()
async def del_web(ctx):
    with open("data.json", "r") as f:
        data = json.load(f)
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    guild = str(ctx.guild.id)
    if guild in data:
        room = data[guild]["id"]
        partner = mchat[room]
        for x in partner:
            try:
                wid = data[x]["webhook"]
                guild = client.get_guild(int(x))
                channel = client.get_channel(data[x]["channel"])
                webhook = await client.fetch_webhook(wid)
                await webhook.delete()
                await ctx.send(f"deleted webhook from Guild: {guild.name}")
            except:
                pass

wereComm(client)
MultiChat(client)
                                
token = os.getenv("token")
client.run(token)
