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
@commands.has_guild_permissions(administrator=True)
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
                        data[guild]["webhook"] = webhook.id
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

@client.command()
@commands.has_guild_permissions(administrator=True)
async def create(ctx,name):
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    if name in mchat:
        await ctx.send("Phòng chat đã tồn tại!")
    else:
        mchat[name] = []
        await ctx.send("Tạo phòng chat thành công!")
        with open("multichat.json", "w") as f:
            json.dump(mchat, f)
        rm = requests.get(link+"multichat.json",headers=header)
        shm=rm.json()["sha"]
        base64M= base64.b64encode(bytes(json.dumps(mchat), "utf-8"))
        rmjson = {"message":"cf", "content":base64M.decode("utf-8"),"sha":shm}
        rps = requests.put(link+"multichat.json", data=json.dumps(rmjson), headers=header)
        
@client.command()
@commands.has_guild_permissions(administrator=True)
async def msview(ctx):
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    room=mchat
    if len(room) > 10:
        mpage = math.ceil(len(room)/10)
    else:
        mpage = 1
    page = 1
    emb = discord.Embed(color=0x0049FF,title="Các Phòng Chat Hiện Có:",description=" ")
    emb.set_footer(text=f"Trang {page}/{mpage}")
    count = 1
    for x in room:
        if count > page*10:
            break
        emb.add_field(name=f"{list(room).index(x)+1}, {x}",value=f"Số server tham gia: {len(mchat[x])}",inline=False)
        count+=1
    async def precallback(interaction):
        nonlocal page,msg
        if mpage < page:
            page -= 1
        emb.clear_fields()
        count=1
        for x in room:
            if count < ((page-1)*10+1):
                count+=1
                continue
            if count > page*10:
                break
            emb.add_field(name=f"{list(room).index(x)+1}, {x}",value=f"Số server tham gia: {len(mchat[x])}",inline=False)
            count+=1
        emb.set_footer(text=f"Trang {page}/{mpage}")
        await msg.edit(embed=emb)
        await interaction.response.defer()
    async def nextcallback(interaction):
        nonlocal page,msg
        if mpage > page:
            page += 1
        emb.clear_fields()
        count=1
        for x in room:
            if count < ((page-1)*10+1):
                count+=1
                continue
            if count > page*10:
                break
            emb.add_field(name=f"{list(room).index(x)+1}, {x}",value=f"Số server tham gia: {len(mchat[x])}",inline=False)
            count+=1
        emb.set_footer(text=f"Trang {page}/{mpage}")
        await msg.edit(embed=emb)
        await interaction.response.defer()
    v=discord.ui.View(timeout=180)
    backB=discord.ui.Button(label="<",style=discord.ButtonStyle.blurple)
    nextB=discord.ui.Button(label=">",style=discord.ButtonStyle.blurple)
    backB.callback = precallback
    nextB.callback = nextcallback
    v.add_item(backB)
    v.add_item(nextB)
    msg = await ctx.send(embed=emb,view=v)
    
@client.command()
@commands.has_guild_permissions(administrator=True)
async def msban(ctx, id):
    with open("ban.json", "r") as f:
        ban = json.load(f)
    ban["ban_id"].append(id)
    with open("ban.json", "w") as f:
        json.dump(ban, f)
    await ctx.send(content=f"Đã ban player với id: {id}")
    r = requests.get(link+"ban.json",headers=header)
    sh=r.json()["sha"]
    base64S= base64.b64encode(bytes(json.dumps(ban), "utf-8"))
    rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
    response = requests.put(link+"ban.json", data=json.dumps(rjson), headers=header)
    
@client.command()
@commands.has_guild_permissions(administrator=True)
async def leave(ctx):
    with open("data.json", "r") as f:
        data = json.load(f)
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    guild = str(ctx.guild.id)
    if guild in data:
        room = data[guild]["id"]
        mchat[room].remove(guild)
        wid = data[guild]["webhook"]
        channel = client.get_channel(data[guild]["channel"])
        try:
            webhook = await client.fetch_webhook(wid)
            await webhook.delete()
        except:
            print("deleted webhook!")
        data.pop(guild)
        await ctx.send("Rời phòng thành công")
        with open("data.json", "w") as f:
            json.dump(data, f)
        with open("multichat.json", "w") as f:
            json.dump(mchat, f)
    else:
        await ctx.send("Chưa tham gia phòng chat nào!")
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
            
LCount = {}
        
@client.event
async def on_(message):
    await client.process_commands(message)
    with open("data.json", "r") as f:
        data = json.load(f)
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    with open("ban.json", "r") as f:
        ban = json.load(f)
    guild = str(message.guild.id)
    if guild in data:
        tcha = data[guild]["channel"]
        room = data[guild]["id"]
        partner = mchat[room]
        if not message.author.bot and message.channel.id == tcha:
            if "https://" in message.content and "@everyone" not in message.content and "@here" not in message.content:
                try:
                    LCount[str(message.author.id)]
                except:
                    LCount[str(message.author.id)] = 0
                if LCount[str(message.author.id)] == 0:
                    LCount[str(message.author.id)] += 1
                    for x in partner:
                        if x == str(message.guild.id):
                            pass
                        else:
                            wid = data[x]["webhook"]
                            channel = client.get_channel(data[x]["channel"])
                            webhook = await client.fetch_webhook(wid)
                            mfile = []
                            for x in message.attachments:
                                mfile.append(await x.to_file())
                            aurl = message.author.display_avatar.url
                            if message.type == discord.MessageType.reply:
                                if message.author.id not in ban["ban_id"]:
                                    print(f"Rep have link, at {client.get_guild(int(x)).name}")
                                    await webhook.send(get_rfmess(message),username=message.author.display_name,avatar_url=aurl,files=mfile)
                            else:
                                if message.author.id not in ban["ban_id"]:
                                    print(f"Norm have link, at {client.get_guild(int(x)).name}")
                                    await webhook.send(message.content,username=message.author.display_name,avatar_url=aurl,files=mfile)
                    await asyncio.sleep(60)
                    LCount[str(message.author.id)] -= LCount[str(message.author.id)]
                elif LCount[str(message.author.id)] > 0 and LCount[str(message.author.id)] < 3:  
                    SpamMsg =  await message.channel.send(content="không được phép spam link đâu biết chưa")
                    LCount[str(message.author.id)] += 1
                    await asyncio.sleep(60)
                    LCount[str(message.author.id)] -= LCount[str(message.author.id)]
                    await SpamMsg.delete()
                elif LCount[str(message.author.id)] >= 3:
                    with open("ban.json", "r") as f:
                        ban = json.load(f)
                    if message.author.id not in ban["ban_id"]:
                        ban["ban_id"].append(message.author.id)
                        with open("ban.json", "w") as f:
                            json.dump(ban, f)
                        rb = requests.get(link+"ban.json",headers=header)
                        shb=rb.json()["sha"]
                        base64SB= base64.b64encode(bytes(json.dumps(ban), "utf-8"))
                        rbjson = {"message":"cf", "content":base64SB.decode("utf-8"),"sha":shb}
                        resB = requests.put(link+"ban.json", data=json.dumps(rbjson), headers=header)
                    await message.channel.send(content=f"Bạn đã bị ban khỏi multiChat vì spam link")
            elif "@everyone" not in message.content and "@here" not in message.content:  
                for x in partner:
                    if x == str(message.guild.id):
                        pass
                    else:
                        wid = data[x]["webhook"]
                        channel = client.get_channel(data[x]["channel"])
                        webhook = await client.fetch_webhook(wid)
                        mfile = []
                        for x in message.attachments:
                            mfile.append(await x.to_file())
                        aurl = message.author.display_avatar.url
                        if message.type == discord.MessageType.reply:
                            if message.author.id not in ban["ban_id"]:
                                print(f"Rep dont have link, at {client.get_guild(int(x)).name}")
                                await webhook.send(get_rfmess(message),username=message.author.display_name,avatar_url=aurl,files=mfile)
                        else:
                            if message.author.id not in ban["ban_id"]:
                                print(f"Norm dont have link, at {client.get_guild(int(x)).name}")
                                await webhook.send(message.content,username=message.author.display_name,avatar_url=aurl,files=mfile)
            elif "@everyone" in message.content or "@here" in message.content:
                await ctx.send("m có tin t ban m khỏi multichat ko, đừng có ping everyone hoặc here")

@client.event
async def on_message_edit(before, after):
    with open("data.json", "r") as f:
        data = json.load(f)
    with open("multichat.json", "r") as f:
        mchat = json.load(f)
    guild = str(before.guild.id)
    if guild in data:
        tcha = data[guild]["channel"]
        room = data[guild]["id"]
        partner = mchat[room]
        mfile = []
        for x in after.attachments:
            mfile.append(await x.to_file())
        if not after.author.bot and after.channel.id == tcha:
            for x in partner:
                if x == str(after.guild.id):
                    pass
                else:
                    channel = client.get_channel(data[x]["channel"])
                    tchannel = client.get_channel(tcha)
                    wid = data[x]["webhook"]
                    twid = data[guild]["webhook"]
                    webhook = await client.fetch_webhook(wid)
                    twebhook = await client.fetch_webhook(twid)
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
    if guild in data:
        tcha = data[guild]["channel"]
        room = data[guild]["id"]
        partner = mchat[room]
        if not msg.author.bot and msg.channel.id == tcha:
            for x in partner:
                if x == str(msg.guild.id):
                    pass
                else:
                    channel = client.get_channel(data[x]["channel"])
                    tchannel = client.get_channel(tcha)
                    wid = data[x]["webhook"]
                    twid = data[guild]["webhook"]
                    webhook = await client.fetch_webhook(wid)
                    twebhook = await client.fetch_webhook(twid)
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

wereComm(client)
                                
token = os.getenv("token")
client.run(token)
