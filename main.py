import discord
from discord.ext import commands
import json
import datetime
import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

client = commands.Bot(command_prefix='!', intents=intents)

rtoken = os.getenv("rtoken")
header = {"Authorization": "Bearer {}".format(rtoken)}
datalink = "https://api.github.com/repos/noname201012345/PartnerBot/contents/data.json"

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')


def get_mes(msg):
    new_string = ""
    if msg.find(":") == -1 or msg.find(":", (msg.find(":") + 1)) == -1:
        new_string += msg
    else:
        start = (msg.find(":") + 1)
        new_string += msg[0:msg.find(":")]
        if msg[start] == " ":
            new_string += ":"
        while start != len(msg) and msg.find(":", start) != -1:
            end = msg.find(":", start)
            check = 0
            for emoji in client.emojis:
                if msg[start:end] == emoji.name:
                    new_string += f":{emoji.name}:"
                    check = 1
                    break
            if msg[start] == " " and msg[start - 2] == " ":
                new_string += ":"
            if check == 0:
                if msg[start] != " ":
                    new_string += ":"
                new_string += msg[start:end]
                if msg[end - 1] != " " and msg[end - 1] != ":":
                    new_string += ":"
            start = end + 1
        if msg.find(":", start) == -1 and start != len(msg):
            new_string += msg[start:len(msg)]
        if start == len(msg) and msg[start - 2] == " ":
            new_string += ":"
    return new_string


@client.command()
async def add(ctx, partner):
    with open("data.json", "r") as f:
        data = json.load(f)
    guild = str(ctx.guild.id)
    try:
        if data[guild]["url"] != None:
            wc = 0
            for i in ctx.channel.webhooks:
                if i.url == data[guild]["url"]:
                    wc = 1
            if wc == 0:
                for l in client.get_channel(data[guild]["channel"]).webhooks:
                    if l.url == data[guild]["url"]:
                        l.delete()
                webhook = await ctx.channel.create_webhook(name="PartnerBot")
                data[guild]["url"] = webhook.url
        else:
            webhook = await ctx.channel.create_webhook(name="PartnerBot")
            data[guild]["url"] = webhook.url
        if data[guild]["id"] == None or data[guild]["channel"] == None:
            data[guild]["channel"] = ctx.channel.id
            data[guild]["id"] = []
            data[guild]["id"].append(partner)
        else:
            data[guild]["channel"] = ctx.channel.id
            c = 0
            for x in data[guild]["id"]:
                if x == partner:
                    c = 1
            if c == 0:
                data[guild]["id"].append(partner)
        with open("data.json", "w") as f:
            json.dump(data, f)
        r = requests.get(datalink,headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(data), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(datalink, data=json.dumps(rjson), headers=header)
    except:
        data[guild] = {}
        data[guild]["channel"] = ctx.channel.id
        data[guild]["id"] = []
        data[guild]["id"].append(partner)
        webhook = await ctx.channel.create_webhook(name="PartnerBot")
        data[guild]["url"] = webhook.url
        with open("data.json", "w") as f:
            json.dump(data, f)
        r = requests.get(datalink,headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(data), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(datalink, data=json.dumps(rjson), headers=header)
    await ctx.send("connected!")


@client.command()
async def remove(ctx, partner):
    with open("data.json", "r") as f:
        data = json.load(f)
    guild = str(ctx.guild.id)
    try:
        if data[guild]["id"] == None:
            pass
        else:
            for x in data[guild]["id"]:
                if x == partner:
                    data[guild]["id"].remove(x)
            with open("data.json", "w") as f:
                json.dump(data, f)    
            r = requests.get(datalink,headers=header)
            sh=r.json()["sha"]
            base64S= base64.b64encode(bytes(json.dumps(data), "utf-8"))
            rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
            response = requests.put(datalink, data=json.dumps(rjson), headers=header)
    except:
        ctx.send("you didn't add yet!")


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content.startswith("!add") or message.content.startswith("!remove"):
        await message.delete()
    with open("data.json", "r") as f:
        data = json.load(f)
    guild = str(message.guild.id)
    tcha = data[guild]["channel"]
    partner = data[guild]["id"]
    if not message.author.bot and message.channel.id == tcha:
        for x in partner:
            wurl = data[x]["url"]
            channel = client.get_channel(data[x]["channel"])
            whl = await channel.webhooks()
            for w in whl:
                if w.url == wurl:
                    webhook = w
            mfile = []
            for x in message.attachments:
                mfile.append(await x.to_file())
            if message.author.avatar == None:
                aurl = webhook.default_avatar
            else:
                aurl = message.author.avatar.url
            await webhook.send(get_mes(message.content),username=message.author.display_name,avatar_url=aurl,files=mfile)


@client.event
async def on_message_edit(before, after):
    with open("data.json", "r") as f:
        data = json.load(f)
    guild = str(before.guild.id)
    tcha = data[guild]["channel"]
    partner = data[guild]["id"]
    mfile = []
    for x in after.attachments:
        mfile.append(await x.to_file())
    if not after.author.bot and after.channel.id == tcha:
        for x in partner:
            channel = client.get_channel(data[x]["channel"])
            tchannel = client.get_channel(tcha)
            wkl = await channel.webhooks()
            mesloc = []
            for w in wkl:
                if w.url == data[x]["url"]:
                    webhook = w
            ind=0
            async for mess in tchannel.history(before=after.edited_at, after=before.created_at):
                if mess.content == before.content and not mess.author.bot:
                    mesloc.append(mess)
            for m in mesloc:
                if m.id == before.id:
                    ind = mesloc.index(m)
            mesloc.clear()
            async for message in channel.history(before=after.edited_at, after=before.created_at):
                if message.content == get_mes(before.content) and message.author.bot:
                    mesloc.append(message)
            await webhook.edit_message(mesloc[ind].id,content=get_mes(after.content),attachments=mfile)

@client.event
async def on_message_delete(msg):
    with open("data.json", "r") as f:
        data = json.load(f)
    guild = str(msg.guild.id)
    tcha = data[guild]["channel"]
    partner = data[guild]["id"]
    timestamp = datetime.datetime.now()
    if not msg.author.bot and msg.channel.id == tcha:
        for x in partner:
            channel = client.get_channel(data[x]["channel"])
            wkl = await channel.webhooks()
            for w in wkl:
                if w.url == data[x]["url"]:
                    webhook = w
            async for message in channel.history(after=msg.created_at, before=timestamp):
                if message.content == get_mes(msg.content) and message.author.bot:
                    await webhook.delete_message(message.id)
                    break


token = os.getenv("token")
client.run(token)
