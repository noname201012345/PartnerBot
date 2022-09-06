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


def get_rfmess(msg):
    message = msg.content
    ref = msg.reference.resolved
    new_string = f"> <@{ref.author.id}>: "
    if "\n" in ref.content:
        rc = ref.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += "> "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start,end]
            new_string += "> "
            start = end + 1
        new_string += rc[start:-1]
    else:
        new_string += f"{ref.content}"
    new_string += f"\n{message}"
    return new_string

def get_rfbefore(msg, before):
    message = msg.content
    new_string = f"> <@{before.author.id}>: "
    if "\n" in ref.content:
        rc = before.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += "> "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start,end]
            new_string += "> "
            start = end + 1
        new_string += rc[start:-1]
    else:
        new_string += f"{before.content}"
    new_string += f"\n{message}"
    return new_string
    
def get_rfdel(msg):
    message = msg.content
    new_string = f"> Deleted Message\n{message}"
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
            if message.type == discord.MessageType.reply:
                await webhook.send(get_rfmess(message),username=message.author.display_name,avatar_url=aurl,files=mfile)
            else:
                await webhook.send(message.content,username=message.author.display_name,avatar_url=aurl,files=mfile)


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
            for w in wkl:
                if w.url == data[x]["url"]:
                    webhook = w
            async for message in tchannel.history(before=after.edited_at, after=before.created_at):
                if message.type == discord.MessageType.reply:
                    if message.reference.resolved.id == after.id:
                        async for msg in channel.history(before=after.edited_at, after=before.created_at):
                            if msg.content == get_rfbefore(message,before) and msg.author.bot:
                                rfile = []
                                for x in msg.attachments:
                                    rfile.append(await x.to_file())
                                await webhook.edit_message(msg.id,content=get_rfmess(message),attachments=rfile)
                                break
            async for message in channel.history(before=after.edited_at, after=before.created_at):
                if before.type == discord.MessageType.reply:
                    if before.reference.cached_message == None:
                        if message.content == get_rfdel(before) and message.author.bot:
                            await webhook.edit_message(message.id,content=get_rfdel(after),attachments=mfile)
                            break
                    else:
                        if message.content == get_rfmess(before) and message.author.bot:
                            await webhook.edit_message(message.id,content=get_rfmess(after),attachments=mfile)
                            break
                else:
                    if message.content == before.content and message.author.bot:
                        await webhook.edit_message(message.id,content=after.content,attachments=mfile)
                        break

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
            tchannel = client.get_channel(tcha)
            wkl = await channel.webhooks()
            for w in wkl:
                if w.url == data[x]["url"]:
                    webhook = w
            
            async for message in tchannel.history(after=msg.created_at, before=timestamp):
                if message.type == discord.MessageType.reply:
                    if message.reference.resolved.id == msg.id:
                        async for mess in channel.history(after=msg.created_at, before=timestamp):
                            if mess.content == get_rfbefore(message,msg) and mess.author.bot:
                                rfile = []
                                for x in msg.attachments:
                                    rfile.append(await x.to_file())
                                await webhook.edit_message(mess.id,content=get_rfdel(message),attachments=rfile)
                                break
            async for message in channel.history(after=msg.created_at, before=timestamp):
                if msg.type == discord.MessageType.reply:
                    if msg.reference.cached_message == None:
                        if message.content == get_rfdel(msg) and message.author.bot:
                            await webhook.delete_message(message.id)
                            break
                    else:
                        if message.content == get_rfmess(msg) and message.author.bot:
                            await webhook.delete_message(message.id)
                            break
                else:
                    if message.content == msg.content and message.author.bot:
                        await webhook.delete_message(message.id)
                        break


token = os.getenv("token")
client.run(token)
