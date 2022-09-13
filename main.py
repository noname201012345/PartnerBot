import discord
from discord.ext import commands
import json
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
link="https://api.github.com/repos/noname201012345/PartnerBot/contents/"

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

def get_rfpe(msg):
    message = msg.content
    ref = msg.reference.resolved
    new_string = f"> **{ref.author.display_name}**: "
    if "\n" in ref.content:
        rc = ref.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += " "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start:end]
            new_string += " "
            start = end + 1
        new_string += rc[start:len(rc)]
    else:
        new_string += f"{ref.content}"
    new_string += f"\n{message}"
    return new_string

def grfpe(msg):
    message = msg.content
    ref = msg.reference.resolved
    new_string = f"> **{ref.author.display_name}**: "
    if "\n" in ref.content:
        rc = ref.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += " "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start:end]
            new_string += " "
            start = end + 1
        new_string += rc[start:len(rc)]
    else:
        new_string += f"{ref.content}"
    return new_string
    
def get_rfmess(msg):
    message = msg.content
    ref = msg.reference.cached_message
    new_string = f"> **{ref.author.display_name}**: "
    if "\n" in ref.content:
        rc = ref.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += " "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start:end]
            new_string += " "
            start = end + 1
        new_string += rc[start:len(rc)]
    else:
        new_string += f"{ref.content}"
    new_string += f"\n{message}"
    return new_string

def get_rfbefore(msg, before):
    message = msg.content
    new_string = f"> **{before.author.display_name}**: "
    if "\n" in before.content:
        rc = before.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += " "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start:end]
            new_string += " "
            start = end + 1
        new_string += rc[start:len(rc)]
    else:
        new_string += f"{before.content}"
    new_string += f"\n{message}"
    return new_string

def grf(msg):
    message = msg.content
    ref = msg.reference.cached_message
    new_string = f"> **{ref.author.display_name}**: "
    if "\n" in ref.content:
        rc = ref.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += " "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start:end]
            new_string += " "
            start = end + 1
        new_string += rc[start:len(rc)]
    else:
        new_string += f"{ref.content}"
    return new_string
    
def to_ref(msg):
    ref = msg
    new_string = f"> **{ref.author.display_name}**: "
    if "\n" in ref.content:
        rc = ref.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += " "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start:end]
            new_string += " "
            start = end + 1
        new_string += rc[start:len(rc)]
    else:
        new_string += f"{ref.content}"
    return new_string
    
def grfb(msg, before):
    message = msg.content
    new_string = f"> **{before.author.display_name}**: "
    if "\n" in before.content:
        rc = before.content
        start = rc.find("\n") + 1
        new_string += rc[0:(start-1)]
        new_string += " "
        while rc.find("\n",start) != -1:
            end = rc.find("\n",start)
            new_string += rc[start:end]
            new_string += " "
            start = end + 1
        new_string += rc[start:len(rc)]
    else:
        new_string += f"{before.content}"
    return new_string
    

def grfd():
    new_string = f"> Deleted Message"
    return new_string
    
def get_rfdel(msg):
    message = msg.content
    new_string = f"> Deleted Message\n{message}"
    return new_string
    
@client.command()
async def join(ctx, name):
    with open("data.json", "r") as f:
        data = json.load(f)
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    guild = str(ctx.guild.id)
    if name in mchat:
        marr = mchat[name]
        c=0
        if guild in marr:
                await ctx.send("Đã ở trong phòng này")
                c=1
        if c==0:
                cs=0
                for y in mchat:
                        if guild in mchat[y]:
                                await ctx.send("Đã tham gia phòng chat khác")
                                cs=1
                                break
                if cs==0:
                        marr.append(guild)
                        data[guild] = {}
                        data[guild]["channel"] = ctx.channel.id
                        data[guild]["id"] = name
                        webhook = await ctx.channel.create_webhook(name="PartnerBot")
                        data[guild]["url"] = webhook.url
                        await ctx.send("Tham gia thành công")
                        with open("data.json", "w") as f:
                            json.dump(data, f)
                        with open("multichat.json", "w") as f:
                            json.dump(mchat, f)
    else:
        await ctx.send("Không tồn tại phòng chat")
    r = requests.get(link+"data.json",headers=header)
    rm = requests.get(link+"multichat.json",headers=header)
    sh=r.json()["sha"]
    shm=rm.json()["sha"]
    base64S= base64.b64encode(bytes(json.dumps(data), "utf-8"))
    base64M= base64.b64encode(bytes(json.dumps(mchat), "utf-8"))
    rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
    rmjson = {"message":"cf", "content":base64M.decode("utf-8"),"sha":shm}
    response = requests.put(link+"data.json", data=json.dumps(rjson), headers=header)
    rps = requests.put(link+"multichat.json", data=json.dumps(rmjson), headers=header)



@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content.startswith("!join"):
        await message.delete()
    with open("data.json", "r") as f:
        data = json.load(f)
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    guild = str(message.guild.id)
    tcha = data[guild]["channel"]
    room = data[guild]["id"]
    partner = mchat[room]
    if not message.author.bot and message.channel.id == tcha:
        for x in partner:
            if x == message.guild.id:
                pass
            else:
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
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    guild = str(before.guild.id)
    tcha = data[guild]["channel"]
    room = data[guild]["id"]
    partner = mchat[room]
    mfile = []
    for x in after.attachments:
        mfile.append(await x.to_file())
    if not after.author.bot and after.channel.id == tcha:
        for x in partner:
            if x == message.guild.id:
                pass
            else:
                channel = client.get_channel(data[x]["channel"])
                tchannel = client.get_channel(tcha)
                wkl = await channel.webhooks()
                twkl = await tchannel.webhooks()
                for w in wkl:
                    if w.url == data[x]["url"]:
                        webhook = w
                for tw in twkl:
                    if tw.url == data[guild]["url"]:
                        twebhook = tw
                async for message in tchannel.history(after=before.created_at):
                    if message.type == discord.MessageType.reply:
                        if message.reference.resolved.id == after.id:
                            async for msg in channel.history(after=before.created_at):
                                if len(message.content) != 0:
                                    if msg.content == get_rfbefore(message,before) and msg.author.bot:
                                        await webhook.edit_message(msg.id,content=get_rfmess(message))
                                        break
                                else:
                                    if msg.content == grfb(message,before) and msg.author.bot:
                                        await webhook.edit_message(msg.id,content=get_rfmess(message))
                                        break
                    if message.author.bot and message.content.startswith(to_ref(before)):
                        async for msg in channel.history(after=before.created_at):
                            if len(msg.content) != 0 and msg.type == discord.MessageType.reply:
                                if get_rfpe(msg) == message.content:
                                    await twebhook.edit_message(message.id,content=get_rfbefore(msg,after))
                                    break
                            elif len(msg.content) == 0 and msg.type == discord.MessageType.reply:
                                if grfpe(msg) == message.content:
                                    await twebhook.edit_message(message.id,content=get_rfbefore(msg,after))
                                    break
                async for message in channel.history(after=before.created_at):
                    if before.type == discord.MessageType.reply:
                        if before.reference.cached_message == None:
                            if len(before.content) != 0:
                                if message.content == get_rfdel(before) and message.author.bot:
                                    await webhook.edit_message(message.id,content=get_rfdel(after),attachments=mfile)
                                    break
                            else:
                                if message.content == grfd() and message.author.bot:
                                    await webhook.edit_message(message.id,content=get_rfdel(after),attachments=mfile)
                                    break
                        else:
                            if len(before.content) != 0:
                                if message.content == get_rfmess(before) and message.author.bot:
                                    await webhook.edit_message(message.id,content=get_rfmess(after),attachments=mfile)
                                    break
                            else:
                                if message.content == grf(before) and message.author.bot:
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
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    guild = str(msg.guild.id)
    tcha = data[guild]["channel"]
    room = data[guild]["id"]
    partner = mchat[room]
    if not msg.author.bot and msg.channel.id == tcha:
        for x in partner:
            if x == message.guild.id:
                pass
            else:
                channel = client.get_channel(data[x]["channel"])
                tchannel = client.get_channel(tcha)
                wkl = await channel.webhooks()
                twkl = await tchannel.webhooks()
                for w in wkl:
                    if w.url == data[x]["url"]:
                        webhook = w
                for tw in twkl:
                    if tw.url == data[guild]["url"]:
                        twebhook = tw
                async for message in tchannel.history(after=msg.created_at):
                    if message.type == discord.MessageType.reply:
                        if message.reference.resolved.id == msg.id:
                            async for mess in channel.history(after=msg.created_at):
                                if mess.content == get_rfbefore(message,msg) and mess.author.bot:
                                    await webhook.edit_message(mess.id,content=get_rfdel(message))
                                    break
                    if message.author.bot and message.content.startswith(to_ref(msg)):
                        async for mess in channel.history(after=msg.created_at):
                            if len(mess.content) != 0 and mess.type == discord.MessageType.reply:
                                if get_rfpe(mess) == message.content:
                                    await twebhook.edit_message(message.id,content=get_rfdel(mess))
                                    break
                            elif len(mess.content) == 0 and mess.type == discord.MessageType.reply:
                                if grfpe(mess) == message.content:
                                    await twebhook.edit_message(message.id,content=get_rfdel(mess))
                                    break
                async for message in channel.history(after=msg.created_at):
                    if msg.type == discord.MessageType.reply:
                        if msg.reference.cached_message == None:
                            if len(msg.content)!=0:
                                if message.content == get_rfdel(msg) and message.author.bot:
                                    await webhook.delete_message(message.id)
                                    break
                            else:
                                if message.content == grfd() and message.author.bot:
                                    await webhook.delete_message(message.id)
                                    break
                        else:
                            if len(msg.content)!=0:
                                if message.content == get_rfmess(msg) and message.author.bot:
                                    await webhook.delete_message(message.id)
                                    break
                            else:
                                if message.content == grf(msg) and message.author.bot:
                                    await webhook.delete_message(message.id)
                                    break
                    else:
                        if message.content == msg.content and message.author.bot:
                            await webhook.delete_message(message.id)
                            break


token = os.getenv("ptoken")
client.run(token)
