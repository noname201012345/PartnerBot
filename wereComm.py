import discord
from discord.ext import commands
import json
import asyncio
import random
import math
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
   
rtoken = os.getenv("rtoken")
header = {"Authorization": "Bearer {}".format(rtoken)}
link="https://api.github.com/repos/noname201012345/PartnerBot/contents/"
    
def wereComm(client:discord.Client):
    @client.command(aliases=["ms","ww"])
    async def werewolf(ctx, name):
        await ctx.send("Đang tạo phòng ma sói...")
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        guild=str(ctx.guild.id)
        try:
            err = 0
            room = werewolf[guild]["room"]
            for x in room:
                if x["name"] == name:
                    err = 1
                    await ctx.send(f"phòng tên {name} đã tồn tại!")
                elif ctx.author.id in x["playerid"]:
                    err = 1
                    await ctx.send("Vui lòng rời phòng hiện tại để tạo phòng!")
            if err == 0:
                room.append({"name":name})
                room[-1]["playerid"]=[]
                room[-1]["playerid"].append(ctx.author.id)
                room[-1]["lead"]=ctx.author.id
                room[-1]["data"]={}
                room[-1]["data"]["limit"]=12
                room[-1]["data"]["werewolf"]=[]
                room[-1]["data"]["villager"]=[]
                await ctx.send(f"Đã tạo phòng ma sói.\nDùng lệnh **{client.command_prefix}joinww {name}** để tham gia phòng")
        except:
            werewolf[guild] = {}
            werewolf[guild]["room"] = []
            werewolf[guild]["room"].append({"name":name})
            room = werewolf[guild]["room"]
            room[-1]["playerid"]=[]
            room[-1]["playerid"].append(ctx.author.id)
            room[-1]["lead"]=ctx.author.id
            room[-1]["data"]={}
            room[-1]["data"]["limit"]=12
            room[-1]["data"]["werewolf"]=[]
            room[-1]["data"]["villager"]=[]
            await ctx.send(f"Đã tạo phòng ma sói.\nDùng lệnh **{client.command_prefix}joinww {name}** để tham gia phòng")
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    @client.command(aliases=["jms","jww"])
    async def joinww(ctx, name):
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        guild=str(ctx.guild.id)
        try:
            room = werewolf[guild]["room"]
            check = 0
            for x in room:
                if x["name"] == name:
                    check = 1
                    err = 0
                    if ctx.author.id in x["playerid"]:
                        err = 1
                        await ctx.send("bạn đã tham gia phòng này!")
                    if err == 0:
                        if len(x["playerid"]) < int(x["data"]["limit"]):
                            x["playerid"].append(ctx.author.id)
                            await ctx.send("tham gia phòng thành công!")
                        elif len(x["playerid"]) == int(x["data"]["limit"]):
                            await ctx.send("phòng đã đầy!")
            if check == 0:
                await ctx.send("phòng không tồn tại!")
        except:
            werewolf[guild] = {}
            werewolf[guild]["room"] = []
            await ctx.send("không có phòng!")
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    @client.command(aliases=["delms","delww"])
    async def deleteww(ctx):
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        guild = str(ctx.guild.id)
        try:
            room = werewolf[guild]["room"]
            c=0
            notL = 0
            for x in room:
                if x["lead"] == ctx.author.id:
                    room.remove(x)
                    await ctx.send("Xóa thành công!")
                    c=1
                elif ctx.author.id in x["playerid"] and x["lead"] != ctx.author.id:
                    notL = 1
            if c==0 and notL == 0:
                await ctx.send("Bạn chưa tham gia phòng")
            elif notL == 1:
                await ctx.send("Bạn không phải chủ phòng")
        except:
            werewolf[guild] = {}
            werewolf[guild]["room"] = []
            await ctx.send("Bạn chưa tham gia phòng")
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    @client.command(aliases=["leavems","lms","lww"])
    async def leaveww(ctx):
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        guild = str(ctx.guild.id)
        try:
            room = werewolf[guild]["room"]
            c = 0
            for x in room:
                if x["lead"] == ctx.author.id:
                    c = 1
                    await ctx.send("Vui lòng chuyển chủ phòng cho người khác để rời phòng")
                elif ctx.author.id in x["playerid"] and x["lead"] != ctx.author.id:
                    x["playerid"].remove(ctx.author.id)
                    c=1
                    await ctx.send("Rời phòng thành công")
            if c==0:
                await ctx.send("Bạn chưa tham gia phòng")
        except:
            werewolf[guild] = {}
            werewolf[guild]["room"] = []
            await ctx.send("Bạn chưa tham gia phòng")
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    @client.command(aliases=["rms","rww"])
    async def roomww(ctx):
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        guild=str(ctx.guild.id)
        try:
            room = werewolf[guild]["room"]
            if len(room) > 10:
                mpage = math.ceil(len(room)/10)
            else:
                mpage = 1
            page = 1
            emb = discord.Embed(color=0x0049FF,title="Các Phòng Ma Sói Hiện Tại:",description=" ")
            emb.set_footer(text=f"Trang {page}/{mpage}")
            count = 1
            for x in room:
                if count > page*10:
                    break
                rname = x["name"]
                rmem = x["playerid"]
                rmax = x["data"]["limit"]
                emb.add_field(name=f"{room.index(x)+1}, {rname}",value=f"Số người: {len(rmem)}/{rmax}",inline=False)
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
                    rname = x["name"]
                    rmem = x["playerid"]
                    rmax = x["data"]["limit"]
                    emb.add_field(name=f"{room.index(x)+1}, {rname}",value=f"Số người: {len(rmem)}/{rmax}",inline=False)
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
                    rname = x["name"]
                    rmem = x["playerid"]
                    rmax = x["data"]["limit"]
                    emb.add_field(name=f"{room.index(x)+1}, {rname}",value=f"Số người: {len(rmem)}/{rmax}",inline=False)
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
        except:
            werewolf[guild] = {}
            werewolf[guild]["room"] = []
            emb = discord.Embed(color=0x0049FF,title="Các Phòng Ma Sói Hiện Tại:",description=" ")
            emb.set_footer(text=f"Trang 1/1")
            await ctx.send(embed=emb)
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    @client.command(aliases=["sms","sww"])
    async def setupww(ctx):
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        with open("role_data.json","r") as f:
            role = json.load(f)
        guild=str(ctx.guild.id)
        room = werewolf[guild]["room"]
        c=0
        notL = 0
        for x in room:
            if x["lead"] == ctx.author.id:
                rname=x["name"]
                async def wwCallback(interaction):
                    vw = discord.ui.View(timeout=None)
                    selM = discord.ui.Select(max_values=1,placeholder="Select One",options=[discord.SelectOption(label="Sói Thường",value="Sói Thường",description="Ma sói không chức năng"),discord.SelectOption(label="Sói Nguyền",value="Sói Nguyền",description="Có thể biến 1 dân làng thành sói"),discord.SelectOption(label="Sói Con",value="Sói Con",description="Sói có thể giết 2 người 1 đêm khi sói con chết"),discord.SelectOption(label="Sói Gây Mê",value="Sói Gây Mê",description="Có thể gây mê một người")])
                    async def selMCallback(interaction):
                        await interaction.response.defer()
                    async def addCallback(interaction):
                        if (len(x["data"]["werewolf"]) + len(x["data"]["villager"])) < len(x["playerid"]):
                            x["data"]["werewolf"].append(selM.values[0])
                            with open("werewolf.json", "w") as f:
                                json.dump(werewolf,f)
                            emb.clear_fields()
                            for y in x["data"]["werewolf"]:
                                value = role[y]
                                emb.add_field(name=f"{y}",value=value)
                            await interaction.response.edit_message(embed=emb)
                        else:
                            await interaction.response.send_message(content="Phòng đã đủ chức năng",ephemeral=True)
                    async def rmCallback(interaction):
                        if selM.values[0] in x["data"]["werewolf"]:
                            x["data"]["werewolf"].remove(selM.values[0])
                            with open("werewolf.json", "w") as f:
                                json.dump(werewolf,f)
                            emb.clear_fields()
                            for y in x["data"]["werewolf"]:
                                value = role[y]
                                emb.add_field(name=f"{y}",value=value)
                            await interaction.response.edit_message(embed=emb)
                        else:
                            await interaction.response.send_message(content="Phòng không có role này",ephemeral=True)
                    async def backCallback(interaction):
                        emb = discord.Embed(color=0x0049FF,title=f":gear: Setting Phòng {rname}:",description=f"\n")
                        now=len(x["playerid"])
                        max=x["data"]["limit"]
                        emb.add_field(name=f"Số người: {now}/{max}",value="|",inline=False)
                        if x["data"]["villager"] != []:
                            villager=x["data"]["villager"][0]
                        else:
                            villager="Không có"
                        i=0
                        for y in x["data"]["villager"]:
                            if i==0:
                                i+=1
                            else:
                                villager += ", "
                                villager += y
                        emb.add_field(name=f"Dân Làng: ",value=f"{villager}",inline=False)
                        if x["data"]["werewolf"] != []:
                            wolf=x["data"]["werewolf"][0]
                        else:
                            wolf="Không có"
                        i=0
                        for y in x["data"]["werewolf"]:
                            if i==0:
                                i+=1
                            else:
                                wolf += ", "
                                wolf += y
                        emb.add_field(name="Ma Sói: ",value=f"{wolf}",inline=False)
                        await interaction.response.edit_message(embed=emb,view=vi)
                    addB = discord.ui.Button(label="Add",style=discord.ButtonStyle.blurple)
                    rmB = discord.ui.Button(label="Remove",style=discord.ButtonStyle.blurple)
                    backB = discord.ui.Button(label="Back",style=discord.ButtonStyle.blurple)

                    selM.callback = selMCallback
                    addB.callback = addCallback
                    rmB.callback = rmCallback
                    backB.callback = backCallback

                    vw.add_item(selM)
                    vw.add_item(addB)
                    vw.add_item(rmB)
                    vw.add_item(backB)
                    emb.title="Role Ma sói:"
                    emb.clear_fields()
                    for y in x["data"]["werewolf"]:
                        value = role[y]
                        emb.add_field(name=f"{y}",value=value)
                    await interaction.response.edit_message(embed=emb,view=vw)
                async def vlCallback(interaction):
                    vw = discord.ui.View(timeout=None)
                    selM = discord.ui.Select(max_values=1,placeholder="Select One",options=[discord.SelectOption(label="Dân Thường",value="Dân Thường",description="Dân làng không chức năng"),discord.SelectOption(label="Bảo Vệ",value="Bảo Vệ",description="Có thể bảo vệ 1 người mỗi tối"),discord.SelectOption(label="Tiên Tri",value="Tiên Tri",description="Mỗi đêm kiểm tra chức năng một người"),discord.SelectOption(label="Thợ Săn",value="Thợ Săn",description="Kéo theo một người chết cùng"),discord.SelectOption(label="Phù Thủy",value="Phù Thủy",description="Có một bình thuốc giết người và một bình cứu người"),discord.SelectOption(label="Cupid",value="Cupid",description="Khiến 2 người yêu nhau")])
                    async def selMCallback(interaction):
                        await interaction.response.defer()
                    async def addCallback(interaction):
                        if (len(x["data"]["werewolf"]) + len(x["data"]["villager"])) < len(x["playerid"]):
                            x["data"]["villager"].append(selM.values[0])
                            with open("werewolf.json", "w") as f:
                                json.dump(werewolf,f)
                            emb.clear_fields()
                            for y in x["data"]["villager"]:
                                value = role[y]
                                emb.add_field(name=f"{y}",value=value)
                            await interaction.response.edit_message(embed=emb)
                        else:
                            await interaction.response.send_message(content="Phòng đã đủ chức năng",ephemeral=True)
                    async def rmCallback(interaction):
                        if selM.values[0] in x["data"]["villager"]:
                            x["data"]["villager"].remove(selM.values[0])
                            with open("werewolf.json", "w") as f:
                                json.dump(werewolf,f)
                            emb.clear_fields()
                            for y in x["data"]["villager"]:
                                value = role[y]
                                emb.add_field(name=f"{y}",value=value)
                            await interaction.response.edit_message(embed=emb)
                        else:
                            await interaction.response.send_message(content="Phòng không có role này",ephemeral=True)
                    async def backCallback(interaction):
                        emb = discord.Embed(color=0x0049FF,title=f":gear: Setting Phòng {rname}:",description=f"\n")
                        now=len(x["playerid"])
                        max=x["data"]["limit"]
                        emb.add_field(name=f"Số người: {now}/{max}",value="|",inline=False)
                        if x["data"]["villager"] != []:
                            villager=x["data"]["villager"][0]
                        else:
                            villager="Không có"
                        i=0
                        for y in x["data"]["villager"]:
                            if i==0:
                                i+=1
                            else:
                                villager += ", "
                                villager += y
                        emb.add_field(name=f"Dân Làng: ",value=f"{villager}",inline=False)
                        if x["data"]["werewolf"] != []:
                            wolf=x["data"]["werewolf"][0]
                        else:
                            wolf="Không có"
                        i=0
                        for y in x["data"]["werewolf"]:
                            if i==0:
                                i+=1
                            else:
                                wolf += ", "
                                wolf += y
                        emb.add_field(name="Ma Sói: ",value=f"{wolf}",inline=False)
                        await interaction.response.edit_message(embed=emb,view=vi)
                    addB = discord.ui.Button(label="Add",style=discord.ButtonStyle.blurple)
                    rmB = discord.ui.Button(label="Remove",style=discord.ButtonStyle.blurple)
                    backB = discord.ui.Button(label="Back",style=discord.ButtonStyle.blurple)

                    selM.callback = selMCallback
                    addB.callback = addCallback
                    rmB.callback = rmCallback
                    backB.callback = backCallback

                    vw.add_item(selM)
                    vw.add_item(addB)
                    vw.add_item(rmB)
                    vw.add_item(backB)
                    emb.title="Role Dân Làng:"
                    emb.clear_fields()
                    for y in x["data"]["villager"]:
                        value = role[y]
                        emb.add_field(name=f"{y}",value=value)
                    await interaction.response.edit_message(embed=emb,view=vw)
                async def MemCallback(interaction):
                    if (len(x["data"]["werewolf"]) + len(x["data"]["villager"])) <= int(Mem.values[0]):
                        x["data"]["limit"] = Mem.values[0]
                        with open("werewolf.json", "w") as f:
                            json.dump(werewolf,f)
                        emb = discord.Embed(color=0x0049FF,title=f":gear: Setting Phòng {rname}:",description=f"\n")
                        now=len(x["playerid"])
                        max=x["data"]["limit"]
                        emb.add_field(name=f"Số người: {now}/{max}",value="|",inline=False)
                        if x["data"]["villager"] != []:
                            villager=x["data"]["villager"][0]
                        else:
                            villager="Không có"
                        i=0
                        for y in x["data"]["villager"]:
                            if i==0:
                                i+=1
                            else:
                                villager += ", "
                                villager += y
                        emb.add_field(name=f"Dân Làng: ",value=f"{villager}",inline=False)
                        if x["data"]["werewolf"] != []:
                            wolf=x["data"]["werewolf"][0]
                        else:
                            wolf="Không có"
                        i=0
                        for y in x["data"]["werewolf"]:
                            if i==0:
                                i+=1
                            else:
                                wolf += ", "
                                wolf += y
                        emb.add_field(name="Ma Sói: ",value=f"{wolf}",inline=False)
                        await interaction.response.edit_message(embed=emb,view=vi)
                    else:
                        await interaction.response.send_message(content="Số người không được phép bé hơn số chức năng",ephemeral=True)
                Mem = discord.ui.Select(max_values=1,placeholder="Chọn số người",options=[discord.SelectOption(label="12",value=12),discord.SelectOption(label="16",value=16),discord.SelectOption(label="10",value=10)])
                wwB = discord.ui.Button(label="Werewolf",style=discord.ButtonStyle.blurple)
                vlB = discord.ui.Button(label="Villager",style=discord.ButtonStyle.blurple)
                wwB.callback=wwCallback
                vlB.callback=vlCallback
                Mem.callback=MemCallback
                vi = discord.ui.View(timeout=None)
                vi.add_item(Mem)
                vi.add_item(wwB)
                vi.add_item(vlB)
                emb = discord.Embed(color=0x0049FF,title=f":gear: Setting Phòng {rname}:")
                now=len(x["playerid"])
                max=x["data"]["limit"]
                emb.description = f"**Số người:** {now}/{max}"
                if x["data"]["villager"] != []:
                    villager=x["data"]["villager"][0]
                else:
                    villager="Không có"
                i=0
                for y in x["data"]["villager"]:
                    if i==0:
                        i+=1
                    else:
                        villager += ", "
                        villager += y
                emb.add_field(name=f"Dân Làng: ",value=f"{villager}",inline=False)
                if x["data"]["werewolf"] != []:
                    wolf=x["data"]["werewolf"][0]
                else:
                    wolf="Không có"
                i=0
                for y in x["data"]["werewolf"]:
                    if i==0:
                        i+=1
                    else:
                        wolf += ", "
                        wolf += y
                emb.add_field(name="Ma Sói: ",value=f"{wolf}",inline=False)
                c=1
                await ctx.send(embed=emb,view=vi)
            elif ctx.author.id in x["playerid"] and x["lead"] != ctx.author.id:
                notL = 1
        if c==0 and notL == 0:
            await ctx.send("Bạn chưa tham gia phòng")
        elif notL == 1:
            await ctx.send("Bạn không phải chủ phòng")
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    @client.command(aliases=["msc","wwc"])
    @commands.has_guild_permissions(administrator=True)
    async def wwcreate(ctx):
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        guild=str(ctx.guild.id)
        try:
            if werewolf[guild]["category"] != None:
                cemb = discord.Embed(color=0xC10000,title="Category đã tồn tại, bạn có chắc chắn muốn tạo mới?")
                vw = discord.ui.View(timeout=180)
                async def yesCallback(interaction):
                    WWCr = await ctx.guild.create_category(name="WereWolf Category")
                    werewolf[guild]["category"]=WWCr.id
                    await interaction.response.send_message(content="Tạo thành công",ephemeral=True)
                    with open("werewolf.json", "w") as f:
                        json.dump(werewolf,f)
                async def noCallback(interaction):
                    await interaction.response.defer()
                yesB=discord.ui.Button(label="Yes",style=discord.ButtonStyle.blurple)
                noB=discord.ui.Button(label="No",style=discord.ButtonStyle.blurple)
                yesB.callback=yesCallback
                noB.callback=noCallback
                vw.add_item(yesB)
                vw.add_item(noB)
                await ctx.send(embed=cemb,view=vw)
        except:
            WWCr = await ctx.guild.create_category(name="WereWolf Category")
            werewolf[guild]["category"]=WWCr.id
            await ctx.send(content="Tạo thành công")
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    @client.command(aliases=["mss","wws"])
    async def wwstart(ctx):
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        guild = str(ctx.guild.id)
        try:
            room = werewolf[guild]["room"]
            c=0
            notL = 0
            for x in room:
                if x["lead"] == ctx.author.id:
                    play = x["playerid"]
                    x["role"] = {}
                    role = x["role"]
                    rname = x["name"]
                    embed = discord.Embed(title="Nhấn Nút Bên Dưới Để Sẵn Sàng",color=0x0049FF,description=f"Tên Phòng: **{rname}**\nSẵn Sàng: **{len(role)}/{len(play)}**")
                    view = discord.ui.View(timeout=None)
                    async def ssCallback(interaction):
                        x["role"][str(interaction.user.id)] = None
                        rname = x["name"]
                        embed = discord.Embed(color=0x0049FF,title="Nhấn Nút Bên Dưới Để Sẵn Sàng",description=f"Tên Phòng: **{rname}**\nSẵn Sàng: **{len(role)}/{len(play)}**")
                        if len(role) == len(play):
                            ssButton.disabled = True
                            await interaction.response.edit_message(embed=embed,view=view)
                            category = client.get_channel(werewolf[guild]["category"])
                            rname = x["name"]
                            vlover = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                            wwover = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                            voiceover = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                            player = x["playerid"].copy()
                            x["role"] = {}
                            for y in x["data"]["werewolf"]:
                                p = random.choice(player)
                                x["role"][(str)(p)] = y
                                user = client.get_user(p)
                                wwover[user] = discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
                                vlover[user] = discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
                                voiceover[user] = discord.PermissionOverwrite(speak = True, connect = True, view_channel=True)
                                DMChan = await user.create_dm()
                                DMembed = discord.Embed(title=f"Phòng Ma Sói: {rname}",description=f"Bạn là **{y}**",color=0xFFB600)
                                DMembed.set_footer(text=f"Server: {ctx.guild.name}",icon_url=ctx.guild.icon.url)
                                await DMChan.send(embed=DMembed)
                                player.remove(p)
                            for y in x["data"]["villager"]:
                                p = random.choice(player)
                                x["role"][(str)(p)] = y
                                user = client.get_user(p)
                                vlover[user] = discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
                                voiceover[user] = discord.PermissionOverwrite(speak = True, connect = True, view_channel=True)
                                DMChan = await user.create_dm()
                                DMembed = discord.Embed(title=f"Phòng Ma Sói: {rname}",description=f"Bạn là **{y}**",color=0xFFB600)
                                DMembed.set_footer(text=f"Server: {ctx.guild.name}",icon_url=ctx.guild.icon.url)
                                await DMChan.send(embed=DMembed)
                                player.remove(p)
                            vlroom = await category.create_text_channel(f"Dân Làng┃{rname}",overwrites=vlover)
                            wwroom = await category.create_text_channel(f"Ma Sói┃{rname}",overwrites=wwover)
                            wwvoice = await category.create_voice_channel(f"Voice: {rname}",overwrites=voiceover)
                            x["wwroom"] = wwroom.id
                            x["vlroom"] = vlroom.id
                            x["voice"] = wwvoice.id
                            x["alive"] = {}
                            x["NoVote"] = []
                            x["dead"] = []
                            for y in x["playerid"]:
                                x["alive"][str(y)] = []
                            with open("werewolf.json", "w") as f:
                                json.dump(werewolf,f)
                            await runGame(ctx, x, werewolf)
                        else:
                            await interaction.response.edit_message(embed=embed)
                    ssButton = discord.ui.Button(label="✅",style=discord.ButtonStyle.green)
                    ssButton.callback=ssCallback
                    view.add_item(ssButton)
                    await ctx.send(embed=embed,view=view)
                    c=1
                elif ctx.author.id in x["playerid"] and x["lead"] != ctx.author.id:
                    notL = 1
            if c==0 and notL == 0:
                await ctx.send("Bạn chưa tham gia phòng")
            elif notL == 1:
                await ctx.send("Bạn không phải chủ phòng")
        except:
            werewolf[guild] = {}
            werewolf[guild]["room"] = []
            await ctx.send("Bạn chưa tham gia phòng")
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    @client.command(aliases=["leadms"])
    async def leadww(ctx, member: discord.Member):
        with open("werewolf.json","r") as f:
            werewolf = json.load(f)
        guild = str(ctx.guild.id)
        try:
            room = werewolf[guild]["room"]
            c=0
            notL = 0
            for x in room:
                if x["lead"] == ctx.author.id:
                    if member.id in x["playerid"]:
                        x["lead"] = member.id
                        await ctx.send(f"Đã chuyển chủ phòng cho {member}")
                    else:
                        await ctx.send(f"{member} không có trong phòng")
                    c=1
                elif ctx.author.id in x["playerid"] and x["lead"] != ctx.author.id:
                    notL = 1
            if c==0 and notL == 0:
                await ctx.send("Bạn chưa tham gia phòng")
            elif notL == 1:
                await ctx.send("Bạn không phải chủ phòng")
        except:
            werewolf[guild] = {}
            werewolf[guild]["room"] = []
            await ctx.send("Bạn chưa tham gia phòng")
        with open("werewolf.json", "w") as f:
            json.dump(werewolf,f)
        r = requests.get(link+"werewolf.json",headers=header)
        sh=r.json()["sha"]
        base64S= base64.b64encode(bytes(json.dumps(werewolf), "utf-8"))
        rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
        response = requests.put(link+"werewolf.json", data=json.dumps(rjson), headers=header)

    async def runGame(ctx, game, werewolf):
        guild = ctx.guild.id
        vilRoom = client.get_channel(game["vlroom"])
        wereRoom = client.get_channel(game["wwroom"])
        Voice = client.get_channel(game["voice"])
        Night = 0
        TSd={}
        TSd["selfDead"] = None
        WitchDead = {}
        Curse = {}
        GMe = {}
        GMe["Night"] = None
        GMe["Mem"] = None
        GMe["OnMute"] = None
        #loop from here
        while True:
            data = game["data"]
            if "Cupid" in data["villager"] and len(game["alive"]) == 2 and Night != 0:
                if game["Link"] != []:
                    if game["Link"][0] in game["alive"] and game["Link"][1] in game["alive"]:
                        rname = game["name"]
                        p1 = ctx.guild.get_member(int(game["Link"][0]))
                        p2 = ctx.guild.get_member(int(game["Link"][1]))
                        WinEmbed = discord.Embed(title="Chúc Mừng Cặp Đôi Chiến Thắng!!",description=f"**Tên Phòng:** {rname}\n**Người Thắng:** {p1.name}, {p2.name}\n**Số Đêm:** {Night}",color=0xFFFFFF)
                        WinEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                        await ctx.send(embed=WinEmbed)
                        await vilRoom.delete()
                        await wereRoom.delete()
                        await Voice.delete()
                        werewolf[str(guild)]["room"].remove(game)
                        with open("werewolf.json","w") as f:
                            json.dump(werewolf,f)
                        break
            wolfCount = 0
            vilCount = 0
            for x in game["alive"]:
                if game["role"][x] in game["data"]["werewolf"]:
                    wolfCount += 1
                elif game["role"][x] in game["data"]["villager"]:
                    vilCount += 1
            if wolfCount == 0 and vilCount != 0:
                rname = game["name"]
                WinEmbed = discord.Embed(title="Chúc Mừng Dân Làng Chiến Thắng!!",color=0xFFFFFF)
                WinDes=f"**Tên Phòng:** {rname}\n**Người Thắng:** "
                for x in game["alive"]:
                    p = ctx.guild.get_member(int(x))
                    WinDes += f"{p.name} "
                WinDes += f"\n**Số Đêm:** {Night}"
                WinEmbed.description = WinDes
                WinEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                await ctx.send(embed=WinEmbed)
                await vilRoom.delete()
                await wereRoom.delete()
                await Voice.delete()
                werewolf[str(guild)]["room"].remove(game)
                with open("werewolf.json","w") as f:
                    json.dump(werewolf,f)
                break
            elif wolfCount != 0 and vilCount == 0:
                rname = game["name"]
                WinEmbed = discord.Embed(title="Chúc Mừng Ma Sói Chiến Thắng!!",color=0xFFFFFF)
                WinDes=f"**Tên Phòng:** {rname}\n**Người Thắng:** "
                for x in game["alive"]:
                    p = ctx.guild.get_member(int(x))
                    WinDes += f"{p.name} "
                WinDes += f"\n**Số Đêm:** {Night}"
                WinEmbed.description = WinDes
                WinEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                await ctx.send(embed=WinEmbed)
                await vilRoom.delete()
                await wereRoom.delete()
                await Voice.delete()
                werewolf[str(guild)]["room"].remove(game)
                with open("werewolf.json","w") as f:
                    json.dump(werewolf,f)
                break
            elif wolfCount == 0 and vilCount == 0:
                rname = game["name"]
                WinEmbed = discord.Embed(title="Hòa Nhau, Không Có Người Thắng!!",color=0xFFFFFF)
                WinDes=f"**Tên Phòng:** {rname}\n**Số Đêm:** {Night}"
                WinEmbed.description = WinDes
                WinEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                await ctx.send(embed=WinEmbed)
                await vilRoom.delete()
                await wereRoom.delete()
                await Voice.delete()
                werewolf[str(guild)]["room"].remove(game)
                with open("werewolf.json","w") as f:
                    json.dump(werewolf,f)
                break
            for x in game["alive"]:
                game["alive"][x] = []
            game["NoVote"] = []
            if "Thợ Săn" in data["villager"] and TSd["selfDead"] == 1:
                timer = 15
                TSd["dead"] = None
                TSEmbed = discord.Embed(color=0xFF0000,title=f"Thợ Săn đã chết!! ({timer}/15)",description="Hãy kéo theo một người chết chung")
                TSView = discord.ui.View(timeout=None)
                async def TSShotCall(interaction:discord.Interaction):
                    if game["role"][str(interaction.user.id)] == "Thợ Săn":
                        TSd["dead"] = int(TSShot.values[0])
                        p2 = ctx.guild.get_member(TSd["dead"])
                        game["alive"].pop(str(TSShot.values[0]))
                        game["dead"].append(str(TSShot.values[0]))
                        await vilRoom.set_permissions(p2,send_messages=False,view_channel=True)
                        await wereRoom.set_permissions(p2,send_messages=False,view_channel=True)
                        await Voice.set_permissions(p2,speak = False,view_channel=True)
                        await interaction.response.send_message(content=f"Bạn đã kéo theo {p2.name} chết chung",ephemeral=True)
                    else:
                        await interaction.response.send_message(content="Bạn không phải Thợ Săn",ephemeral=True)
                TSShot = discord.ui.Select(placeholder="Chọn người chết chung")
                TSShot.callback = TSShotCall
                for y in game["alive"]:
                    if y != max:
                        py = ctx.guild.get_member(int(y))
                        TSShot.add_option(label=f"{py.name}",value=py.id)
                TSView.add_item(TSShot)
                TSMsg = await vilRoom.send(embed=TSEmbed,view=TSView)
                while timer > 0 and TSd["dead"] == None:
                    await asyncio.sleep(1)
                    timer -= 1
                    TSEmbed.title = f"Thợ Săn đã chết!! ({timer}/15)"
                    await TSMsg.edit(embed=TSEmbed)
                TSShot.disabled = True
                await TSMsg.edit(view=TSView)
                TSd["selfDead"] == None
            if "Sói Gây Mê" in data["werewolf"]:
                if GMe["OnMute"] != None:
                    p = client.get_guild(guild).get_member(int(GMe["OnMute"]))
                    await vilRoom.set_permissions(target=p,send_messages=True,view_channel=True)    
                    await Voice.set_permissions(target=p,speak = True,view_channel=True)
                    GMe["OnMute"] = None
                if GMe["Night"] == Night and GMe["Mem"] != None:
                    p = client.get_guild(guild).get_member(int(GMe["Mem"]))
                    await vilRoom.set_permissions(target=p,send_messages=False,view_channel=True)    
                    await Voice.set_permissions(target=p,speak = False,view_channel=True)
                    GMe["OnMute"] = GMe["Mem"]
            for x in game["dead"]:
                p = client.get_guild(guild).get_member(int(x))
                await vilRoom.set_permissions(target=p,send_messages=False,view_channel=True)
                await wereRoom.set_permissions(target=p,send_messages=False,view_channel=True)
                await Voice.set_permissions(target=p,speak = False,view_channel=True)
            timer = 150
            voteEmbed = discord.Embed(title=":sunny:Trời Sáng, Vote Người Bị Treo Cổ",description=f"**Thời Gian**: {timer}/150",color=0x0049FF)
            voteEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
            NightEmbed = discord.Embed(title=":crescent_moon:Trời Tối, Tất Cả Mọi Người Đi Ngủ", color=0xffbb00)
            NightEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
            NightEmbed.set_image(url="https://c.tenor.com/MFN5yK3lKusAAAAC/anime-sleep.gif")
            view = discord.ui.View(timeout=180)
            option = []
            for x in game["alive"]:
                player = client.get_guild(guild).get_member(int(x))
                vote = len(game["alive"][x])
                voteEmbed.add_field(name=f"{player.name}",value=f"{vote} Vote",inline=True)
                option.append(discord.SelectOption(label=f"{player.name}",value=f"{player.id}"))
            SelPlayer = discord.ui.Select(options=option,placeholder="Chọn Người Chơi",max_values=1)
            VoteButton = discord.ui.Button(label="Vote",style=discord.ButtonStyle.green)
            UnVoteButton = discord.ui.Button(label="UnVote",style=discord.ButtonStyle.red)
            NoVoteButton = discord.ui.Button(label="Bỏ Vote",style=discord.ButtonStyle.blurple)
            async def SelCallback(interaction: discord.Interaction):
                await interaction.response.defer()
            async def VoteCallback(interaction: discord.Interaction):
                if timer > 0:
                    if interaction.user.id not in game["alive"][str(SelPlayer.values[0])] and interaction.user.id not in game["NoVote"]:
                        for y in game["alive"]:
                            if y == str(SelPlayer.values[0]):
                                game["alive"][y].append(interaction.user.id)
                                voteEmbed.clear_fields()
                                for x in game["alive"]:
                                    player = client.get_guild(guild).get_member(int(x))
                                    vote = len(game["alive"][x])
                                    voteEmbed.add_field(name=f"{player.name}",value=f"{vote} Vote",inline=True)
                                with open("werewolf.json","w") as f:
                                    json.dump(werewolf,f)
                                await interaction.response.edit_message(embed=voteEmbed)
                            elif interaction.user.id in game["alive"][y]:
                                game["alive"][y].remove(interaction.user.id)
                                game["alive"][str(SelPlayer.values[0])].append(interaction.user.id)
                                voteEmbed.clear_fields()
                                for x in game["alive"]:
                                    player = client.get_guild(guild).get_member(int(x))
                                    vote = len(game["alive"][x])
                                    voteEmbed.add_field(name=f"{player.name}",value=f"{vote} Vote",inline=True)
                                with open("werewolf.json","w") as f:
                                    json.dump(werewolf,f)
                                await interaction.response.edit_message(embed=voteEmbed)
                    elif interaction.user.id in game["NoVote"]:
                        game["NoVote"].remove(interaction.user.id)
                        game["alive"][str(SelPlayer.values[0])].append(interaction.user.id)
                        voteEmbed.clear_fields()
                        for x in game["alive"]:
                            player = client.get_guild(guild).get_member(int(x))
                            vote = len(game["alive"][x])
                            voteEmbed.add_field(name=f"{player.name}",value=f"{vote} Vote",inline=True)
                        with open("werewolf.json","w") as f:
                            json.dump(werewolf,f)
                        await interaction.response.edit_message(embed=voteEmbed)
                    else:
                        await interaction.response.send_message(content="Bạn đã vote người này trước đó",ephemeral=True)
                else:
                    await interaction.response.defer()
            async def UnVoteCallback(interaction: discord.Interaction):
                if timer > 0:
                    if interaction.user.id in game["alive"][str(SelPlayer.values[0])]:
                        game["alive"][str(SelPlayer.values[0])].remove(interaction.user.id)
                        voteEmbed.clear_fields()
                        for x in game["alive"]:
                            player = client.get_guild(guild).get_member(int(x))
                            vote = len(game["alive"][x])
                            voteEmbed.add_field(name=f"{player.name}",value=f"{vote} Vote",inline=True)
                        with open("werewolf.json","w") as f:
                            json.dump(werewolf,f)
                        await interaction.response.edit_message(embed=voteEmbed)
                    else:
                        await interaction.response.send_message(content="Bạn chưa vote người này",ephemeral=True)
                else:
                    await interaction.response.defer()
            async def NoVoteCallback(interaction: discord.Interaction):
                if timer > 0:
                    if interaction.user.id in game["NoVote"]:
                        await interaction.response.send_message(content="Bạn đã bỏ vote từ trước",ephemeral=True)
                    else:
                        c=0
                        for y in game["alive"]:
                            if interaction.user.id in game["alive"][y]:
                                game["alive"][y].remove(interaction.user.id)
                                game["NoVote"].append(interaction.user.id)
                                voteEmbed.clear_fields()
                                for x in game["alive"]:
                                    player = client.get_guild(guild).get_member(int(x))
                                    vote = len(game["alive"][x])
                                    voteEmbed.add_field(name=f"{player.name}",value=f"{vote} Vote",inline=True)
                                with open("werewolf.json","w") as f:
                                    json.dump(werewolf,f)
                                await VoteMsg.edit(embed=voteEmbed)
                                await interaction.response.send_message(content="Bỏ vote thành công",ephemeral=True)
                                c+=1
                        if c==0:
                            game["NoVote"].append(interaction.user.id)
                            with open("werewolf.json","w") as f:
                                json.dump(werewolf,f)
                            await interaction.response.send_message(content="Bỏ vote thành công",ephemeral=True)
                else:
                    await interaction.response.defer()
            SelPlayer.callback = SelCallback
            VoteButton.callback = VoteCallback
            UnVoteButton.callback = UnVoteCallback
            NoVoteButton.callback = NoVoteCallback
            view.add_item(SelPlayer)
            view.add_item(VoteButton)
            view.add_item(UnVoteButton)
            view.add_item(NoVoteButton)
            VoteMsg = await vilRoom.send(embed=voteEmbed,view=view)
            with open("werewolf.json","w") as f:
                json.dump(werewolf,f)
            voteCount = 0
            for y in game["alive"]:
                voteCount += len(game["alive"][y])
            voteCount += len(game["NoVote"])
            while timer > 0 and voteCount != len(game["alive"]):
                await asyncio.sleep(1)
                timer -= 1
                voteEmbed.description = f"**Thời Gian**: {timer}/150"
                await VoteMsg.edit(embed=voteEmbed,view=view)
                voteCount = 0
                for y in game["alive"]:
                    voteCount += len(game["alive"][y])
                voteCount += len(game["NoVote"])
            count = 0
            max = None
            for x in game["alive"]:
                if count == 0 and len(game["alive"][x]) > 0:
                    max = x
                    count=-1
                elif len(game["alive"][x]) > 0 and count != 0:
                    if len(game["alive"][max]) < len(game["alive"][x]):
                        max = x
                    elif len(game["alive"][max]) == len(game["alive"][x]): 
                        count = len(game["alive"][x])
            SelPlayer.disabled = True
            VoteButton.disabled = True
            UnVoteButton.disabled = True
            NoVoteButton.disabled = True
            await VoteMsg.edit(view=view)
            await asyncio.sleep(1)
            if "Thợ Săn" in data["villager"]:
                if max != None:
                    if len(game["alive"][max]) != count:
                        if game["role"][max] != "Thợ Săn":
                            game["alive"].pop(max)
                            game["dead"].append(max)
                            p = client.get_guild(guild).get_member(int(max))
                            await vilRoom.set_permissions(p,send_messages=False,view_channel=True)
                            await wereRoom.set_permissions(p,send_messages=False,view_channel=True)
                            await Voice.set_permissions(p,speak = False,view_channel=True)
                        elif game["role"][max] == "Thợ Săn":
                            timer = 15
                            TSd["dead"] = None
                            TSEmbed = discord.Embed(color=0xFF0000,title=f"Thợ Săn đã chết!! ({timer}/15)",description="Hãy kéo theo một người chết chung")
                            TSView = discord.ui.View(timeout=None)
                            async def TSShotCall(interaction:discord.Interaction):
                                if str(interaction.user.id) in game["alive"]:
                                    if game["role"][str(interaction.user.id)] == "Thợ Săn":
                                        TSd["dead"] = int(TSShot.values[0])
                                        p2 = ctx.guild.get_member(TSd["dead"])
                                        game["alive"].pop(str(TSShot.values[0]))
                                        game["dead"].append(str(TSShot.values[0]))
                                        await vilRoom.set_permissions(p2,send_messages=False,view_channel=True)
                                        await wereRoom.set_permissions(p2,send_messages=False,view_channel=True)
                                        await Voice.set_permissions(p2,speak = False,view_channel=True)
                                        await interaction.response.send_message(content=f"Bạn đã kéo theo {p2.name} chết chung",ephemeral=True)
                                    else:
                                        await interaction.response.send_message(content="Bạn không phải Thợ Săn",ephemeral=True)
                                else:
                                    await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                            TSShot = discord.ui.Select(placeholder="Chọn người chết chung")
                            TSShot.callback = TSShotCall
                            for y in game["alive"]:
                                if y != max:
                                    py = ctx.guild.get_member(int(y))
                                    TSShot.add_option(label=f"{py.name}",value=py.id)
                            TSView.add_item(TSShot)
                            TSMsg = await vilRoom.send(embed=TSEmbed,view=TSView)
                            while timer > 0 and TSd["dead"] == None:
                                await asyncio.sleep(1)
                                timer -= 1
                                TSEmbed.title = f"Thợ Săn đã chết!! ({timer}/15)"
                                await TSMsg.edit(embed=TSEmbed)
                            TSShot.disabled = True
                            await TSMsg.edit(view=TSView)
                            game["alive"].pop(max)
                            game["dead"].append(max)
                            p = client.get_guild(guild).get_member(int(max))
                            await vilRoom.set_permissions(p,send_messages=False,view_channel=True)
                            await wereRoom.set_permissions(p,send_messages=False,view_channel=True)
                            await Voice.set_permissions(p,speak = False,view_channel=True)
            else:
                if max != None:
                    if len(game["alive"][max]) != count :
                        game["alive"].pop(max)
                        game["dead"].append(max)
                        p = client.get_guild(guild).get_member(int(max))
                        await vilRoom.set_permissions(p,send_messages=False,view_channel=True)
                        await wereRoom.set_permissions(p,send_messages=False,view_channel=True)
                        await Voice.set_permissions(p,speak = False,view_channel=True)
            if "Cupid" in data["villager"] and len(game["alive"]) == 2 and Night != 0:
                if game["Link"] != []:
                    if game["Link"][0] in game["alive"] and game["Link"][1] in game["alive"]:
                        rname = game["name"]
                        p1 = ctx.guild.get_member(int(game["Link"][0]))
                        p2 = ctx.guild.get_member(int(game["Link"][1]))
                        WinEmbed = discord.Embed(title="Chúc Mừng Cặp Đôi Chiến Thắng!!",description=f"**Tên Phòng:** {rname}\n**Người Thắng:** {p1.name}, {p2.name}\n**Số Đêm:** {Night}",color=0xFFFFFF)
                        WinEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                        await ctx.send(embed=WinEmbed)
                        await vilRoom.delete()
                        await wereRoom.delete()
                        await Voice.delete()
                        werewolf[str(guild)]["room"].remove(game)
                        with open("werewolf.json","w") as f:
                            json.dump(werewolf,f)
                        break
            wolfCount = 0
            vilCount = 0
            for x in game["alive"]:
                if game["role"][x] in game["data"]["werewolf"]:
                    wolfCount += 1
                elif game["role"][x] in game["data"]["villager"]:
                    vilCount += 1
            if wolfCount == 0 and vilCount != 0:
                rname = game["name"]
                WinEmbed = discord.Embed(title="Chúc Mừng Dân Làng Chiến Thắng!!",color=0xFFFFFF)
                WinDes=f"**Tên Phòng:** {rname}\n**Người Thắng:** "
                for x in game["alive"]:
                    p = ctx.guild.get_member(int(x))
                    WinDes += f"{p.name} "
                WinDes += f"\n**Số Đêm:** {Night}"
                WinEmbed.description = WinDes
                WinEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                await ctx.send(embed=WinEmbed)
                await vilRoom.delete()
                await wereRoom.delete()
                await Voice.delete()
                werewolf[str(guild)]["room"].remove(game)
                with open("werewolf.json","w") as f:
                    json.dump(werewolf,f)
                break
            elif wolfCount != 0 and vilCount == 0:
                rname = game["name"]
                WinEmbed = discord.Embed(title="Chúc Mừng Ma Sói Chiến Thắng!!",color=0xFFFFFF)
                WinDes=f"**Tên Phòng:** {rname}\n**Người Thắng:** "
                for x in game["alive"]:
                    p = ctx.guild.get_member(int(x))
                    WinDes += f"{p.name} "
                WinDes += f"\n**Số Đêm:** {Night}"
                WinEmbed.description = WinDes
                WinEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                await ctx.send(embed=WinEmbed)
                await vilRoom.delete()
                await wereRoom.delete()
                await Voice.delete()
                werewolf[str(guild)]["room"].remove(game)
                with open("werewolf.json","w") as f:
                    json.dump(werewolf,f)
                break
            elif wolfCount == 0 and vilCount == 0:
                rname = game["name"]
                WinEmbed = discord.Embed(title="Hòa Nhau, Không Có Người Thắng!!",color=0xFFFFFF)
                WinDes=f"**Tên Phòng:** {rname}\n**Số Đêm:** {Night}"
                WinEmbed.description = WinDes
                WinEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                await ctx.send(embed=WinEmbed)
                await vilRoom.delete()
                await wereRoom.delete()
                await Voice.delete()
                werewolf[str(guild)]["room"].remove(game)
                with open("werewolf.json","w") as f:
                    json.dump(werewolf,f)
                break
            await vilRoom.send(embed=NightEmbed)
            Night+=1
            if "Cupid" in data["villager"] and Night == 1:
                await asyncio.sleep(1)
                timer = 30
                CupidEmbed = discord.Embed(title=f"Cupid dậy đi! ({timer}/30)",color=0xFF00B2)
                CupidEmbed.set_image(url="https://media.istockphoto.com/vectors/cupid-vector-id96893233?k=20&m=96893233&s=612x612&w=0&h=A7b54BCLdRXMATO6wvM06CAc2htQ06GnKsm9Hfs-4Yo=")
                CupidEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                async def NoShotCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Cupid":
                            game["Link"] = None
                            await interaction.response.send_message(content="Bạn đã từ bỏ bắn mũi tên tình yêu",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Cupid",ephemeral=True)
                    else:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                async def ShotCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Cupid":
                            ChooseEmbed = discord.Embed(title="Chọn 2 người để họ yêu nhau")
                            ChooseView = discord.ui.View(timeout=None)
                            ChooseSelect = discord.ui.Select(placeholder="Chọn 2 người",min_values=2,max_values=2)
                            async def SelectCallback(inter:discord.Interaction):
                                for l in ChooseSelect.values:
                                    game["Link"].append(l)
                                p1 = ctx.guild.get_member(int(game["Link"][0]))
                                p2 = ctx.guild.get_member(int(game["Link"][1]))
                                await inter.response.send_message(content=f"Đã liên kết {p1.name} với {p2.name}",ephemeral=True)
                            ChooseSelect.callback = SelectCallback
                            for x in game["alive"]:
                                p = client.get_guild(guild).get_member(int(x))
                                ChooseSelect.add_option(label=f"{p.name}",value=x)
                            ChooseView.add_item(ChooseSelect)
                            await interaction.response.send_message(embed=ChooseEmbed,view=ChooseView,ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Cupid",ephemeral=True)
                    else:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                CupidView = discord.ui.View(timeout=None)
                CupidButton = discord.ui.Button(label="Bắn",style=discord.ButtonStyle.green)
                NoCupidButton = discord.ui.Button(label="Không Bắn",style=discord.ButtonStyle.red)
                CupidButton.callback = ShotCallback
                NoCupidButton.callback = NoShotCallback
                CupidView.add_item(CupidButton)
                CupidView.add_item(NoCupidButton)
                CupidMsg = await vilRoom.send(embed=CupidEmbed,view=CupidView)
                game["Link"] = []
                while timer > 0 and game["Link"] == []:
                    await asyncio.sleep(1)
                    timer -= 1
                    CupidEmbed.title = f"Cupid dậy đi! ({timer}/30)"
                    await CupidMsg.edit(embed=CupidEmbed)
                CupidButton.disabled = True
                NoCupidButton.disabled = True
                await CupidMsg.edit(view=CupidView)
                await asyncio.sleep(1)
            if "Bảo Vệ" in data["villager"] and Night == 1:
                game["protect"] = 0
                timer = 30
                async def protectCallback(interaction: discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Bảo Vệ":
                            game["protect"] = int(protectSelect.values[0])
                            protectSelect.disabled = True
                            await interaction.response.edit_message(view=protectView)
                        else:
                            await interaction.response.send_message(content="Bạn không phải bảo vệ",ephemeral=True)
                    else:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                protectView = discord.ui.View(timeout=None)
                ProtectOption = []
                for x in game["alive"]:
                    p = client.get_guild(guild).get_member(int(x))
                    ProtectOption.append(discord.SelectOption(label=f"{p.name}",value=x))
                protectSelect = discord.ui.Select(placeholder="Chọn Người Bạn Muốn Bảo Vệ",max_values=1,options=ProtectOption)
                protectSelect.callback = protectCallback
                protectView.add_item(protectSelect)
                ProtectEmbed = discord.Embed(color=0x0027FF,title=f"Bảo vệ dậy đi! ({timer}/30)")
                ProtectEmbed.set_image(url="https://w7.pngwing.com/pngs/474/333/png-transparent-shield-metal-icon-shield-element-chemical-element-angle-shields.png")
                ProtectEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                protectMsg = await vilRoom.send(embed=ProtectEmbed,view=protectView)
                while timer > 0 and game["protect"] == 0:
                    await asyncio.sleep(1)
                    timer -=1
                    ProtectEmbed.title = f"Bảo vệ dậy đi! ({timer}/30)"
                    await protectMsg.edit(embed=ProtectEmbed)
                protectSelect.disabled = True
                await protectMsg.edit(view=protectView)
                await asyncio.sleep(1)
            elif "Bảo Vệ" in data["villager"] and Night != 1:
                timer = 30
                async def protectCallback(interaction: discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Bảo Vệ":
                            if game["protect"] != int(protectSelect.values[0]):
                                game["protect"] = int(protectSelect.values[0])
                                protectSelect.disabled = True
                                await interaction.response.edit_message(view=protectView)
                            elif game["protect"] == int(protectSelect.values[0]):
                                await interaction.response.send_message(content="Bạn đã bảo vệ người này tối qua",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải bảo vệ",ephemeral=True)
                    else:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                protectView = discord.ui.View(timeout=None)
                ProtectOption = []
                for x in game["alive"]:
                    p = client.get_guild(guild).get_member(int(x))
                    ProtectOption.append(discord.SelectOption(label=f"{p.name}",value=x))
                protectSelect = discord.ui.Select(placeholder="Chọn Người Bạn Muốn Bảo Vệ",max_values=1,options=ProtectOption)
                protectSelect.callback = protectCallback
                protectView.add_item(protectSelect)
                ProtectEmbed = discord.Embed(color=0x0027FF,title=f"Bảo vệ dậy đi! ({timer}/30)")
                ProtectEmbed.set_image(url="https://w7.pngwing.com/pngs/474/333/png-transparent-shield-metal-icon-shield-element-chemical-element-angle-shields.png")
                ProtectEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                protectMsg = await vilRoom.send(embed=ProtectEmbed,view=protectView)
                while timer > 0 and game["protect"] == 0:
                    await asyncio.sleep(1)
                    timer -=1
                    ProtectEmbed.title = f"Bảo vệ dậy đi! ({timer}/30)"
                    await protectMsg.edit(embed=ProtectEmbed)
                protectSelect.disabled = True
                await protectMsg.edit(view=protectView)
                await asyncio.sleep(1)
            if "Tiên Tri" in data["villager"]:
                timer = 30
                TTri = {}
                TTri["Done"] = None
                TTEmbed = discord.Embed(color=0x00A3F5,title=f"Tiên Tri dậy đi! ({timer}/30)")
                TTEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                TTEmbed.set_image(url="https://hstatic.net/363/1000016363/10/2016/6-4/tien-tri-1.jpg")
                TTView = discord.ui.View(timeout=None)
                async def TTCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Tiên Tri":
                            ChooseEmbed = discord.Embed(color=0x00A3F5,title="Chọn người để kiểm tra role")
                            ChooseEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                            ChooseView = discord.ui.View(timeout=None)
                            async def ChooseCall(inter:discord.Interaction):
                                if TTri["Done"] == None:
                                    pl = ctx.guild.get_member(int(ChooseSel.values[0]))
                                    role = game["role"][str(ChooseSel.values[0])]
                                    RoleEmbed = discord.Embed(color=0x00A3F5,title=f"Role của {pl.name} là: {role}")
                                    RoleEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                                    await inter.response.send_message(embed=RoleEmbed,ephemeral=True)
                                    TTri["Done"] = 1
                                else:
                                    await inter.response.send_message(content="Không kiểm tra được người nữa đâu ba",ephemeral=True)
                            ChooseSel = discord.ui.Select(placeholder="Chọn 1 người")
                            ChooseSel.callback = ChooseCall
                            ChooseView.add_item(ChooseSel)
                            for y in game["alive"]:
                                p = ctx.guild.get_member(int(y))
                                ChooseSel.add_option(label=f"{p.name}",value=p.id)
                            await interaction.response.send_message(embed=ChooseEmbed,view=ChooseView,ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Tiên Tri",ephemeral=True)
                    else:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                async def NoCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Tiên Tri":
                            TTri["Done"] = 1
                            await interaction.response.send_message(content="Bạn đã từ bỏ kiểm tra",ephemeral=True)  
                        else:  
                            await interaction.response.send_message(content="Bạn không phải Tiên Tri",ephemeral=True)  
                    else:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                TTSee = discord.ui.Button(label="Tiên Tri",style=discord.ButtonStyle.green)
                NoTT = discord.ui.Button(label="Bỏ Qua",style=discord.ButtonStyle.red)
                NoTT.callback = NoCallback
                TTSee.callback = TTCallback
                TTView.add_item(TTSee)
                TTView.add_item(NoTT)
                TTMsg = await vilRoom.send(embed=TTEmbed,view=TTView)
                while timer > 0 and TTri["Done"] == None:
                    await asyncio.sleep(1)
                    timer -= 1
                    TTEmbed.title = f"Tiên Tri dậy đi! ({timer}/30)"
                    await TTMsg.edit(embed=TTEmbed)
                NoTT.disabled = True
                TTSee.disabled = True
                await TTMsg.edit(view=TTView)
                await asyncio.sleep(1)
            timer = 50
            WWEmbed = discord.Embed(color=0x566164,title="Chọn một người để cắn đêm nay!",description=f"**Thời Gian:** {timer}/50")
            WWView = discord.ui.View(timeout=None)
            WWVote = {}
            WWVote["Vote"] = {}
            WWVote["NoVote"] = []
            WWSelect = discord.ui.Select(placeholder="Chọn người để cắn")
            WWBite = discord.ui.Button(label="Cắn",style=discord.ButtonStyle.red)
            WWNoBite = discord.ui.Button(label="Không Cắn",style=discord.ButtonStyle.green)
            async def WWSCallback(interaction:discord.Interaction):
                await interaction.response.defer()
            async def BiteCallback(interaction:discord.Interaction):
                if str(interaction.user.id) in game["alive"]:
                    if interaction.user.id in WWVote["NoVote"]:
                        WWVote["NoVote"].remove(interaction.user.id)
                        WWVote["Vote"][str(WWSelect.values[0])].append(interaction.user.id)
                        WWEmbed.clear_fields()
                        for x in game["alive"]:
                            play = ctx.guild.get_member(int(x))
                            vote = len(WWVote["Vote"][x])
                            WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                        await interaction.response.edit_message(embed=WWEmbed)
                    elif interaction.user.id in WWVote["Vote"][str(WWSelect.values[0])]:
                        await interaction.response.send_message(content="Bạn đã vote người này trước đó",ephemeral=True)
                    else:
                        c = 0
                        for x in WWVote["Vote"]:
                            if x == str(WWSelect.values[0]):
                                pass
                            else:
                                if interaction.user.id in WWVote["Vote"][x]:
                                    WWVote["Vote"][x].remove(interaction.user.id)
                                    WWVote["Vote"][str(WWSelect.values[0])].append(interaction.user.id)
                                    WWEmbed.clear_fields()
                                    for x in game["alive"]:
                                        play = ctx.guild.get_member(int(x))
                                        vote = len(WWVote["Vote"][x])
                                        WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                                    await interaction.response.edit_message(embed=WWEmbed)
                                    c+=1
                        if c == 0:
                            WWVote["Vote"][str(WWSelect.values[0])].append(interaction.user.id)
                            WWEmbed.clear_fields()
                            for x in game["alive"]:
                                play = ctx.guild.get_member(int(x))
                                vote = len(WWVote["Vote"][x])
                                WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                            await interaction.response.edit_message(embed=WWEmbed)
                else:
                    await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
            async def NoBiteCallback(interaction:discord.Interaction):
                if str(interaction.user.id) in game["alive"]:
                    if interaction.user.id in WWVote["NoVote"]:
                        await interaction.response.send_message(content="Bạn đã bỏ vote trước đó",ephemeral=True)
                    else:
                        c = 0
                        for x in WWVote["Vote"]:
                            if WWSelect.values != []:
                                if x == str(WWSelect.values[0]):
                                    pass
                                else:
                                    if interaction.user.id in WWVote["Vote"][x]:
                                        WWVote["Vote"][x].remove(interaction.user.id)
                                        WWVote["NoVote"].append(interaction.user.id)
                                        for x in game["alive"]:
                                            play = ctx.guild.get_member(int(x))
                                            vote = len(WWVote["Vote"][x])
                                            WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                                        await WWVMsg.edit(embed=WWEmbed)
                                        await interaction.response.send_message(content="Bỏ vote thành công",ephemeral=True)
                                        c+=1
                            else:
                                if interaction.user.id in WWVote["Vote"][x]:
                                    WWVote["Vote"][x].remove(interaction.user.id)
                                    WWVote["NoVote"].append(interaction.user.id)
                                    for x in game["alive"]:
                                        play = ctx.guild.get_member(int(x))
                                        vote = len(WWVote["Vote"][x])
                                        WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                                    await WWVMsg.edit(embed=WWEmbed)
                                    await interaction.response.send_message(content="Bỏ vote thành công",ephemeral=True)
                                    c+=1
                        if c == 0:
                            WWVote["NoVote"].append(interaction.user.id)
                            await interaction.response.send_message(content="Bỏ vote thành công",ephemeral=True)
                else:
                    await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
            WWView.add_item(WWSelect)
            WWSelect.callback = WWSCallback
            WWView.add_item(WWBite)
            WWBite.callback = BiteCallback
            WWView.add_item(WWNoBite)
            WWNoBite.callback = NoBiteCallback
            for x in game["alive"]:
                play = ctx.guild.get_member(int(x))
                WWVote["Vote"][x] = []
                WWEmbed.add_field(name=f"{play.name}",value="0 vote",inline=True)
                WWSelect.add_option(label=f"{play.name}",value=play.id)
            WWEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
            WWVMsg = await wereRoom.send(embed=WWEmbed,view=WWView)
            WWVCount = 0
            AliveWW = 0
            for x in game["alive"]:
                if game["role"][x] in game["data"]["werewolf"]:
                    AliveWW +=1
            while timer > 0 and (WWVCount + len(WWVote["NoVote"])) != AliveWW:
                await asyncio.sleep(1)
                timer -= 1
                WWEmbed.description=f"**Thời Gian:** {timer}/50"
                await WWVMsg.edit(embed=WWEmbed)
                for y in WWVote["Vote"]:
                    WWVCount += len(WWVote["Vote"][y])
            wwcount = 0
            wwmax = None
            for x in WWVote["Vote"]:
                if wwcount == 0 and len(WWVote["Vote"][x]) > 0:
                    wwmax = x
                    count=-1
                elif len(WWVote["Vote"][x]) > 0 and wwcount != 0:
                    if len(WWVote["Vote"][wwmax]) < len(WWVote["Vote"][x]):
                        wwmax = x
                    elif len(WWVote["Vote"][wwmax]) == len(WWVote["Vote"][x]): 
                        wwcount = len(WWVote["Vote"][wwmax])
            WWSelect.disabled = True
            WWBite.disabled = True
            WWNoBite.disabled = True
            await WWVMsg.edit(view=WWView)
            await asyncio.sleep(1)
            if wwmax != None:
                if len(WWVote["Vote"][wwmax]) != wwcount and "Bảo Vệ" in data["villager"]:
                    if int(wwmax) != game["protect"]:
                        game["alive"].pop(wwmax)
                        game["dead"].append(wwmax)
                        if game["role"][wwmax] == "Thợ Săn":
                            TSd["selfDead"] = 1
                        if game["role"][wwmax] == "Phù Thủy":
                            WitchDead["check"] = True
                        if "Sói Nguyền" in game["data"]["werewolf"] and Night == 1:
                            Curse["check"] = True
                            Curse["NoneCurse"] = False
                            timer = 30
                            CurseEmbed = discord.Embed(color=0x000000,title="Sói Nguyền dậy đi!",description=f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không")
                            CurseView = discord.ui.View(timeout=None)
                            async def CurseCallback(interaction:discord.Interaction):
                                if str(interaction.user.id) in game["alive"]:
                                    if game["role"][str(interaction.user.id)] == "Sói Nguyền":
                                        Curse["check"] = False
                                        game["alive"][wwmax] = []
                                        game["dead"].remove(wwmax)
                                        if game["role"][wwmax] == "Thợ Săn":
                                            TSd["selfDead"] = None
                                        if game["role"][wwmax] == "Phù Thủy":
                                            WitchDead["check"] = False
                                        game["role"][wwmax] = "Sói Thường"
                                        p = ctx.guild.get_member(int(wwmax))
                                        await interaction.response.send_message(content=f"Nguyền thành công **{p.name}**",ephemeral=True)
                                    else:
                                        await interaction.response.send_message(content="Bạn không phải Sói Nguyền",ephemeral=True)
                                else:
                                    await interaction.response.send_message(content="Bạn chết rồi, ấn cái gì mà ấn.",ephemeral=True)
                            async def NoCurseCallback(interaction:discord.Interaction):
                                Curse["NoneCurse"] = True
                                await interaction.response.send_message(content="Bạn đã từ bỏ nguyền",ephemeral=True)
                            CurseButton = discord.ui.Button(label="Nguyền",style=discord.ButtonStyle.red)
                            NoCurseButton = discord.ui.Button(label="Không Nguyền",style=discord.ButtonStyle.red)
                            CurseButton.callback = CurseCallback
                            NoCurseButton.callback = NoCurseCallback
                            CurseView.add_item(CurseButton)
                            CurseView.add_item(NoCurseButton)
                            CurseMsg = await wereRoom.send(embed=CurseEmbed,view=CurseView)
                            while timer > 0 and Curse["check"] == True and Curse["NoneCurse"] == False:
                                await asyncio.sleep(1)
                                timer -= 1
                                CurseEmbed.description = f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không"
                                await CurseMsg.edit(embed=CurseEmbed)
                            CurseButton.disabled = True
                            NoCurseButton.disabled = True
                            await CurseMsg.edit(view=CurseView)
                        elif "Sói Nguyền" in game["data"]["werewolf"] and Night != 1 and Curse["check"] == True:
                            Curse["NoneCurse"] = False
                            timer = 30
                            CurseEmbed = discord.Embed(color=0x000000,title="Sói Nguyền dậy đi!",description=f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không")
                            CurseView = discord.ui.View(timeout=None)
                            async def CurseCallback(interaction:discord.Interaction):
                                if str(interaction.user.id) in game["alive"]:
                                    if game["role"][str(interaction.user.id)] == "Sói Nguyền":
                                        Curse["check"] = False
                                        game["alive"][wwmax] = []
                                        game["dead"].remove(wwmax)
                                        if game["role"][wwmax] == "Thợ Săn":
                                            TSd["selfDead"] = None
                                        if game["role"][wwmax] == "Phù Thủy":
                                            WitchDead["check"] = False
                                        game["role"][wwmax] = "Sói Thường"
                                        p = ctx.guild.get_member(int(wwmax))
                                        await interaction.response.send_message(content=f"Nguyền thành công **{p.name}**",ephemeral=True)
                                    else:
                                        await interaction.response.send_message(content="Bạn không phải Sói Nguyền",ephemeral=True)
                                else:
                                    await interaction.response.send_message(content="Bạn chết rồi, ấn cái gì mà ấn.",ephemeral=True)
                            async def NoCurseCallback(interaction:discord.Interaction):
                                Curse["NoneCurse"] = True
                                await interaction.response.send_message(content="Bạn đã từ bỏ nguyền",ephemeral=True)
                            CurseButton = discord.ui.Button(label="Nguyền",style=discord.ButtonStyle.red)
                            NoCurseButton = discord.ui.Button(label="Không Nguyền",style=discord.ButtonStyle.red)
                            CurseButton.callback = CurseCallback
                            NoCurseButton.callback = NoCurseCallback
                            CurseView.add_item(CurseButton)
                            CurseView.add_item(NoCurseButton)
                            CurseMsg = await wereRoom.send(embed=CurseEmbed,view=CurseView)
                            while timer > 0 and Curse["check"] == True and Curse["NoneCurse"] == False:
                                await asyncio.sleep(1)
                                timer -= 1
                                CurseEmbed.description = f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không"
                                await CurseMsg.edit(embed=CurseEmbed)
                            CurseButton.disabled = True
                            NoCurseButton.disabled = True
                            await CurseMsg.edit(view=CurseView)
                elif len(WWVote["Vote"][wwmax]) != wwcount and "Bảo Vệ" not in data["villager"]:
                    game["alive"].pop(wwmax)
                    game["dead"].append(wwmax)
                    if game["role"][wwmax] == "Thợ Săn":
                        TSd["selfDead"] = 1
                    if game["role"][wwmax] == "Phù Thủy":
                        WitchDead["check"] = True
                    if "Sói Nguyền" in game["data"]["werewolf"] and Night == 1:
                        Curse["check"] = True
                        Curse["NoneCurse"] = False
                        timer = 30
                        CurseEmbed = discord.Embed(color=0x000000,title="Sói Nguyền dậy đi!",description=f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không")
                        CurseView = discord.ui.View(timeout=None)
                        async def CurseCallback(interaction:discord.Interaction):
                            if str(interaction.user.id) in game["alive"]:
                                if game["role"][str(interaction.user.id)] == "Sói Nguyền":
                                    Curse["check"] = False
                                    game["alive"][wwmax] = []
                                    game["dead"].remove(wwmax)
                                    if game["role"][wwmax] == "Thợ Săn":
                                        TSd["selfDead"] = None
                                    if game["role"][wwmax] == "Phù Thủy":
                                        WitchDead["check"] = False
                                    game["role"][wwmax] = "Sói Thường"
                                    p = ctx.guild.get_member(int(wwmax))
                                    await interaction.response.send_message(content=f"Nguyền thành công **{p.name}**",ephemeral=True)
                                else:
                                    await interaction.response.send_message(content="Bạn không phải Sói Nguyền",ephemeral=True)
                            else:
                                await interaction.response.send_message(content="Bạn chết rồi, ấn cái gì mà ấn.",ephemeral=True)
                        async def NoCurseCallback(interaction:discord.Interaction):
                            Curse["NoneCurse"] = True
                            await interaction.response.send_message(content="Bạn đã từ bỏ nguyền",ephemeral=True)
                        CurseButton = discord.ui.Button(label="Nguyền",style=discord.ButtonStyle.red)
                        NoCurseButton = discord.ui.Button(label="Không Nguyền",style=discord.ButtonStyle.red)
                        CurseButton.callback = CurseCallback
                        NoCurseButton.callback = NoCurseCallback
                        CurseView.add_item(CurseButton)
                        CurseView.add_item(NoCurseButton)
                        CurseMsg = await wereRoom.send(embed=CurseEmbed,view=CurseView)
                        while timer > 0 and Curse["check"] == True and Curse["NoneCurse"] == False:
                            await asyncio.sleep(1)
                            timer -= 1
                            CurseEmbed.description = f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không"
                            await CurseMsg.edit(embed=CurseEmbed)
                        CurseButton.disabled = True
                        NoCurseButton.disabled = True
                        await CurseMsg.edit(view=CurseView)
                    elif "Sói Nguyền" in game["data"]["werewolf"] and Night != 1 and Curse["check"] == True:
                        Curse["NoneCurse"] = False
                        timer = 30
                        CurseEmbed = discord.Embed(color=0x000000,title="Sói Nguyền dậy đi!",description=f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không")
                        CurseView = discord.ui.View(timeout=None)
                        async def CurseCallback(interaction:discord.Interaction):
                            if str(interaction.user.id) in game["alive"]:
                                if game["role"][str(interaction.user.id)] == "Sói Nguyền":
                                    Curse["check"] = False
                                    game["alive"][wwmax] = []
                                    game["dead"].remove(wwmax)
                                    if game["role"][wwmax] == "Thợ Săn":
                                        TSd["selfDead"] = None
                                    if game["role"][wwmax] == "Phù Thủy":
                                        WitchDead["check"] = False
                                    game["role"][wwmax] = "Sói Thường"
                                    p = ctx.guild.get_member(int(wwmax))
                                    await interaction.response.send_message(content=f"Nguyền thành công **{p.name}**",ephemeral=True)
                                else:
                                    await interaction.response.send_message(content="Bạn không phải Sói Nguyền",ephemeral=True)
                            else:
                                await interaction.response.send_message(content="Bạn chết rồi, ấn cái gì mà ấn.",ephemeral=True)
                        async def NoCurseCallback(interaction:discord.Interaction):
                            Curse["NoneCurse"] = True
                            await interaction.response.send_message(content="Bạn đã từ bỏ nguyền",ephemeral=True)
                        CurseButton = discord.ui.Button(label="Nguyền",style=discord.ButtonStyle.red)
                        NoCurseButton = discord.ui.Button(label="Không Nguyền",style=discord.ButtonStyle.red)
                        CurseButton.callback = CurseCallback
                        NoCurseButton.callback = NoCurseCallback
                        CurseView.add_item(CurseButton)
                        CurseView.add_item(NoCurseButton)
                        CurseMsg = await wereRoom.send(embed=CurseEmbed,view=CurseView)
                        while timer > 0 and Curse["check"] == True and Curse["NoneCurse"] == False:
                            await asyncio.sleep(1)
                            timer -= 1
                            CurseEmbed.description = f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không"
                            await CurseMsg.edit(embed=CurseEmbed)
                        CurseButton.disabled = True
                        NoCurseButton.disabled = True
                        await CurseMsg.edit(view=CurseView)
            if "Sói Con" in game["data"]["werewolf"]:
                sc = list(game["role"].keys())[list(game["role"].values()).index("Sói Con")]
                if sc in game["dead"]:
                    timer = 50
                    WWEmbed = discord.Embed(color=0x566164,title="Chọn một người để cắn đêm nay!",description=f"**Thời Gian:** {timer}/50")
                    WWView = discord.ui.View(timeout=None)
                    WWVote = {}
                    WWVote["Vote"] = {}
                    WWVote["NoVote"] = []
                    WWSelect = discord.ui.Select(placeholder="Chọn người để cắn")
                    WWBite = discord.ui.Button(label="Cắn",style=discord.ButtonStyle.red)
                    WWNoBite = discord.ui.Button(label="Không Cắn",style=discord.ButtonStyle.green)
                    async def WWSCallback(interaction:discord.Interaction):
                        await interaction.response.defer()
                    async def BiteCallback(interaction:discord.Interaction):
                        if str(interaction.user.id) in game["alive"]:
                            if interaction.user.id in WWVote["NoVote"]:
                                WWVote["NoVote"].remove(interaction.user.id)
                                WWVote["Vote"][str(WWSelect.values[0])].append(interaction.user.id)
                                WWEmbed.clear_fields()
                                for x in game["alive"]:
                                    play = ctx.guild.get_member(int(x))
                                    vote = len(WWVote["Vote"][x])
                                    WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                                await interaction.response.edit_message(embed=WWEmbed)
                            elif interaction.user.id in WWVote["Vote"][str(WWSelect.values[0])]:
                                await interaction.response.send_message(content="Bạn đã vote người này trước đó",ephemeral=True)
                            else:
                                c = 0
                                for x in WWVote["Vote"]:
                                    if x == str(WWSelect.values[0]):
                                        pass
                                    else:
                                        if interaction.user.id in WWVote["Vote"][x]:
                                            WWVote["Vote"][x].remove(interaction.user.id)
                                            WWVote["Vote"][str(WWSelect.values[0])].append(interaction.user.id)
                                            WWEmbed.clear_fields()
                                            for x in game["alive"]:
                                                play = ctx.guild.get_member(int(x))
                                                vote = len(WWVote["Vote"][x])
                                                WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                                            await interaction.response.edit_message(embed=WWEmbed)
                                            c+=1
                                if c == 0:
                                    WWVote["Vote"][str(WWSelect.values[0])].append(interaction.user.id)
                                    WWEmbed.clear_fields()
                                    for x in game["alive"]:
                                        play = ctx.guild.get_member(int(x))
                                        vote = len(WWVote["Vote"][x])
                                        WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                                    await interaction.response.edit_message(embed=WWEmbed)
                        else:
                            await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                    async def NoBiteCallback(interaction:discord.Interaction):
                        if str(interaction.user.id) in game["alive"]:
                            if interaction.user.id in WWVote["NoVote"]:
                                await interaction.response.send_message(content="Bạn đã bỏ vote trước đó",ephemeral=True)
                            else:
                                c = 0
                                for x in WWVote["Vote"]:
                                    if WWSelect.values != []:
                                        if x == str(WWSelect.values[0]):
                                            pass
                                        else:
                                            if interaction.user.id in WWVote["Vote"][x]:
                                                WWVote["Vote"][x].remove(interaction.user.id)
                                                WWVote["NoVote"].append(interaction.user.id)
                                                for x in game["alive"]:
                                                    play = ctx.guild.get_member(int(x))
                                                    vote = len(WWVote["Vote"][x])
                                                    WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                                                await WWVMsg.edit(embed=WWEmbed)
                                                await interaction.response.send_message(content="Bỏ vote thành công",ephemeral=True)
                                                c+=1
                                    else:
                                        if interaction.user.id in WWVote["Vote"][x]:
                                            WWVote["Vote"][x].remove(interaction.user.id)
                                            WWVote["NoVote"].append(interaction.user.id)
                                            for x in game["alive"]:
                                                play = ctx.guild.get_member(int(x))
                                                vote = len(WWVote["Vote"][x])
                                                WWEmbed.add_field(name=f"{play.name}",value=f"{vote} vote",inline=True)
                                            await WWVMsg.edit(embed=WWEmbed)
                                            await interaction.response.send_message(content="Bỏ vote thành công",ephemeral=True)
                                            c+=1
                                if c == 0:
                                    WWVote["NoVote"].append(interaction.user.id)
                                    await interaction.response.send_message(content="Bỏ vote thành công",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                    WWView.add_item(WWSelect)
                    WWSelect.callback = WWSCallback
                    WWView.add_item(WWBite)
                    WWBite.callback = BiteCallback
                    WWView.add_item(WWNoBite)
                    WWNoBite.callback = NoBiteCallback
                    for x in game["alive"]:
                        play = ctx.guild.get_member(int(x))
                        WWVote["Vote"][x] = []
                        WWEmbed.add_field(name=f"{play.name}",value="0 vote",inline=True)
                        WWSelect.add_option(label=f"{play.name}",value=play.id)
                    WWEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                    WWVMsg = await wereRoom.send(embed=WWEmbed,view=WWView)
                    WWVCount = 0
                    AliveWW = 0
                    for x in game["alive"]:
                        if game["role"][x] in game["data"]["werewolf"]:
                            AliveWW +=1
                    while timer > 0 and (WWVCount + len(WWVote["NoVote"])) != AliveWW:
                        await asyncio.sleep(1)
                        timer -= 1
                        WWEmbed.description=f"**Thời Gian:** {timer}/50"
                        await WWVMsg.edit(embed=WWEmbed)
                        for y in WWVote["Vote"]:
                            WWVCount += len(WWVote["Vote"][y])
                    wwcount = 0
                    wwmax = None
                    for x in WWVote["Vote"]:
                        if wwcount == 0 and len(WWVote["Vote"][x]) > 0:
                            wwmax = x
                            count=-1
                        elif len(WWVote["Vote"][x]) > 0 and wwcount != 0:
                            if len(WWVote["Vote"][wwmax]) < len(WWVote["Vote"][x]):
                                wwmax = x
                            elif len(WWVote["Vote"][wwmax]) == len(WWVote["Vote"][x]): 
                                wwcount = len(WWVote["Vote"][wwmax])
                    WWSelect.disabled = True
                    WWBite.disabled = True
                    WWNoBite.disabled = True
                    await WWVMsg.edit(view=WWView)
                    await asyncio.sleep(1)
                    if wwmax != None:
                        if len(WWVote["Vote"][wwmax]) != wwcount and "Bảo Vệ" in data["villager"]:
                            if int(wwmax) != game["protect"]:
                                game["alive"].pop(wwmax)
                                game["dead"].append(wwmax)
                                if game["role"][wwmax] == "Thợ Săn":
                                    TSd["selfDead"] = 1
                                if game["role"][wwmax] == "Phù Thủy":
                                    WitchDead["check"] = True
                                if "Sói Nguyền" in game["data"]["werewolf"] and Curse["check"] == True:
                                    Curse["NoneCurse"] = False
                                    timer = 30
                                    CurseEmbed = discord.Embed(color=0x000000,title="Sói Nguyền dậy đi!",description=f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không")
                                    CurseView = discord.ui.View(timeout=None)
                                    async def CurseCallback(interaction:discord.Interaction):
                                        if str(interaction.user.id) in game["alive"]:
                                            if game["role"][str(interaction.user.id)] == "Sói Nguyền":
                                                Curse["check"] = False
                                                game["alive"][wwmax] = []
                                                game["dead"].remove(wwmax)
                                                if game["role"][wwmax] == "Thợ Săn":
                                                    TSd["selfDead"] = None
                                                if game["role"][wwmax] == "Phù Thủy":
                                                    WitchDead["check"] = False
                                                game["role"][wwmax] = "Sói Thường"
                                                p = ctx.guild.get_member(int(wwmax))
                                                await interaction.response.send_message(content=f"Nguyền thành công **{p.name}**",ephemeral=True)
                                            else:
                                                await interaction.response.send_message(content="Bạn không phải Sói Nguyền",ephemeral=True)
                                        else:
                                            await interaction.response.send_message(content="Bạn chết rồi, ấn cái gì mà ấn.",ephemeral=True)
                                    async def NoCurseCallback(interaction:discord.Interaction):
                                        Curse["NoneCurse"] = True
                                        await interaction.response.send_message(content="Bạn đã từ bỏ nguyền",ephemeral=True)
                                    CurseButton = discord.ui.Button(label="Nguyền",style=discord.ButtonStyle.red)
                                    NoCurseButton = discord.ui.Button(label="Không Nguyền",style=discord.ButtonStyle.red)
                                    CurseButton.callback = CurseCallback
                                    NoCurseButton.callback = NoCurseCallback
                                    CurseView.add_item(CurseButton)
                                    CurseView.add_item(NoCurseButton)
                                    CurseMsg = await wereRoom.send(embed=CurseEmbed,view=CurseView)
                                    while timer > 0 and Curse["check"] == True and Curse["NoneCurse"] == False:
                                        await asyncio.sleep(1)
                                        timer -= 1
                                        CurseEmbed.description = f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không"
                                        await CurseMsg.edit(embed=CurseEmbed)
                                    CurseButton.disabled = True
                                    NoCurseButton.disabled = True
                                    await CurseMsg.edit(view=CurseView)
                        elif len(WWVote["Vote"][wwmax]) != wwcount and "Bảo Vệ" not in data["villager"]:
                            game["alive"].pop(wwmax)
                            game["dead"].append(wwmax)
                            if game["role"][wwmax] == "Thợ Săn":
                                TSd["selfDead"] = 1
                            if game["role"][wwmax] == "Phù Thủy":
                                WitchDead["check"] = True
                            if "Sói Nguyền" in game["data"]["werewolf"] and Curse["check"] == True:
                                Curse["NoneCurse"] = False
                                timer = 30
                                CurseEmbed = discord.Embed(color=0x000000,title="Sói Nguyền dậy đi!",description=f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không")
                                CurseView = discord.ui.View(timeout=None)
                                async def CurseCallback(interaction:discord.Interaction):
                                    if str(interaction.user.id) in game["alive"]:
                                        if game["role"][str(interaction.user.id)] == "Sói Nguyền":
                                            Curse["check"] = False
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            if game["role"][wwmax] == "Phù Thủy":
                                                WitchDead["check"] = False
                                            game["role"][wwmax] = "Sói Thường"
                                            p = ctx.guild.get_member(int(wwmax))
                                            await interaction.response.send_message(content=f"Nguyền thành công **{p.name}**",ephemeral=True)
                                        else:
                                            await interaction.response.send_message(content="Bạn không phải Sói Nguyền",ephemeral=True)
                                    else:
                                        await interaction.response.send_message(content="Bạn chết rồi, ấn cái gì mà ấn.",ephemeral=True)
                                async def NoCurseCallback(interaction:discord.Interaction):
                                    Curse["NoneCurse"] = True
                                    await interaction.response.send_message(content="Bạn đã từ bỏ nguyền",ephemeral=True)
                                CurseButton = discord.ui.Button(label="Nguyền",style=discord.ButtonStyle.red)
                                NoCurseButton = discord.ui.Button(label="Không Nguyền",style=discord.ButtonStyle.red)
                                CurseButton.callback = CurseCallback
                                NoCurseButton.callback = NoCurseCallback
                                CurseView.add_item(CurseButton)
                                CurseView.add_item(NoCurseButton)
                                CurseMsg = await wereRoom.send(embed=CurseEmbed,view=CurseView)
                                while timer > 0 and Curse["check"] == True and Curse["NoneCurse"] == False:
                                    await asyncio.sleep(1)
                                    timer -= 1
                                    CurseEmbed.description = f"**Thời Gian:** {timer}/30\nHãy quyết định nguyền hay không"
                                    await CurseMsg.edit(embed=CurseEmbed)
                                CurseButton.disabled = True
                                NoCurseButton.disabled = True
                                await CurseMsg.edit(view=CurseView)            
            if "Sói Gây Mê" in game["data"]["werewolf"]:
                timer = 30
                GMe["out"] = 0
                GMEmbed = discord.Embed(title=f"Sói Gây Mê dậy đi! ({timer}/30)",description="Hãy chọn người để gây mê vào sáng hôm sau\n*Nhắc Nhở nho nhỏ: bạn có thể gây mê một người liên tục mấy ngày nếu thấy cần thiết*")
                GMEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                GMView = discord.ui.View(timeout=None)
                async def GMCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Sói Gây Mê":
                            GMCEmb = discord.Embed(title="Chọn người để gây mê")
                            GMCView = discord.ui.View(timeout=None)
                            async def GMChooseCall(inter:discord.Interaction):
                                if GMe["out"] == 0:
                                    p = client.get_guild(guild).get_member(int(GMChoose.values[0]))
                                    GMe["out"] = 1
                                    GMe["Night"] = Night
                                    GMe["Mem"] = GMChoose.values[0]
                                    await inter.response.send_message(content=f"Bạn đã gây mê {p.name}",ephemeral=True)
                                else:
                                    await inter.response.send_message(content="Bạn đã gây mê tối nay",ephemeral=True)
                            GMChoose = discord.ui.Select(placeholder="Chọn người chơi")
                            for x in game["alive"]:
                                p = client.get_guild(guild).get_member(int(x))
                                GMChoose.add_option(label=f"{p.name}",value=p.id)
                            GMChoose.callback = GMChooseCall
                            GMCView.add_item(GMChoose)
                            GMCEmb.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                            await interaction.response.send_message(embed=GMCEmb,view=GMCView,ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Sói Gây Mê",ephemeral=True)
                    else:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                async def NoGMCallback(interaction:discord.Interaction):
                        if str(interaction.user.id) in game["alive"]:
                            if game["role"][str(interaction.user.id)] == "Sói Gây Mê":
                                GMe["out"] = 1
                                await interaction.response.send_message(content="Bạn đã bỏ qua",ephemeral=True)
                            else:
                                await interaction.response.send_message(content="Bạn không phải Sói Gây Mê",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                GMButton = discord.ui.Button(label="Gây Mê",style=discord.ButtonStyle.blurple)
                NoGMButton = discord.ui.Button(label="Bỏ Qua",style=discord.ButtonStyle.green)
                GMView.add_item(GMButton)
                GMView.add_item(NoGMButton)
                GMButton.callback = GMCallback
                NoGMButton.callback = NoGMCallback
                GMMsg = await wereRoom.send(embed=GMEmbed,view=GMView)
                while timer > 0 and GMe["out"] == 0:
                    await asyncio.sleep(1)
                    timer -= 1
                    GMEmbed.title = f"Sói Gây Mê dậy đi! ({timer}/30)"
                    await GMMsg.edit(embed=GMEmbed)
                GMButton.disabled = True
                NoGMButton.disabled = True
                await GMMsg.edit(view=GMView)
            if "Phù Thủy" in game["data"]["villager"] and Night == 1:
                Witch = {}
                Witch["live_bottle"] = 1
                Witch["dead_bottle"] = 1
                Witch["None"] = 0
                Witch["Do"] = 0
                timer = 30
                WitchEmbed = discord.Embed(color=0xB900FF,title=f"Phù Thủy Dậy Đi! ({timer}/30)")
                WitchEmbed.set_image(url="https://media.istockphoto.com/vectors/witch-silhouette-vector-id588968400?k=20&m=588968400&s=612x612&w=0&h=3PxlAWFM-qViBpTkzwNDOHFTacygDfd0GsqMjlJD-z4=")
                WitchEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                WitchView = discord.ui.View(timeout=None)
                async def LiveCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            LiveEmbed = discord.Embed(title="Người Sẽ Bị Giết Hôm Nay:")
                            LiveView = discord.ui.View(timeout=None)
                            if "Bảo Vệ" in data["villager"]:
                                if wwmax == str(game["protect"]) or wwmax == wwcount or wwmax == None:
                                    LiveEmbed.description = "Không Có Ai Chết"
                                else:
                                    p = ctx.guild.get_member(int(wwmax))
                                    LiveEmbed.description = f"**{p.name}**"
                                    async def SaveCallback(inter:discord.Interaction):
                                        if Witch["live_bottle"] == 1:
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            Witch["live_bottle"] = 0
                                            Witch["Do"] = 1
                                            await inter.response.send_message(content="Cứu thành công",ephemeral=True)
                                        elif Witch["live_bottle"] == 0:
                                            await inter.response.send_message(content="Bạn đã hết bình cứu người",ephemeral=True)
                                    SaveButton = discord.ui.Button(label="Cứu Người",style=discord.ButtonStyle.green)
                                    SaveButton.callback = SaveCallback
                                    LiveView.add_item(SaveButton)
                            else:
                                if wwmax == wwcount or wwmax == None:
                                    LiveEmbed.description = "Không Có Ai Chết"
                                else:
                                    p = ctx.guild.get_member(int(wwmax))
                                    LiveEmbed.description = f"**{p.name}**"
                                    async def SaveCallback(inter:discord.Interaction):
                                        if Witch["live_bottle"] == 1:
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            Witch["live_bottle"] = 0
                                            Witch["Do"] = 1
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            await inter.response.send_message(content="Cứu thành công",ephemeral=True)
                                        elif Witch["live_bottle"] == 0:
                                            await inter.response.send_message(content="Bạn đã hết bình cứu người",ephemeral=True)
                                    SaveButton = discord.ui.Button(label="Cứu Người",style=discord.ButtonStyle.green)
                                    SaveButton.callback = SaveCallback
                                    LiveView.add_item(SaveButton)
                            LiveEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                            await interaction.response.send_message(embed=LiveEmbed,view=LiveView,ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                    elif not WitchDead["check"]:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                    elif WitchDead["check"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            LiveEmbed = discord.Embed(title="Người Sẽ Bị Giết Hôm Nay:")
                            LiveView = discord.ui.View(timeout=None)
                            if "Bảo Vệ" in data["villager"]:
                                if wwmax == str(game["protect"]) or wwmax == wwcount or wwmax == None:
                                    LiveEmbed.description = "Không Có Ai Chết"
                                else:
                                    p = ctx.guild.get_member(int(wwmax))
                                    LiveEmbed.description = f"**{p.name}**"
                                    async def SaveCallback(inter:discord.Interaction):
                                        if Witch["live_bottle"] == 1:
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            Witch["live_bottle"] = 0
                                            Witch["Do"] = 1
                                            await inter.response.send_message(content="Cứu thành công",ephemeral=True)
                                        elif Witch["live_bottle"] == 0:
                                            await inter.response.send_message(content="Bạn đã hết bình cứu người",ephemeral=True)
                                    SaveButton = discord.ui.Button(label="Cứu Người",style=discord.ButtonStyle.green)
                                    SaveButton.callback = SaveCallback
                                    LiveView.add_item(SaveButton)
                            else:
                                if wwmax == wwcount or wwmax == None:
                                    LiveEmbed.description = "Không Có Ai Chết"
                                else:
                                    p = ctx.guild.get_member(int(wwmax))
                                    LiveEmbed.description = f"**{p.name}**"
                                    async def SaveCallback(inter:discord.Interaction):
                                        if Witch["live_bottle"] == 1:
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            Witch["live_bottle"] = 0
                                            Witch["Do"] = 1
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            await inter.response.send_message(content="Cứu thành công",ephemeral=True)
                                        elif Witch["live_bottle"] == 0:
                                            await inter.response.send_message(content="Bạn đã hết bình cứu người",ephemeral=True)
                                    SaveButton = discord.ui.Button(label="Cứu Người",style=discord.ButtonStyle.green)
                                    SaveButton.callback = SaveCallback
                                    LiveView.add_item(SaveButton)
                            LiveEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                            await interaction.response.send_message(embed=LiveEmbed,view=LiveView,ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                async def DeadCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            if Witch["dead_bottle"] == 1:
                                DeadEmbed = discord.Embed(title="Hãy chọn giết một người",description="*Nhắc nhỏ nè, nếu thấy mình vô dụng quá thì tự ném chết chính mình được á*")
                                DeadEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                                DeadView = discord.ui.View(timeout=None)
                                DeadSelect = discord.ui.Select(placeholder="Chọn một người để giết")
                                async def DeadSelCallback(inter:discord.Interaction):
                                    play = ctx.guild.get_member(int(DeadSelect.values[0]))
                                    game["alive"].pop(str(DeadSelect.values[0]))
                                    game["dead"].append(str(DeadSelect.values[0]))
                                    Witch["dead_bottle"] = 0
                                    Witch["Do"] = 1
                                    if game["role"][str(DeadSelect.values[0])] == "Thợ Săn":
                                        TSd["selfDead"] = 1
                                    await inter.response.send_message(content=f"Đã độc chết {play.name}",ephemeral=True)
                                for x in game["alive"]:
                                    p = ctx.guild.get_member(int(x))
                                    DeadSelect.add_option(label=f"{p.name}",value=p.id)
                                DeadView.add_item(DeadSelect)
                                DeadSelect.callback = DeadSelCallback
                                await interaction.response.send_message(embed=DeadEmbed,view=DeadView,ephemeral=True)
                            elif Witch["dead_bottle"] == 0:
                                await interaction.response.send_message(content="Bạn đã hết bình độc",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                    elif not WitchDead["check"]:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                    elif WitchDead["check"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            if Witch["dead_bottle"] == 1:
                                DeadEmbed = discord.Embed(title="Hãy chọn giết một người",description="*Nhắc nhỏ nè, nếu thấy mình vô dụng quá thì tự ném chết chính mình được á*")
                                DeadEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                                DeadView = discord.ui.View(timeout=None)
                                DeadSelect = discord.ui.Select(placeholder="Chọn một người để giết")
                                async def DeadSelCallback(inter:discord.Interaction):
                                    play = ctx.guild.get_member(int(DeadSelect.values[0]))
                                    game["alive"].pop(str(DeadSelect.values[0]))
                                    game["dead"].append(str(DeadSelect.values[0]))
                                    Witch["dead_bottle"] = 0
                                    Witch["Do"] = 1
                                    if game["role"][str(DeadSelect.values[0])] == "Thợ Săn":
                                        TSd["selfDead"] = 1
                                    await inter.response.send_message(content=f"Đã độc chết {play.name}",ephemeral=True)
                                for x in game["alive"]:
                                    p = ctx.guild.get_member(int(x))
                                    DeadSelect.add_option(label=f"{p.name}",value=p.id)
                                DeadView.add_item(DeadSelect)
                                DeadSelect.callback = DeadSelCallback
                                await interaction.response.send_message(embed=DeadEmbed,view=DeadView,ephemeral=True)
                            elif Witch["dead_bottle"] == 0:
                                await interaction.response.send_message(content="Bạn đã hết bình độc",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                async def NoneCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            Witch["None"] = 1
                            await interaction.response.send_message(content="Bạn đã từ bỏ lựa chọn",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                    elif not WitchDead["check"]:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                    elif WitchDead["check"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            Witch["None"] = 1
                            await interaction.response.send_message(content="Bạn đã từ bỏ lựa chọn",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                LiveButton = discord.ui.Button(label="Cứu người",style=discord.ButtonStyle.green)
                DeadButton = discord.ui.Button(label="Giết người",style=discord.ButtonStyle.red)
                NoneButton = discord.ui.Button(label="Bỏ Qua",style=discord.ButtonStyle.green)
                LiveButton.callback = LiveCallback
                DeadButton.callback = DeadCallback
                NoneButton.callback = NoneCallback
                WitchView.add_item(LiveButton)
                WitchView.add_item(DeadButton)
                WitchView.add_item(NoneButton)
                WitchMsg = await vilRoom.send(embed=WitchEmbed,view=WitchView)
                while timer > 0 and Witch["None"] == 0 and Witch["Do"] == 0:
                    await asyncio.sleep(1)
                    timer -= 1
                    WitchEmbed.title=f"Phù Thủy Dậy Đi! ({timer}/30)"
                    await WitchMsg.edit(embed=WitchEmbed)
                LiveButton.disabled = True
                DeadButton.disabled = True
                NoneButton.disabled = True
                await WitchMsg.edit(view=WitchView)
                WitchDead["check"] = False
            elif "Phù Thủy" in game["data"]["villager"] and Night != 1:
                Witch["None"] = 0
                Witch["Do"] = 0
                timer = 30
                WitchEmbed = discord.Embed(color=0xB900FF,title=f"Phù Thủy Dậy Đi! ({timer}/30)")
                WitchEmbed.set_image(url="https://media.istockphoto.com/vectors/witch-silhouette-vector-id588968400?k=20&m=588968400&s=612x612&w=0&h=3PxlAWFM-qViBpTkzwNDOHFTacygDfd0GsqMjlJD-z4=")
                WitchEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                WitchView = discord.ui.View(timeout=None)
                async def LiveCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            LiveEmbed = discord.Embed(title="Người Sẽ Bị Giết Hôm Nay:")
                            LiveView = discord.ui.View(timeout=None)
                            if "Bảo Vệ" in game["data"]["villager"]:
                                if wwmax == str(game["protect"]) or wwmax == wwcount or wwmax == None:
                                    LiveEmbed.description = "Không Có Ai Chết"
                                else:
                                    p = ctx.guild.get_member(int(wwmax))
                                    LiveEmbed.description = f"**{p.name}**"
                                    async def SaveCallback(inter:discord.Interaction):
                                        if Witch["live_bottle"] == 1:
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            Witch["live_bottle"] = 0
                                            Witch["Do"] = 1
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            await inter.response.send_message(content="Cứu thành công",ephemeral=True)
                                        elif Witch["live_bottle"] == 0:
                                            await inter.response.send_message(content="Bạn đã hết bình cứu người",ephemeral=True)
                                    SaveButton = discord.ui.Button(label="Cứu Người",style=discord.ButtonStyle.green)
                                    SaveButton.callback = SaveCallback
                                    LiveView.add_item(SaveButton)
                            else:
                                if wwmax == wwcount or wwmax == None:
                                    LiveEmbed.description = "Không Có Ai Chết"
                                else:
                                    p = ctx.guild.get_member(int(wwmax))
                                    LiveEmbed.description = f"**{p.name}**"
                                    async def SaveCallback(inter:discord.Interaction):
                                        if Witch["live_bottle"] == 1:
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            Witch["live_bottle"] = 0
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            await inter.response.send_message(content="Cứu thành công",ephemeral=True)
                                        elif Witch["live_bottle"] == 0:
                                            await inter.response.send_message(content="Bạn đã hết bình cứu người",ephemeral=True)
                                    SaveButton = discord.ui.Button(label="Cứu Người",style=discord.ButtonStyle.green)
                                    SaveButton.callback = SaveCallback
                                    LiveView.add_item(SaveButton)
                            LiveEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                            await interaction.response.send_message(embed=LiveEmbed,view=LiveView,ephemeral=True)
                        await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                    elif not WitchDead["check"]:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                    elif WitchDead["check"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            LiveEmbed = discord.Embed(title="Người Sẽ Bị Giết Hôm Nay:")
                            LiveView = discord.ui.View(timeout=None)
                            if "Bảo Vệ" in game["data"]["villager"]:
                                if wwmax == str(game["protect"]) or wwmax == wwcount or wwmax == None:
                                    LiveEmbed.description = "Không Có Ai Chết"
                                else:
                                    p = ctx.guild.get_member(int(wwmax))
                                    LiveEmbed.description = f"**{p.name}**"
                                    async def SaveCallback(inter:discord.Interaction):
                                        if Witch["live_bottle"] == 1:
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            Witch["live_bottle"] = 0
                                            Witch["Do"] = 1
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            await inter.response.send_message(content="Cứu thành công",ephemeral=True)
                                        elif Witch["live_bottle"] == 0:
                                            await inter.response.send_message(content="Bạn đã hết bình cứu người",ephemeral=True)
                                    SaveButton = discord.ui.Button(label="Cứu Người",style=discord.ButtonStyle.green)
                                    SaveButton.callback = SaveCallback
                                    LiveView.add_item(SaveButton)
                            else:
                                if wwmax == wwcount or wwmax == None:
                                    LiveEmbed.description = "Không Có Ai Chết"
                                else:
                                    p = ctx.guild.get_member(int(wwmax))
                                    LiveEmbed.description = f"**{p.name}**"
                                    async def SaveCallback(inter:discord.Interaction):
                                        if Witch["live_bottle"] == 1:
                                            game["alive"][wwmax] = []
                                            game["dead"].remove(wwmax)
                                            Witch["live_bottle"] = 0
                                            if game["role"][wwmax] == "Thợ Săn":
                                                TSd["selfDead"] = None
                                            await inter.response.send_message(content="Cứu thành công",ephemeral=True)
                                        elif Witch["live_bottle"] == 0:
                                            await inter.response.send_message(content="Bạn đã hết bình cứu người",ephemeral=True)
                                    SaveButton = discord.ui.Button(label="Cứu Người",style=discord.ButtonStyle.green)
                                    SaveButton.callback = SaveCallback
                                    LiveView.add_item(SaveButton)
                            LiveEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                            await interaction.response.send_message(embed=LiveEmbed,view=LiveView,ephemeral=True)
                        await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                async def DeadCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            if Witch["dead_bottle"] == 1:
                                DeadEmbed = discord.Embed(title="Hãy chọn giết một người",description="*Nhắc nhỏ nè, nếu thấy mình vô dụng quá thì tự ném chết chính mình được á*")
                                DeadEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                                DeadView = discord.ui.View(timeout=None)
                                DeadSelect = discord.ui.Select(placeholder="Chọn một người để giết")
                                async def DeadSelCallback(inter:discord.Interaction):
                                    play = ctx.guild.get_member(int(DeadSelect.values[0]))
                                    game["alive"].pop(str(DeadSelect.values[0]))
                                    game["dead"].append(str(DeadSelect.values[0]))
                                    Witch["dead_bottle"] = 0
                                    Witch["Do"] = 1
                                    if game["role"][str(DeadSelect.values[0])] == "Thợ Săn":
                                        TSd["selfDead"] = 1
                                    await inter.response.send_message(content=f"Đã độc chết {play.name}",ephemeral=True)
                                for x in game["alive"]:
                                    p = ctx.guild.get_member(int(x))
                                    DeadSelect.add_option(label=f"{p.name}",value=p.id)
                                DeadView.add_item(DeadSelect)
                                DeadSelect.callback = DeadSelCallback
                                await interaction.response.send_message(embed=DeadEmbed,view=DeadView,ephemeral=True)
                            elif Witch["dead_bottle"] == 0:
                                await interaction.response.send_message(content="Bạn đã hết bình độc",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                    elif not WitchDead["check"]:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                    elif WitchDead["check"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            if Witch["dead_bottle"] == 1:
                                DeadEmbed = discord.Embed(title="Hãy chọn giết một người",description="*Nhắc nhỏ nè, nếu thấy mình vô dụng quá thì tự ném chết chính mình được á*")
                                DeadEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
                                DeadView = discord.ui.View(timeout=None)
                                DeadSelect = discord.ui.Select(placeholder="Chọn một người để giết")
                                async def DeadSelCallback(inter:discord.Interaction):
                                    play = ctx.guild.get_member(int(DeadSelect.values[0]))
                                    game["alive"].pop(str(DeadSelect.values[0]))
                                    game["dead"].append(str(DeadSelect.values[0]))
                                    Witch["dead_bottle"] = 0
                                    Witch["Do"] = 1
                                    if game["role"][str(DeadSelect.values[0])] == "Thợ Săn":
                                        TSd["selfDead"] = 1
                                    await inter.response.send_message(content=f"Đã độc chết {play.name}",ephemeral=True)
                                for x in game["alive"]:
                                    p = ctx.guild.get_member(int(x))
                                    DeadSelect.add_option(label=f"{p.name}",value=p.id)
                                DeadView.add_item(DeadSelect)
                                DeadSelect.callback = DeadSelCallback
                                await interaction.response.send_message(embed=DeadEmbed,view=DeadView,ephemeral=True)
                            elif Witch["dead_bottle"] == 0:
                                await interaction.response.send_message(content="Bạn đã hết bình độc",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                async def NoneCallback(interaction:discord.Interaction):
                    if str(interaction.user.id) in game["alive"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            Witch["None"] = 1
                            await interaction.response.send_message(content="Bạn đã từ bỏ lựa chọn",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                    elif not WitchDead["check"]:
                        await interaction.response.send_message(content="Bạn chết rồi, ấn sao được mà ấn",ephemeral=True)
                    elif WitchDead["check"]:
                        if game["role"][str(interaction.user.id)] == "Phù Thủy":
                            Witch["None"] = 1
                            await interaction.response.send_message(content="Bạn đã từ bỏ lựa chọn",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="Bạn không phải Phù Thủy",ephemeral=True)
                LiveButton = discord.ui.Button(label="Cứu người",style=discord.ButtonStyle.green)
                DeadButton = discord.ui.Button(label="Giết người",style=discord.ButtonStyle.red)
                NoneButton = discord.ui.Button(label="Bỏ Qua",style=discord.ButtonStyle.green)
                LiveButton.callback = LiveCallback
                DeadButton.callback = DeadCallback
                NoneButton.callback = NoneCallback
                WitchView.add_item(LiveButton)
                WitchView.add_item(DeadButton)
                WitchView.add_item(NoneButton)
                WitchMsg = await vilRoom.send(embed=WitchEmbed,view=WitchView)
                while timer > 0 and Witch["None"] == 0 and Witch["Do"] == 0:
                    await asyncio.sleep(1)
                    timer -= 1
                    WitchEmbed.title=f"Phù Thủy Dậy Đi! ({timer}/30)"
                    await WitchMsg.edit(embed=WitchEmbed)
                LiveButton.disabled = True
                DeadButton.disabled = True
                NoneButton.disabled = True
                await WitchMsg.edit(view=WitchView)
                WitchDead["check"] = False

