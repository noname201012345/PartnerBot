import discord
from discord.ext import commands
import os
import json
import asyncio
import math
import requests
import base64

rtoken = os.getenv("rtoken")
header = {"Authorization": "Bearer {}".format(rtoken)}
link="https://api.github.com/repos/noname201012345/PartnerBot/contents/"

LCount = {}
def MultiChat(client:discord.Client):
    @client.command()
    async def join(ctx, name):
        if ctx.author.guild_permissions.administrator:
            with open("data.json", "r") as f:
                data = json.load(f)
            with open("multichat.json", "r") as f:
                mchat = json.load(f)
            guild = str(ctx.guild.id)
            await ctx.send("Đang tìm phòng chat...")
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
                                for x in marr:
                                    chan = client.get_channel(data[x]["channel"])
                                    await chan.send(f"**Server:** {ctx.guild.name} vừa tham gia!")
                                marr.append(guild)
                                data[guild] = {}
                                data[guild]["channel"] = ctx.channel.id
                                data[guild]["id"] = name
                                await ctx.send("Tham gia thành công")
                                await ctx.message.delete()
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
        else: 
            await ctx.send("Bạn cần quyền quản lý để dùng lệnh này")

    @client.command()
    async def create(ctx,name):
        if ctx.author.guild_permissions.administrator:
            with open("multichat.json", "r") as f:
                mchat = json.load(f)
            with open("ban.json", "r") as f:
                ban = json.load(f)
            with open("mod.json", "r") as f:
                mod = json.load(f)
            if name in mchat:
                await ctx.send("Phòng chat đã tồn tại!")
            else:
                c=0
                for y in mchat:
                    if str(ctx.guild.id) in mchat[y]:
                        await ctx.send("Hãy rời phòng chat hiện tại để tạo phòng")
                        c=1
                if c==0:
                    mchat[name] = []
                    ban[name] = []
                    mod[name] = []
                    mod[name].append(ctx.author.id)
                    await ctx.send("Tạo phòng chat thành công!")
                    await ctx.send(f"Dùng lệnh **join {name}** để tham gia")
                    with open("multichat.json", "w") as f:
                        json.dump(mchat, f)
                    rm = requests.get(link+"multichat.json",headers=header)
                    shm=rm.json()["sha"]
                    base64M= base64.b64encode(bytes(json.dumps(mchat), "utf-8"))
                    rmjson = {"message":"cf", "content":base64M.decode("utf-8"),"sha":shm}
                    rps = requests.put(link+"multichat.json", data=json.dumps(rmjson), headers=header)
                    
                    rm = requests.get(link+"ban.json",headers=header)
                    shm=rm.json()["sha"]
                    base64M= base64.b64encode(bytes(json.dumps(ban), "utf-8"))
                    rmjson = {"message":"cf", "content":base64M.decode("utf-8"),"sha":shm}
                    rps = requests.put(link+"ban.json", data=json.dumps(rmjson), headers=header)
                    
                    rm = requests.get(link+"mod.json",headers=header)
                    shm=rm.json()["sha"]
                    base64M= base64.b64encode(bytes(json.dumps(mod), "utf-8"))
                    rmjson = {"message":"cf", "content":base64M.decode("utf-8"),"sha":shm}
                    rps = requests.put(link+"mod.json", data=json.dumps(rmjson), headers=header)
        else: 
            await ctx.send("Bạn cần quyền quản lý để dùng lệnh này")
            
    @client.command()
    async def msview(ctx):
        if ctx.author.guild_permissions.administrator:
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
        else: 
            await ctx.send("Bạn cần quyền quản lý để dùng lệnh này")
        
    @client.command()
    async def msban(ctx, id):
        if ctx.author.guild_permissions.administrator:
            with open("ban.json", "r") as f:
                ban = json.load(f)
            with open("mod.json", "r") as f:
                mod = json.load(f)
            with open("data.json", "r") as f:
                data = json.load(f)
            try:
                room = data[str(ctx.guild.id)]["id"]
                if ctx.author.id in mod[room]:
                    ban[str(ctx.guild.id)].append(int(id))
                    with open("ban.json", "w") as f:
                        json.dump(ban, f)
                    await ctx.send(content=f"Đã ban player với id: {id}")
                    r = requests.get(link+"ban.json",headers=header)
                    sh=r.json()["sha"]
                    base64S= base64.b64encode(bytes(json.dumps(ban), "utf-8"))
                    rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
                    response = requests.put(link+"ban.json", data=json.dumps(rjson), headers=header)
                else:
                    await ctx.send("Bạn phải là mod của phòng chat để dùng lệnh này")
            except:
                await ctx.send("Hãy vào phòng chat để dùng lệnh")
        else: 
            await ctx.send("Bạn cần quyền quản lý để dùng lệnh này")
        
    @client.command()
    async def leave(ctx):
        if ctx.author.guild_permissions.administrator:
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
        else: 
            await ctx.send("Bạn cần quyền quản lý để dùng lệnh này")
    
    @client.command()
    async def mod(ctx, member:discord.Member):
        with open("mod.json", "r") as f:
            mod = json.load(f)
        with open("data.json", "r") as f:
            data = json.load(f)
        try:
            room = data[str(ctx.guild.id)]["id"]
            if ctx.author.id in mod[room]:
                mod[room].append(member.id)
                await ctx.send(f"Đã cấp {member} quyền mod!")
                r = requests.get(link+"mod.json",headers=header)
                sh=r.json()["sha"]
                base64S= base64.b64encode(bytes(json.dumps(mod), "utf-8"))
                rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
                response = requests.put(link+"mod.json", data=json.dumps(rjson), headers=header)
            else:
                await ctx.send("Bạn phải là mod của phòng để dùng lệnh")
        except:
            await ctx.send("Tham gia phòng trước khi ")
    
    @client.event
    async def on_message(message:discord.Message):
        await client.process_commands(message)
        with open("multichat.json","r") as f:
            multi = json.load(f)
        with open("data.json","r") as f:
            data = json.load(f)
        with open("ban.json","r") as f:
            banid = json.load(f)
        guild = str(message.guild.id)
        if guild in data:
            tcha = data[guild]["channel"]
            room = data[guild]["id"]
            partner = multi[room]
            ban = banid[room]
            if not message.author.bot and message.channel.id == tcha:
                st = []
                attach = []
                file = []
                img = []
                for x in message.stickers:
                    st.append(await x.fetch())
                for x in st:
                    if x not in client.stickers:
                        st.remove(x)
                for x in message.attachments:
                    attach.append(x)
                if "https://" in message.content and "@everyone" not in message.content and "@here" not in message.content:
                    try:
                        LCount[str(message.author.id)]
                    except:
                        LCount[str(message.author.id)] = 0
                    if LCount[str(message.author.id)] == 0:
                        LCount[str(message.author.id)] += 1
                        for x in partner:
                            file = []
                            img = []
                            if x == str(message.guild.id):
                                pass
                            else:
                                channel = client.get_channel(data[x]["channel"])
                                mess = discord.Embed(description=f"{message.content}",color=message.author.color)
                                if message.content.find(" ") == -1 and message.attachments == []:
                                    if "gif" in message.content:
                                        mess.set_image(url=message.content)
                                        mess.description=""
                                        for y in st:
                                            if y not in client.get_guild(int(x)).stickers:
                                                st.remove(x)
                                        mess.set_footer(text=f"Server: {message.guild.name}",icon_url=f"{message.guild.icon.url}")
                                        mess.set_author(name=f"{message.author.display_name}",icon_url=f"{message.author.display_avatar.url}",url=f"{message.jump_url}")
                                        if message.author.id not in ban:
                                            if message.reference == None:
                                                await channel.send(embed=mess,stickers=st,files=file)
                                            else:
                                                if not message.reference.cached_message.author.bot and message.reference.cached_message.author.id not in ban:
                                                    async for messa in channel.history(after=message.reference.cached_message.created_at):
                                                        if messa.author.bot and messa.author.id == client.user.id:
                                                            if messa.embeds[0].author.url == message.reference.jump_url:
                                                                await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                                break
                                                elif message.reference.cached_message.author.bot and message.reference.cached_message.author.id != client.user.id or message.reference.cached_message.author.id in ban:
                                                    await channel.send(embed=mess,stickers=st,files=file)
                                                    break 
                                                elif message.reference.cached_message.author.bot and message.reference.cached_message.author.id == client.user.id:
                                                    u = message.reference.cached_message.embeds[0].author.url
                                                    tguild = u[29:u.find("/",29)-1]
                                                    if str(x) == str(tguild):
                                                        refer = message.reference.cached_message
                                                        async for messa in channel.history(before=refer.created_at,oldest_first=False):
                                                            if not messa.author.bot:
                                                                if refer.embeds[0].author.url == messa.jump_url:
                                                                    await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                                    break
                                                    else:
                                                        ind = (u.find("/",(u.find("/",29)+2))+1)
                                                        mesid = u[ind:len(u)]
                                                        mes = await client.get_channel(data[str(tguild)]["channel"]).fetch_message(mesid)
                                                        refer = message.reference.cached_message
                                                        async for messa in channel.history(after=mes.created_at):
                                                            if messa.author.bot and messa.author.id == client.user.id:
                                                                if refer.embeds[0].author.url == messa.embeds[0].author.url:
                                                                    await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                                    break
                                    else:
                                        if message.content != "":
                                            mess.title = "Message:"
                                        if len(attach) == 1:
                                            if attach[0].content_type.startswith("image"):
                                                mess.set_image(url=attach[0].url)
                                            else:
                                                file.append(await attach[0].to_file())
                                        elif len(attach) > 1:
                                            for x in attach:
                                                if x == attach[0]:
                                                    if x.content_type.startswith("image"):
                                                        mess.set_image(url=x.url)
                                                    else:
                                                        file.append(await x.to_file())
                                                else:
                                                    if x.content_type.startswith("image"):
                                                        img.append(x)
                                                    else:
                                                        file.append(await x.to_file())
                                        for y in st:
                                                if y not in client.get_guild(int(x)).stickers:
                                                    st.remove(x)
                                        if len(img) > 0:
                                            embeds = []
                                            embeds.append(mess)
                                            for x in img:
                                                e = discord.Embed(color=mess.color)
                                                e.set_image(url=x.url)
                                                embeds.append(e)
                                        mess.set_footer(text=f"Server: {message.guild.name}",icon_url=f"{message.guild.icon.url}")
                                        mess.set_author(name=f"{message.author.display_name}",icon_url=f"{message.author.display_avatar.url}",url=f"{message.jump_url}")
                                        if message.author.id not in ban:
                                            if message.reference == None:
                                                if len(img) > 0:
                                                    await channel.send(embeds=embeds,stickers=st,files=file)
                                                else:
                                                    await channel.send(embed=mess,stickers=st,files=file)
                                            else:
                                                if not message.reference.cached_message.author.bot and message.reference.cached_message.author.id not in ban:
                                                    async for messa in channel.history(after=message.reference.cached_message.created_at):
                                                        if messa.author.bot and messa.author.id == client.user.id:
                                                            if messa.embeds[0].author.url == message.reference.jump_url:
                                                                if len(img) > 0:
                                                                    await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                                else:
                                                                    await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                                break
                                                elif message.reference.cached_message.author.bot and message.reference.cached_message.author.id != client.user.id or message.reference.cached_message.author.id in ban:
                                                    if len(img) > 0:
                                                        await channel.send(embeds=embeds,stickers=st,files=file)
                                                    else:
                                                        await channel.send(embed=mess,stickers=st,files=file)
                                                    break 
                                                elif message.reference.cached_message.author.bot and message.reference.cached_message.author.id == client.user.id:
                                                    u = message.reference.cached_message.embeds[0].author.url
                                                    tguild = u[29:u.find("/",29)-1]
                                                    if str(x) == str(tguild):
                                                        refer = message.reference.cached_message
                                                        async for messa in channel.history(before=refer.created_at,oldest_first=False):
                                                            if not messa.author.bot:
                                                                if refer.embeds[0].author.url == messa.jump_url:
                                                                    if len(img) > 0:
                                                                        await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                                    else:
                                                                        await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                                    break
                                                    else:
                                                        ind = (u.find("/",(u.find("/",29)+2))+1)
                                                        mesid = u[ind:len(u)]
                                                        mes = await client.get_channel(data[str(tguild)]["channel"]).fetch_message(mesid)
                                                        refer = message.reference.cached_message
                                                        async for messa in channel.history(after=mes.created_at):
                                                            if messa.author.bot and messa.author.id == client.user.id:
                                                                if refer.embeds[0].author.url == messa.embeds[0].author.url:
                                                                    if len(img) > 0:
                                                                        await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                                    else:
                                                                        await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                                    break
                                else:
                                    if message.content != "":
                                        mess.title = "Message:"
                                    if len(attach) == 1:
                                        if attach[0].content_type.startswith("image"):
                                            mess.set_image(url=attach[0].url)
                                        else:
                                            file.append(await attach[0].to_file())
                                    elif len(attach) > 1:
                                        for x in attach:
                                            if x == attach[0]:
                                                if x.content_type.startswith("image"):
                                                    mess.set_image(url=x.url)
                                                else:
                                                    file.append(await x.to_file())
                                            else:
                                                if x.content_type.startswith("image"):
                                                    img.append(x)
                                                else:
                                                    file.append(await x.to_file())
                                    for y in st:
                                            if y not in client.get_guild(int(x)).stickers:
                                                st.remove(x)
                                    if len(img) > 0:
                                        embeds = []
                                        embeds.append(mess)
                                        for x in img:
                                            e = discord.Embed(color=mess.color)
                                            e.set_image(url=x.url)
                                            embeds.append(e)
                                    mess.set_footer(text=f"Server: {message.guild.name}",icon_url=f"{message.guild.icon.url}")
                                    mess.set_author(name=f"{message.author.display_name}",icon_url=f"{message.author.display_avatar.url}",url=f"{message.jump_url}")
                                    if message.author.id not in ban:
                                        if message.reference == None:
                                            if len(img) > 0:
                                                await channel.send(embeds=embeds,stickers=st,files=file)
                                            else:
                                                await channel.send(embed=mess,stickers=st,files=file)
                                        else:
                                            if not message.reference.cached_message.author.bot and message.reference.cached_message.author.id not in ban:
                                                async for messa in channel.history(after=message.reference.cached_message.created_at):
                                                    if messa.author.bot and messa.author.id == client.user.id:
                                                        if messa.embeds[0].author.url == message.reference.jump_url:
                                                            if len(img) > 0:
                                                                await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                            else:
                                                                await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                            break
                                            elif message.reference.cached_message.author.bot and message.reference.cached_message.author.id != client.user.id or message.reference.cached_message.author.id in ban:
                                                if len(img) > 0:
                                                    await channel.send(embeds=embeds,stickers=st,files=file)
                                                else:
                                                    await channel.send(embed=mess,stickers=st,files=file)
                                                break 
                                            elif message.reference.cached_message.author.bot and message.reference.cached_message.author.id == client.user.id:
                                                u = message.reference.cached_message.embeds[0].author.url
                                                tguild = u[29:u.find("/",29)-1]
                                                if str(x) == str(tguild):
                                                    refer = message.reference.cached_message
                                                    async for messa in channel.history(before=refer.created_at,oldest_first=False):
                                                        if not messa.author.bot:
                                                            if refer.embeds[0].author.url == messa.jump_url:
                                                                if len(img) > 0:
                                                                    await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                                else:
                                                                    await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                                break
                                                else:
                                                    ind = (u.find("/",(u.find("/",29)+2))+1)
                                                    mesid = u[ind:len(u)]
                                                    mes = await client.get_channel(data[str(tguild)]["channel"]).fetch_message(mesid)
                                                    refer = message.reference.cached_message
                                                    async for messa in channel.history(after=mes.created_at):
                                                        if messa.author.bot and messa.author.id == client.user.id:
                                                            if refer.embeds[0].author.url == messa.embeds[0].author.url:
                                                                if len(img) > 0:
                                                                    await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                                else:
                                                                    await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                                break
                        await asyncio.sleep(30)
                        LCount[str(message.author.id)] -= LCount[str(message.author.id)]
                    elif LCount[str(message.author.id)] > 0 and LCount[str(message.author.id)] < 3:  
                        Msg = await message.channel.send("Do not spam link!")
                        LCount[str(message.author.id)] += 1
                        await asyncio.sleep(30)
                        LCount[str(message.author.id)] -= LCount[str(message.author.id)]
                        await Msg.delete()
                    elif LCount[str(message.author.id)] >= 3:
                        if message.author.id not in ban:
                            ban.append(message.author.id)
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
                        file = []
                        img = []
                        if x == str(message.guild.id):
                            pass
                        else:
                            channel = client.get_channel(data[x]["channel"])
                            mess = discord.Embed(description=f"{message.content}",color=message.author.color,)
                            if message.content != "":
                                mess.title = "Message:"
                            if len(attach) == 1:
                                if attach[0].content_type.startswith("image"):
                                    mess.set_image(url=attach[0].url)
                                else:
                                    file.append(await attach[0].to_file())
                            elif len(attach) > 1:
                                for x in attach:
                                    if x == attach[0]:
                                        if x.content_type.startswith("image"):
                                            mess.set_image(url=x.url)
                                        else:
                                            file.append(await x.to_file())
                                    else:
                                        if x.content_type.startswith("image"):
                                            img.append(x)
                                        else:
                                            file.append(await x.to_file())
                            for y in st:
                                    if y not in client.get_guild(int(x)).stickers:
                                        st.remove(x)
                            if len(img) > 0:
                                embeds = []
                                embeds.append(mess)
                                for x in img:
                                    e = discord.Embed(color=mess.color)
                                    e.set_image(url=x.url)
                                    embeds.append(e)
                            mess.set_footer(text=f"Server: {message.guild.name}",icon_url=f"{message.guild.icon.url}")
                            mess.set_author(name=f"{message.author.display_name}",icon_url=f"{message.author.display_avatar.url}",url=f"{message.jump_url}")
                            if message.author.id not in ban:
                                if message.reference == None:
                                    if len(img) > 0:
                                        await channel.send(embeds=embeds,stickers=st,files=file)
                                    else:
                                        await channel.send(embed=mess,stickers=st,files=file)
                                else:
                                    if not message.reference.cached_message.author.bot and message.reference.cached_message.author.id not in ban:
                                        async for messa in channel.history(after=message.reference.cached_message.created_at):
                                            if messa.author.bot and messa.author.id == client.user.id:
                                                if messa.embeds[0].author.url == message.reference.jump_url:
                                                    if len(img) > 0:
                                                        await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                    else:
                                                        await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                    break
                                    elif message.reference.cached_message.author.bot and message.reference.cached_message.author.id != client.user.id or message.reference.cached_message.author.id in ban:
                                        if len(img) > 0:
                                            await channel.send(embeds=embeds,stickers=st,files=file)
                                        else:
                                            await channel.send(embed=mess,stickers=st,files=file)
                                        break 
                                    elif message.reference.cached_message.author.bot and message.reference.cached_message.author.id == client.user.id:
                                        u = message.reference.cached_message.embeds[0].author.url
                                        tguild = u[29:u.find("/",29)]
                                        if str(x) == str(tguild):
                                            refer = message.reference.cached_message
                                            async for messa in channel.history(before=refer.created_at,oldest_first=False):
                                                if not messa.author.bot:
                                                    if refer.embeds[0].author.url == messa.jump_url:
                                                        if len(img) > 0:
                                                            await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                        else:
                                                            await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                        break
                                        else:
                                            ind = (u.find("/",(u.find("/",29)+2))+1)
                                            mesid = u[ind:len(u)]
                                            mes = await client.get_channel(data[str(tguild)]["channel"]).fetch_message(mesid)
                                            refer = message.reference.cached_message
                                            async for messa in channel.history(after=mes.created_at):
                                                if messa.author.bot and messa.author.id == client.user.id:
                                                    if refer.embeds[0].author.url == messa.embeds[0].author.url:
                                                        if len(img) > 0:
                                                            await channel.send(embeds=embeds,stickers=st,files=file,reference=messa)
                                                        else:
                                                            await channel.send(embed=mess,stickers=st,files=file,reference=messa)
                                                        break
                elif "@everyone" in message.content or "@here" in message.content:
                    await message.delete()
                    await message.channel.send("Ay yo bro, ping what?")

    @client.event
    async def on_message_edit(before, after):
        with open("data.json", "r") as f:
            data = json.load(f)
        with open("multichat.json", "r") as f:
            mchat = json.load(f)
        with open("ban.json", "r") as f:
            ban = json.load(f)
        guild = str(before.guild.id)
        if guild in data:
            tcha = data[guild]["channel"]
            room = data[guild]["id"]
            partner = mchat[room]
            if not after.author.bot and after.channel.id == tcha and after.author.id not in ban[room]:
                attach = []
                file = []
                img = []
                for x in after.attachments:
                    attach.append(x)
                for x in partner:
                    file = []
                    img = []
                    if x == str(after.guild.id):
                        pass
                    else:
                        channel = client.get_channel(data[x]["channel"])
                        mess = discord.Embed(description=f"{after.content}",color=after.author.color,)
                        if after.content != "":
                            mess.title = "Message:"
                        if len(attach) == 1:
                            if attach[0].content_type.startswith("image"):
                                mess.set_image(url=attach[0].url)
                            else:
                                file.append(await attach[0].to_file())
                        elif len(attach) > 1:
                            for x in attach:
                                if x == attach[0]:
                                    if x.content_type.startswith("image"):
                                        mess.set_image(url=x.url)
                                    else:
                                        file.append(await x.to_file())
                                else:
                                    if x.content_type.startswith("image"):
                                        img.append(x)
                                    else:
                                        file.append(await x.to_file())
                        if len(img) > 0:
                            embeds = []
                            embeds.append(mess)
                            for x in img:
                                e = discord.Embed(color=mess.color)
                                e.set_image(url=x.url)
                                embeds.append(e)
                        mess.set_footer(text=f"Server: {after.guild.name}",icon_url=f"{after.guild.icon.url}")
                        mess.set_author(name=f"{after.author.display_name}",icon_url=f"{after.author.display_avatar.url}",url=f"{after.jump_url}")
                        if "https://" in after.content:
                            if after.content.find(" ") == -1 and after.attachments == []:
                                if "gif" in after.content:
                                    mess.set_image(url=after.content)
                                    mess.description=""
                                    mess.title=""
                        async for messa in channel.history(after=before.created_at):
                            if messa.author.bot and messa.author.id == client.user.id:
                                if messa.embeds[0].author.url == before.jump_url:
                                    if len(img) > 0:
                                        await messa.edit(embeds=embeds,attachments=file)
                                        print("test")
                                    else:
                                        await messa.edit(embed=mess,attachments=file)
                                    break
                                
    @client.event
    async def on_message_delete(message):
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
            if not message.author.bot and message.channel.id == tcha and message.author.id not in ban[room]:
                for x in partner:
                    channel = client.get_channel(data[x]["channel"])
                    if x == str(message.guild.id):
                        pass
                    else:
                        async for messa in channel.history(after=message.created_at):
                            if messa.author.bot and messa.author.id == client.user.id:
                                if messa.embeds[0].author.url == message.jump_url:
                                    await messa.delete()
                                    break
                                
