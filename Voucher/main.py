import discord
from discord.ext import commands
import matplotlib as mpl
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
import aiosqlite
import json
import datetime
import asyncio
from PIL import Image, ImageEnhance, ImageDraw, ImageOps, ImageFont
from easy_pil import load_image_async,Editor
from Voucher.config import channel as chan
import math
from Voucher.reset_database import reset_dtb

def Vouching(client: commands.Bot):
    @client.event
    async def on_ready():
        print(f"{client.user} is ready!")
        async with aiosqlite.connect("Voucher/main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER , info JSON)')
                await cursor.execute('CREATE TABLE IF NOT EXISTS vouch (id INTEGER , info JSON)')
            await db.commit()
        await client.tree.sync()
            
    VouchCooldown = {}
    VCooldown = {}
            
    @client.tree.command(name="vouch",description="Vouch member")
    async def vouch(interaction: discord.Interaction, member:discord.Member, reason: str, image: discord.Attachment):
        if member.bot:
            await interaction.response.send_message("❌ | You cannot vote bots!")
        elif not interaction.user.bot:
            async with aiosqlite.connect("Voucher/main.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                    data = await cursor.fetchone()
                    if data:
                        d = str(data)[2:-3]
                        info = json.loads(d.replace("\'","\""))
                        channel = chan
                        if channel != None:
                            try:
                                VouchCooldown[str(interaction.user.id)]
                            except:
                                VouchCooldown[str(interaction.user.id)] = 0
                            if VouchCooldown[str(interaction.user.id)] == 0:
                                Checker = False
                                if datetime.datetime.now().strftime("%Y") == interaction.user.created_at.strftime("%Y"):
                                    if (int(datetime.datetime.now().strftime("%m")) - int(interaction.user.created_at.strftime("%m")) < 5) and (int(datetime.datetime.now().strftime("%m")) - int(member.created_at.strftime("%m")) < 5):
                                        Checker = True
                                elif int(datetime.datetime.now().strftime("%Y")) == (int(interaction.user.created_at.strftime("%Y"))+1):
                                    if int(datetime.datetime.now().strftime("%m")) < 5:
                                        Checker = True
                                    elif (int(datetime.datetime.now().strftime("%m")) + (12-int(interaction.user.created_at.strftime("%m")))) < 5:
                                        Checker = True
                                else:
                                    Checker = True
                                if Checker:
                                    await interaction.response.send_message(content="✔️ | Submit Vouch Request Successfully, It Will Be Considered",ephemeral=True) 
                                    embed = discord.Embed(title=f"{interaction.user} Vouch Request Sent To {member}",description=f"**Content:** {reason}\n**Image:**")
                                    embed.set_image(url=image.url)
                                    view = discord.ui.View(timeout=None)
                                    YesButton = discord.ui.Button(label="Accept",style=discord.ButtonStyle.green,emoji="<:Accept:1027947834386956350>")
                                    NoButton = discord.ui.Button(label="Deny",style=discord.ButtonStyle.red,emoji="<:deny:1027947850258186313>")
                                    async def YesCallback(inter:discord.Interaction):
                                        async with aiosqlite.connect("Voucher/main.db") as db:
                                            async with db.cursor() as cursor:
                                                info["vouch"] += 1
                                                Daydate = datetime.datetime.now().strftime("%d/%m/%Y")
                                                Monthdate = datetime.datetime.now().strftime("%m/%Y")
                                                await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                                                vouch = await cursor.fetchone()
                                                d = str(vouch)[2:-3]
                                                vouchi = json.loads(d.replace("\'","\""))
                                                try:
                                                    info["vouch_month"][str(Monthdate)] += 1
                                                except:
                                                    info["vouch_month"][str(Monthdate)] = 1
                                                    info["unvouch_month"][str(Monthdate)] = 0
                                                try:
                                                    info["vouch_day"][str(Daydate)] += 1
                                                    vouchi[str(Daydate)]["type"].append("vouch")
                                                    vouchi[str(Daydate)]["voucher"].append(interaction.user.id)
                                                    vouchi[str(Daydate)]["reason"].append(reason)
                                                    vouchi[str(Daydate)]["accept"].append(inter.user.id)
                                                    vouchi[str(Daydate)]["image"].append(image.url)
                                                except:
                                                    info["vouch_day"][str(Daydate)] = 1
                                                    info["unvouch_day"][str(Daydate)] = 0
                                                    vouchi[str(Daydate)] = {}
                                                    vouchi[str(Daydate)]["type"] = "vouch"
                                                    vouchi[str(Daydate)]["voucher"]= interaction.user.id
                                                    vouchi[str(Daydate)]["reason"] = reason
                                                    vouchi[str(Daydate)]["accept"] = inter.user.id
                                                    vouchi[str(Daydate)]["image"] = image.url
                                                js = json.dumps(info)
                                                await cursor.execute('UPDATE users SET info = ? WHERE id = ?',(js,member.id,))
                                                vs = json.dumps(vouchi)
                                                await cursor.execute('UPDATE vouch SET info = ? WHERE id = ?',(vs,member.id,))
                                            await db.commit()        
                                        YesButton.style = discord.ButtonStyle.green
                                        YesButton.disabled = True
                                        NoButton.disabled = True
                                        await Msg.edit(view=view)
                                        await inter.response.send_message(ephemeral=True,content="✔️ | You Have Browsed Successfully!")
                                    async def NoCallback(inter:discord.Interaction):
                                        NoButton.style = discord.ButtonStyle.green
                                        YesButton.disabled = True
                                        NoButton.disabled = True
                                        await Msg.edit(view=view)
                                        await inter.response.send_message(ephemeral=True,content="Từ chối ✔️ | Request Sent Successfully, It Needs Approval")
                                    view.add_item(YesButton)
                                    YesButton.callback = YesCallback
                                    view.add_item(NoButton)
                                    NoButton.callback = NoCallback
                                    Msg = await client.get_channel(int(channel)).send(embed=embed,view=view)
                                    VouchCooldown[str(interaction.user.id)] = 24
                                else:
                                    await interaction.response.send_message(ephemeral=True,content="Vouch thành công!")
                                    dat = {}
                                    async with aiosqlite.connect("Voucher/main.db") as db:
                                        async with db.cursor() as cursor:
                                            info["vouch"] += 1
                                            Daydate = datetime.datetime.now().strftime("%d/%m/%Y")
                                            Monthdate = datetime.datetime.now().strftime("%m/%Y")
                                            dat["day"] = Daydate
                                            dat["month"] = Monthdate
                                            await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                                            vouch = await cursor.fetchone()
                                            d = str(vouch)[2:-3]
                                            vouchi = json.loads(d.replace("\'","\""))
                                            try:
                                                info["vouch_month"][str(Monthdate)] += 1
                                            except:
                                                info["vouch_month"][str(Monthdate)] = 1
                                                info["unvouch_month"][str(Monthdate)] = 0
                                            try:
                                                info["vouch_day"][str(Daydate)] += 1
                                                vouchi[str(Daydate)]["type"].append("vouch")
                                                vouchi[str(Daydate)]["voucher"].append(interaction.user.id)
                                                vouchi[str(Daydate)]["reason"].append(reason)
                                                vouchi[str(Daydate)]["accept"].append(client.user.id)
                                                vouchi[str(Daydate)]["image"].append(image.url)
                                            except:
                                                info["vouch_day"][str(Daydate)] = 1
                                                info["unvouch_day"][str(Daydate)] = 0
                                                vouchi[str(Daydate)] = {}
                                                vouchi[str(Daydate)]["type"] = "vouch"
                                                vouchi[str(Daydate)]["voucher"]= interaction.user.id
                                                vouchi[str(Daydate)]["reason"] = reason
                                                vouchi[str(Daydate)]["accept"] = client.user.id
                                                vouchi[str(Daydate)]["image"] = image.url
                                            dat["index"] = len(vouchi[str(Daydate)]["type"]) - 1
                                            js = json.dumps(info)
                                            vs = json.dumps(vouchi)
                                            await cursor.execute('UPDATE users SET info = ? WHERE id = ?',(js,member.id,))
                                            await cursor.execute('UPDATE vouch SET info = ? WHERE id = ?',(vs,member.id,))
                                        await db.commit()    
                                    embed = discord.Embed(title=f"{interaction.user} đã xin vouch {member}",description=f"**Lý do:** {reason}")
                                    embed.set_image(url=image.url)
                                    view = discord.ui.View(timeout=None)
                                    async def HuyCallback(inter:discord.Interaction):
                                        HuyButton.style = discord.ButtonStyle.green
                                        HuyButton.disabled = True
                                        await Msg.edit(view=view)
                                        async with aiosqlite.connect("Voucher/main.db") as db:
                                                async with db.cursor() as cursor:
                                                    await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                                                    data = await cursor.fetchone()
                                                    d = str(data)[2:-3]
                                                    info = json.loads(d.replace("\'","\""))
                                                    info["vouch"] -= 1
                                                    info["vouch_day"][str(dat["day"])] -= 1
                                                    info["vouch_month"][str(dat["month"])] -= 1
                                                    await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                                                    vouch = await cursor.fetchone()
                                                    d = str(vouch)[2:-3]
                                                    vi = json.loads(d.replace("\'","\""))
                                                    for x in vi[str(dat["day"])]:
                                                        vi[str(dat["day"])][x].pop(dat["index"])
                                                    js = json.dumps(info)
                                                    vs = json.dumps(vi)
                                                    await cursor.execute('UPDATE users SET info = ? WHERE id = ?',(js,member.id,))
                                                    await cursor.execute('UPDATE vouch SET info = ? WHERE id = ?',(vs,member.id,))
                                                await db.commit()
                                        await inter.response.send_message(ephemeral=True,content="Đã hủy devouch!")
                                    HuyButton = discord.ui.Button(label="Hủy",style=discord.ButtonStyle.gray)
                                    view.add_item(HuyButton)
                                    HuyButton.callback = HuyCallback
                                    Msg = await client.get_channel(int(channel)).send(embed=embed,view=view)  
                                    VouchCooldown[str(interaction.user.id)] = 24
                            else:
                                await interaction.response.send_message(content="❌ | You have reached the limit!, you can only vouch/devouch once a day./..",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="❌ | Bot Has Unknown Problem...",ephemeral=True)
                    else:
                        channel = chan
                        if channel != None:
                            try:
                                VouchCooldown[str(interaction.user.id)]
                            except:
                                VouchCooldown[str(interaction.user.id)] = 0
                            if VouchCooldown[str(interaction.user.id)] == 0:
                                Checker = False
                                if datetime.datetime.now().strftime("%Y") == interaction.user.created_at.strftime("%Y"):
                                    if (int(datetime.datetime.now().strftime("%m")) - int(interaction.user.created_at.strftime("%m")) < 5) and (int(datetime.datetime.now().strftime("%m")) - int(member.created_at.strftime("%m")) < 5):
                                        Checker = True
                                elif int(datetime.datetime.now().strftime("%Y")) == (int(interaction.user.created_at.strftime("%Y"))+1):
                                    if int(datetime.datetime.now().strftime("%m")) < 5:
                                        Checker = True
                                    elif (int(datetime.datetime.now().strftime("%m")) + (12-int(interaction.user.created_at.strftime("%m")))) < 5:
                                        Checker = True
                                else:
                                    Checker = True
                                if Checker:
                                    await interaction.response.send_message(content="✔️ | Submit Vouch Request Successfully, It Will Be Considered",ephemeral=True) 
                                    embed = discord.Embed(title=f"{interaction.user} đã xin vouch {member}",description=f"**Lý do:** {reason}")
                                    embed.set_image(url=image.url)
                                    view = discord.ui.View(timeout=None)
                                    YesButton = discord.ui.Button(label="Accept",style=discord.ButtonStyle.green,emoji="<:Accept:1027947834386956350>")
                                    NoButton = discord.ui.Button(label="Deny",style=discord.ButtonStyle.red,emoji="<:deny:1027947850258186313>")
                                    async def YesCallback(inter:discord.Interaction):
                                        async with aiosqlite.connect("Voucher/main.db") as db:
                                            async with db.cursor() as cursor:
                                                Daydate = datetime.datetime.now().strftime("%d/%m/%Y")
                                                Monthdate = datetime.datetime.now().strftime("%m/%Y")
                                                j = {"vouch": 1, "unvouch": 0,"vouch_day": {f"{Daydate}":1},"unvouch_day": {f"{Daydate}":0},"vouch_month":{f"{Monthdate}":1},"unvouch_month":{f"{Monthdate}":0}}
                                                js = json.dumps(j)
                                                v = {f"{Daydate}":{"type":["vouch"],"voucher":[interaction.user.id],"reason":[reason],"accept":[inter.user.id],"image":[image.url]}}
                                                vs = json.dumps(v)
                                                await cursor.execute('INSERT INTO users (info, id) VALUES (?, ?)',(js,member.id,))
                                                await cursor.execute('INSERT INTO vouch (info, id) VALUES (?, ?)',(vs,member.id,))
                                                YesButton.style = discord.ButtonStyle.green
                                                YesButton.disabled = True
                                                NoButton.disabled = True
                                                await Msg.edit(view=view)
                                                await inter.response.send_message(ephemeral=True,content="✔️ | You Have Browsed Successfully!")
                                            await db.commit()   
                                    async def NoCallback(inter:discord.Interaction):
                                        NoButton.style = discord.ButtonStyle.green
                                        YesButton.disabled = True
                                        NoButton.disabled = True
                                        await Msg.edit(view=view)
                                        await inter.response.send_message(ephemeral=True,content="✔️ | Successfully refused to vote!")
                                    view.add_item(YesButton)
                                    YesButton.callback = YesCallback
                                    view.add_item(NoButton)
                                    NoButton.callback = NoCallback
                                    Msg = await client.get_channel(int(channel)).send(embed=embed,view=view)      
                                    VouchCooldown[str(interaction.user.id)] = 24
                                else:
                                    await interaction.response.send_message(ephemeral=True,content="✔️ | Request Sent Successfully, It Needs Approval")
                                    dat = {}
                                    async with aiosqlite.connect("Voucher/main.db") as db:
                                        async with db.cursor() as cursor:
                                            Daydate = datetime.datetime.now().strftime("%d/%m/%Y")
                                            Monthdate = datetime.datetime.now().strftime("%m/%Y")
                                            j = {"vouch": 1, "unvouch": 0, "vouch_day":{f"{Daydate}":1}, "unvouch_day": {f"{Daydate}":0}, "vouch_month":{f"{Monthdate}":1}, "unvouch_month": {f"{Monthdate}":0}}
                                            js = json.dumps(j)
                                            v = {f"{Daydate}":{"type":["vouch"],"voucher":[interaction.user.id],"reason":[reason],"accept":[client.user.id],"image":[image.url]}}
                                            vs = json.dumps(v)
                                            dat["day"] = Daydate
                                            dat["month"] = Monthdate
                                            dat["index"] = 0
                                            await cursor.execute('INSERT INTO users (info, id) VALUES (?, ?)',(js,member.id,))
                                            await cursor.execute('INSERT INTO vouch (info, id) VALUES (?, ?)',(vs,member.id,))
                                        await db.commit()
                                    embed = discord.Embed(title=f"{interaction.user} đã xin vouch {member}",description=f"**Lý do:** {reason}")
                                    embed.set_image(url=image.url)
                                    view = discord.ui.View(timeout=None)
                                    async def HuyCallback(inter:discord.Interaction):
                                        HuyButton.style = discord.ButtonStyle.green
                                        HuyButton.disabled = True
                                        await Msg.edit(view=view)
                                        async with aiosqlite.connect("Voucher/main.db") as db:
                                                async with db.cursor() as cursor:
                                                    await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                                                    data = await cursor.fetchone()
                                                    d = str(data)[2:-3]
                                                    info = json.loads(d.replace("\'","\""))
                                                    info["vouch"] -= 1
                                                    info["vouch_day"][str(dat["day"])] -= 1
                                                    info["vouch_month"][str(dat["month"])] -= 1
                                                    await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                                                    vouch = await cursor.fetchone()
                                                    d = str(vouch)[2:-3]
                                                    vi = json.loads(d.replace("\'","\""))
                                                    for x in vi[str(dat["day"])]:
                                                        vi[str(dat["day"])][x].pop(dat["index"])
                                                    js = json.dumps(info)
                                                    vs = json.dumps(vi)
                                                    await cursor.execute('UPDATE users SET info = ? WHERE id = ?',(js,member.id,))
                                                    await cursor.execute('UPDATE vouch SET info = ? WHERE id = ?',(vs,member.id,))
                                                await db.commit()
                                        await inter.response.send_message(ephemeral=True,content="Đã hủy vouch!")
                                    HuyButton = discord.ui.Button(label="Hủy",style=discord.ButtonStyle.gray)
                                    view.add_item(HuyButton)
                                    HuyButton.callback = HuyCallback
                                    Msg = await client.get_channel(int(channel)).send(embed=embed,view=view)  
                                    VouchCooldown[str(interaction.user.id)] = 24
                            else:
                                await interaction.response.send_message(content="❌ | You have reached the limit!, you can only vouch/devouch once a day./..",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="❌ | Bot Has Unknown Problem...",ephemeral=True)
                try:
                    if VCooldown[str(interaction.user.id)] == 0:
                        VCooldown[str(interaction.user.id)] = 1
                        while VouchCooldown[str(interaction.user.id)] > 0:
                            await asyncio.sleep(3600)
                            VouchCooldown[str(interaction.user.id)] -= 1
                        VCooldown[str(interaction.user.id)] = 0
                    else:
                        pass
                except:
                    VCooldown[str(interaction.user.id)] = 1
                    while VouchCooldown[str(interaction.user.id)] > 0:
                        await asyncio.sleep(3600)
                        VouchCooldown[str(interaction.user.id)] -= 1
                    VCooldown[str(interaction.user.id)] = 0

    @client.tree.command(name="devouch",description="Devouch member")
    async def devouch(interaction: discord.Interaction, member:discord.Member,reason: str, image: discord.Attachment):
        if member.bot:
            await interaction.response.send_message("❌ | You cannot vote bots!",ephemeral=True)
        elif not interaction.user.bot:
            async with aiosqlite.connect("Voucher/main.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                    data = await cursor.fetchone()
                    if data:
                        d = str(data)[2:-3]
                        info = json.loads(d.replace("\'","\""))
                        channel = chan
                        if channel != None:
                            try:
                                VouchCooldown[str(interaction.user.id)]
                            except:
                                VouchCooldown[str(interaction.user.id)] = 0
                            if VouchCooldown[str(interaction.user.id)] == 0:
                                Checker = False
                                if datetime.datetime.now().strftime("%Y") == interaction.user.created_at.strftime("%Y"):
                                    if (int(datetime.datetime.now().strftime("%m")) - int(interaction.user.created_at.strftime("%m")) < 5) and (int(datetime.datetime.now().strftime("%m")) - int(member.created_at.strftime("%m")) < 5):
                                        Checker = True
                                elif int(datetime.datetime.now().strftime("%Y")) == (int(interaction.user.created_at.strftime("%Y"))+1):
                                    if int(datetime.datetime.now().strftime("%m")) < 5:
                                        Checker = True
                                    elif (int(datetime.datetime.now().strftime("%m")) + (12-int(interaction.user.created_at.strftime("%m")))) < 5:
                                        Checker = True
                                else:
                                    Checker = True
                                if Checker:
                                    await interaction.response.send_message(content="✔️ | You Have Browsed Successfully!",ephemeral=True) 
                                    embed = discord.Embed(title=f"{interaction.user} đã xin devouch {member}",description=f"**Lý do:** {reason}")
                                    embed.set_image(url=image.url)
                                    view = discord.ui.View(timeout=None)
                                    YesButton = discord.ui.Button(label="Accept",style=discord.ButtonStyle.green,emoji="<:Accept:1027947834386956350>")
                                    NoButton = discord.ui.Button(label="Deny",style=discord.ButtonStyle.red,emoji="<:deny:1027947850258186313>")

                                    async def YesCallback(inter:discord.Interaction):
                                        async with aiosqlite.connect("Voucher/main.db") as db:
                                            async with db.cursor() as cursor:
                                                info["unvouch"] += 1
                                                Daydate = datetime.datetime.now().strftime("%d/%m/%Y")
                                                Monthdate = datetime.datetime.now().strftime("%m/%Y")
                                                await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                                                vouch = await cursor.fetchone()
                                                d = str(vouch)[2:-3]
                                                vouchi = json.loads(d.replace("\'","\""))
                                                try:
                                                    info["unvouch_month"][str(Monthdate)] += 1
                                                except:
                                                    info["unvouch_month"][str(Monthdate)] = 1
                                                    info["vouch_month"][str(Monthdate)] = 0
                                                try:
                                                    info["unvouch_day"][str(Daydate)] += 1
                                                    vouchi[str(Daydate)]["type"].append("unvouch")
                                                    vouchi[str(Daydate)]["voucher"].append(interaction.user.id)
                                                    vouchi[str(Daydate)]["reason"].append(reason)
                                                    vouchi[str(Daydate)]["accept"].append(inter.user.id)
                                                    vouchi[str(Daydate)]["image"].append(image.url)
                                                except:
                                                    info["unvouch_day"][str(Daydate)] = 1
                                                    info["vouch_day"][str(Daydate)] = 0
                                                    vouchi[str(Daydate)] = {}
                                                    vouchi[str(Daydate)]["type"] = "unvouch"
                                                    vouchi[str(Daydate)]["voucher"]= interaction.user.id
                                                    vouchi[str(Daydate)]["reason"] = reason
                                                    vouchi[str(Daydate)]["accept"] = inter.user.id
                                                    vouchi[str(Daydate)]["image"] = image.url
                                                js = json.dumps(info)
                                                vs = json.dumps(vouchi)
                                                await cursor.execute('UPDATE users SET info = ? WHERE id = ?',(js,member.id,))
                                                await cursor.execute('UPDATE vouch SET info = ? WHERE id = ?',(vs,member.id,))
                                                YesButton.style = discord.ButtonStyle.green
                                                YesButton.disabled = True
                                                NoButton.disabled = True
                                                await Msg.edit(view=view)
                                                await inter.response.send_message(ephemeral=True,content="✔️ | Request Sent Successfully, It Needs Approval")
                                            await db.commit()
                                    async def NoCallback(inter:discord.Interaction):
                                        NoButton.style = discord.ButtonStyle.green
                                        YesButton.disabled = True
                                        NoButton.disabled = True
                                        await Msg.edit(view=view)
                                        await inter.response.send_message(ephemeral=True,content="✔️ | Request Sent Successfully, It Needs Approval")
                                    view.add_item(YesButton)
                                    YesButton.callback = YesCallback
                                    view.add_item(NoButton)
                                    NoButton.callback = NoCallback
                                    Msg = await client.get_channel(int(channel)).send(embed=embed,view=view)
                                    VouchCooldown[str(interaction.user.id)] = 24
                                else:
                                    await interaction.response.send_message(ephemeral=True,content="✔️ | Request Sent Successfully, It Needs Approval")
                                    dat = {}
                                    async with aiosqlite.connect("Voucher/main.db") as db:
                                        async with db.cursor() as cursor:
                                            info["unvouch"] += 1
                                            Daydate = datetime.datetime.now().strftime("%d/%m/%Y")
                                            Monthdate = datetime.datetime.now().strftime("%m/%Y")
                                            dat["day"] = Daydate
                                            dat["month"] = Monthdate
                                            await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                                            vouch = await cursor.fetchone()
                                            d = str(vouch)[2:-3]
                                            vouchi = json.loads(d.replace("\'","\""))
                                            try:
                                                info["unvouch_month"][str(Monthdate)] += 1
                                            except:
                                                info["unvouch_month"][str(Monthdate)] = 1
                                                info["vouch_month"][str(Monthdate)] = 0
                                            try:
                                                info["unvouch_day"][str(Daydate)] += 1
                                                vouchi[str(Daydate)]["type"].append("unvouch")
                                                vouchi[str(Daydate)]["voucher"].append(interaction.user.id)
                                                vouchi[str(Daydate)]["reason"].append(reason)
                                                vouchi[str(Daydate)]["accept"].append(client.user.id)
                                                vouchi[str(Daydate)]["image"].append(image.url)
                                            except:
                                                info["unvouch_day"][str(Daydate)] = 1
                                                info["vouch_day"][str(Daydate)] = 0
                                                vouchi[str(Daydate)] = {}
                                                vouchi[str(Daydate)]["type"] = "unvouch"
                                                vouchi[str(Daydate)]["voucher"]= interaction.user.id
                                                vouchi[str(Daydate)]["reason"] = reason
                                                vouchi[str(Daydate)]["accept"] = client.user.id
                                                vouchi[str(Daydate)]["image"] = image.url
                                            dat["index"] = len(vouchi[str(Daydate)]["type"]) - 1
                                            js = json.dumps(info)
                                            vs = json.dumps(vouchi)
                                            await cursor.execute('UPDATE users SET info = ? WHERE id = ?',(js,member.id,))
                                            await cursor.execute('UPDATE vouch SET info = ? WHERE id = ?',(vs,member.id,))
                                        await db.commit()
                                    embed = discord.Embed(title=f"{interaction.user} đã xin devouch {member}",description=f"**Lý do:** {reason}")
                                    embed.set_image(url=image.url)
                                    view = discord.ui.View(timeout=None)
                                    async def HuyCallback(inter:discord.Interaction):
                                        HuyButton.style = discord.ButtonStyle.green
                                        HuyButton.disabled = True
                                        await Msg.edit(view=view)
                                        async with aiosqlite.connect("Voucher/main.db") as db:
                                                async with db.cursor() as cursor:
                                                    await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                                                    data = await cursor.fetchone()
                                                    d = str(data)[2:-3]
                                                    info = json.loads(d.replace("\'","\""))
                                                    info["unvouch"] -= 1
                                                    info["unvouch_day"][str(dat["day"])] -= 1
                                                    info["unvouch_month"][str(dat["month"])] -= 1
                                                    await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                                                    vouch = await cursor.fetchone()
                                                    d = str(vouch)[2:-3]
                                                    vi = json.loads(d.replace("\'","\""))
                                                    for x in vi[str(dat["day"])]:
                                                        vi[str(dat["day"])][x].pop(dat["index"])
                                                    js = json.dumps(info)
                                                    vs = json.dumps(vi)
                                                    await cursor.execute('UPDATE users SET info = ? WHERE id = ?',(js,member.id,))
                                                    await cursor.execute('UPDATE vouch SET info = ? WHERE id = ?',(vs,member.id,))
                                                await db.commit()
                                        await inter.response.send_message(ephemeral=True,content="Đã hủy devouch!")
                                    HuyButton = discord.ui.Button(label="Hủy",style=discord.ButtonStyle.gray)
                                    view.add_item(HuyButton)
                                    HuyButton.callback = HuyCallback
                                    Msg = await client.get_channel(int(channel)).send(embed=embed,view=view)  
                                    VouchCooldown[str(interaction.user.id)] = 24
                            else:
                                await interaction.response.send_message(content="❌ | You have reached the limit!, you can only vouch/devouch once a day./..",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="❌ | Source Code Error !",ephemeral=True)
                    else:
                        channel = chan
                        if channel != None:
                            try:
                                VouchCooldown[str(interaction.user.id)]
                            except:
                                VouchCooldown[str(interaction.user.id)] = 0
                            if VouchCooldown[str(interaction.user.id)] == 0:
                                Checker = False
                                if datetime.datetime.now().strftime("%Y") == interaction.user.created_at.strftime("%Y"):
                                    if (int(datetime.datetime.now().strftime("%m")) - int(interaction.user.created_at.strftime("%m")) < 5) and (int(datetime.datetime.now().strftime("%m")) - int(member.created_at.strftime("%m")) < 5):
                                        Checker = True
                                elif int(datetime.datetime.now().strftime("%Y")) == (int(interaction.user.created_at.strftime("%Y"))+1):
                                    if int(datetime.datetime.now().strftime("%m")) < 5:
                                        Checker = True
                                    elif (int(datetime.datetime.now().strftime("%m")) + (12-int(interaction.user.created_at.strftime("%m")))) < 5:
                                        Checker = True
                                else:
                                    Checker = True
                                if Checker:
                                    await interaction.response.send_message(content="✔️ | You Have Browsed Successfully!") 
                                    embed = discord.Embed(title=f"{interaction.user.mention} Devouch Request Sent To {member.mention}",description=f"**Content:** {reason}\n**Image:**")
                                    embed.set_image(url=image.url)
                                    view = discord.ui.View(timeout=None)
                                    YesButton = discord.ui.Button(label="Accept",style=discord.ButtonStyle.green,emoji="<:Accept:1027947834386956350>")
                                    NoButton = discord.ui.Button(label="Deny",style=discord.ButtonStyle.red,emoji="<:deny:1027947850258186313>")

                                    async def YesCallback(inter:discord.Interaction):
                                        async with aiosqlite.connect("Voucher/main.db") as db:
                                                async with db.cursor() as cursor:
                                                    Daydate = datetime.datetime.now().strftime("%d/%m/%Y")
                                                    Monthdate = datetime.datetime.now().strftime("%m/%Y")
                                                    j = {"vouch": 0, "unvouch": 1, "vouch_day":{f"{Daydate}":0}, "unvouch_day": {f"{Daydate}":1}, "vouch_month":{f"{Monthdate}":0}, "unvouch_month": {f"{Monthdate}":1}}
                                                    js = json.dumps(j)
                                                    v = {f"{Daydate}":{"type":["unvouch"],"voucher":[interaction.user.id],"reason":[reason],"accept":[inter.user.id],"image":[image.url]}}
                                                    vs = json.dumps(v)
                                                    await cursor.execute('INSERT INTO users (info, id) VALUES (?, ?)',(js,member.id,))
                                                    await cursor.execute('INSERT INTO vouch (info, id) VALUES (?, ?)',(vs,member.id,))
                                                    YesButton.style = discord.ButtonStyle.green
                                                    YesButton.disabled = True
                                                    NoButton.disabled = True
                                                    await Msg.edit(view=view)
                                                    await inter.response.send_message(ephemeral=True,content="✔️ | Request Sent Successfully, It Needs Approval")
                                                await db.commit()
                                    async def NoCallback(inter:discord.Interaction):
                                        NoButton.style = discord.ButtonStyle.green
                                        YesButton.disabled = True
                                        NoButton.disabled = True
                                        await Msg.edit(view=view)
                                        await inter.response.send_message(ephemeral=True,content="✔️ | Request Sent Successfully, It Needs Approval")
                                    view.add_item(YesButton)
                                    YesButton.callback = YesCallback
                                    view.add_item(NoButton)
                                    NoButton.callback = NoCallback
                                    Msg = await client.get_channel(int(channel)).send(embed=embed,view=view)  
                                    VouchCooldown[str(interaction.user.id)] = 24
                                else:
                                    await interaction.response.send_message(ephemeral=True,content="✔️ | Request Sent Successfully, It Needs Approval")
                                    dat = {}
                                    async with aiosqlite.connect("Voucher/main.db") as db:
                                        async with db.cursor() as cursor:
                                            Daydate = datetime.datetime.now().strftime("%d/%m/%Y")
                                            Monthdate = datetime.datetime.now().strftime("%m/%Y")
                                            j = {"vouch": 0, "unvouch": 1, "vouch_day":{f"{Daydate}":0}, "unvouch_day": {f"{Daydate}":1}, "vouch_month":{f"{Monthdate}":0}, "unvouch_month": {f"{Monthdate}":1}}
                                            js = json.dumps(j)
                                            v = {f"{Daydate}":{"type":["unvouch"],"voucher":[interaction.user.id],"reason":[reason],"accept":[client.user.id],"image":[image.url]}}
                                            vs = json.dumps(v)
                                            dat["day"] = Daydate
                                            dat["month"] = Monthdate
                                            dat["index"] = 0
                                            await cursor.execute('INSERT INTO users (info, id) VALUES (?, ?)',(js,member.id,))
                                            await cursor.execute('INSERT INTO vouch (info, id) VALUES (?, ?)',(vs,member.id,))
                                        await db.commit()
                                    embed = discord.Embed(title=f"{interaction.user} đã xin devouch {member}",description=f"**Lý do:** {reason}")
                                    embed.set_image(url=image.url)
                                    view = discord.ui.View(timeout=None)
                                    async def HuyCallback(inter:discord.Interaction):
                                        HuyButton.style = discord.ButtonStyle.green
                                        HuyButton.disabled = True
                                        await Msg.edit(view=view)
                                        async with aiosqlite.connect("Voucher/main.db") as db:
                                                async with db.cursor() as cursor:
                                                    await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                                                    data = await cursor.fetchone()
                                                    d = str(data)[2:-3]
                                                    info = json.loads(d.replace("\'","\""))
                                                    info["unvouch"] -= 1
                                                    info["unvouch_day"][str(dat["day"])] -= 1
                                                    info["unvouch_month"][str(dat["month"])] -= 1
                                                    await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                                                    vouch = await cursor.fetchone()
                                                    d = str(vouch)[2:-3]
                                                    vi = json.loads(d.replace("\'","\""))
                                                    for x in vi[str(dat["day"])]:
                                                        vi[str(dat["day"])][x].pop(dat["index"])
                                                    js = json.dumps(info)
                                                    vs = json.dumps(vi)
                                                    await cursor.execute('UPDATE users SET info = ? WHERE id = ?',(js,member.id,))
                                                    await cursor.execute('UPDATE vouch SET info = ? WHERE id = ?',(vs,member.id,))
                                                await db.commit()
                                        await inter.response.send_message(ephemeral=True,content="Đã hủy devouch!")
                                    HuyButton = discord.ui.Button(label="Hủy",style=discord.ButtonStyle.gray)
                                    view.add_item(HuyButton)
                                    HuyButton.callback = HuyCallback
                                    Msg = await client.get_channel(int(channel)).send(embed=embed,view=view)  
                                    VouchCooldown[str(interaction.user.id)] = 24
                            else:
                                await interaction.response.send_message(content="❌ | You have reached the limit!, you can only vouch/devouch once a day./..",ephemeral=True)
                        else:
                            await interaction.response.send_message(content="❌ | Source Code Error!",ephemeral=True)
                try:
                    if VCooldown[str(interaction.user.id)] == 0:
                        VCooldown[str(interaction.user.id)] = 1
                        while VouchCooldown[str(interaction.user.id)] > 0:
                            await asyncio.sleep(3600)
                            VouchCooldown[str(interaction.user.id)] -= 1
                        VCooldown[str(interaction.user.id)] = 0
                    else:
                        pass
                except:
                    VCooldown[str(interaction.user.id)] = 1
                    while VouchCooldown[str(interaction.user.id)] > 0:
                        await asyncio.sleep(3600)
                        VouchCooldown[str(interaction.user.id)] -= 1
                    VCooldown[str(interaction.user.id)] = 0
        
    @client.tree.command(name="info",description="User information")
    async def info(interaction: discord.Interaction, member:discord.Member):
        vouch = 0
        unvouch = 0
        if member.bot:
            await interaction.response.send_message("❌ | Bot No Information!",ephemeral=True)
        elif not interaction.user.bot:
            async with aiosqlite.connect("Voucher/main.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                    data = await cursor.fetchone()
                    if data:
                        d = str(data)[2:-3]
                        info = json.loads(d.replace("\'","\""))
                        vouch = int(info["vouch"])
                        unvouch = int(info["unvouch"])
                    else:
                        pass
            try:
                image = discord.File("Voucher/info.png",filename="info.png")
                names = ["vouch","devouch"]
                marks = np.array([vouch,unvouch])
                plt.rcParams['figure.facecolor'] = '#2f3136'
                plt.rcParams['axes.facecolor'] = '#2f3136'
                fig, ax = plt.subplots()
                my_circle = plt.Circle((0, 0), 0.7, color='#2f3136')
                plt.pie(marks, autopct="%1.1f%%",colors=['#76FF57', '#EE4848'],startangle=90,pctdistance=0.825)
                p = plt.gcf()
                p.set_size_inches(6,6)
                mpl.rcParams['text.color'] = 'white'
                ax.text(0.5, 0.5, f'{vouch}\nVouches',horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,weight="bold",font={'size':15})
                p.gca().add_artist(my_circle)
                plt.legend(names, loc="upper center",ncol=2)
                plt.savefig("Voucher/info.png")
                plt.close()
                view = discord.ui.View(timeout=None)
                
                #User rep
                UButton = discord.ui.Button(label="User",style=discord.ButtonStyle.green,emoji="<:user:1027484498851541022>")
                #Process Button
                ProButton = discord.ui.Button(label="Process",style=discord.ButtonStyle.green,emoji="<:Process:1027479997016969227>")
                #Info Button
                InfoButton = discord.ui.Button(label="Details",style=discord.ButtonStyle.gray,emoji="<:Detail:1027956098377986099>")
                
                view.add_item(ProButton)
                view.add_item(UButton)
                view.add_item(InfoButton)
                
                async def ProCallback(inter:discord.Interaction):
                    async def home(interac:discord.Interaction):
                        emb.set_image(url="attachment://info.png")
                        await interac.response.edit_message(attachments=[discord.File("Voucher/info.png",filename="info.png")],embed=emb,view = view)
                        ViewN["view"] = 1
                        if ProButton.disabled == False:
                            timer = 15
                            while timer > 0:
                                await asyncio.sleep(1)
                                timer -= 1
                            if ViewN["view"] == 1:
                                ProButton.disabled = True
                                UButton.disabled = True
                                InfoButton.disabled = True
                                await interaction.edit_original_response(view=view)
                    HomeB = discord.ui.Button(label="Home",style=discord.ButtonStyle.green)
                    Nview = discord.ui.View(timeout=None)
                    Nview.add_item(HomeB)
                    HomeB.callback = home
                    
                    async def WeekCall(intr:discord.Interaction):
                        data = {}
                        data["Day"] = []
                        data["rate"] = []
                        color = None
                        if (info["vouch"] >= info["unvouch"]):
                            date = datetime.datetime.now()
                            color = "green"
                            temp = []
                            if int(date.strftime("%d")) >= 7:
                                for x in info["vouch_day"]:
                                    if len(temp) == 7:
                                        break
                                    if x[3:len(x)] == str(date.strftime("%m/%Y")):
                                        i = 6
                                        while i >= 0:
                                            if int(x[0:2]) == int(int(date.strftime("%d")) - i):
                                                temp.append(x)
                                            i-=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[0:2]) > int(temp[j][0:2]):
                                            tmp = str(x)
                                            x = str(temp[j])
                                            temp[j] = str(tmp)
                                        j+= 1
                                    i+= 1
                            else:
                                for x in info["vouch_day"]:
                                    if len(temp) == 7:
                                        break
                                    if x[3:len(x)] == str(date.strftime("%m/%Y")):
                                        i = int(date.strftime("%d"))-1
                                        while i >= 0:
                                            if int(x[0:2]) == int(int(date.strftime("%d")) - i):
                                                temp.append(x)
                                            i-=1
                                    lmon = str(int(date.strftime("%m"))-1)
                                    if int(lmon) < 10 and int(lmon) != 0:
                                        lmon = "0" + lmon
                                        lmon += str(date.strftime("/%Y"))
                                    elif int(lmon) == 0:
                                        lmon = "12/"
                                        lmon += str(int(date.strftime("%Y"))-1)
                                    elif int(lmon) >= 10 and int(lmon) != 0:
                                        lmon += str(date.strftime("/%Y"))
                                    if x[3:len(x)] == lmon:
                                        i = 6-int(date.strftime("%d"))
                                        if int(int(date.strftime("%m"))-1) in [1,3,5,7,8,10,12]:
                                            md = 31
                                        if int(int(date.strftime("%m"))-1) in [4,6,7,11,9]:
                                            md = 30
                                        if int(int(date.strftime("%m"))-1) == 2:
                                            if int(date.strftime("%Y"))%4 == 0 and int(date.strftime("%Y"))%100 != 0 or int(date.strftime("%Y"))%400 == 0:
                                                md = 29
                                            else:
                                                md = 28
                                        while i >= 0:
                                            if int(x[0:2]) == int(md - i):
                                                temp.append(x)
                                            i-=1
                                i = 0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[3:5]) > int(temp[j][3:5]):
                                            tmp = str(x)
                                            x = str(temp[j])
                                            temp[j] = str(x)
                                        j+= 1
                                    i+=1
                                i = 0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[3:5]) == int(temp[j][3:5]):
                                            if int(x[0:2]) > int(temp[j][0:2]):
                                                tmp = str(x)
                                                x = str(temp[j])
                                                temp[j] = str(x)
                                        j+= 1
                                    i+=1
                            data["Day"] = temp.copy()
                            for x in data["Day"]:
                                s = info["vouch_day"][x] + info["unvouch_day"][x]
                                rate = (info["vouch_day"][x] / s)*100
                                data["rate"].append(rate)
                            i = 0
                            while i < len(data["Day"]):
                                data["Day"][i] = str(i+1) + ", " + data["Day"][i][0:5]
                                i+= 1
                        else:
                            date = datetime.datetime.now()
                            color = "red"
                            temp = []
                            if int(date.strftime("%d")) >= 7:
                                for x in info["unvouch_day"]:
                                    if len(temp) == 7:
                                        break
                                    if x[3:len(x)] == str(date.strftime("%m/%Y")):
                                        i = 6
                                        while i >= 0:
                                            if int(x[0:2]) == int(int(date.strftime("%d")) - i):
                                                temp.append(x)
                                            i-=1
                                i = 0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[0:2]) > int(temp[j][0:2]):
                                            tmp = str(x)
                                            x = str(temp[j])
                                            temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                            else:
                                for x in info["unvouch_day"]:
                                    if len(temp) == 7:
                                        break
                                    if x[3:len(x)] == str(date.strftime("%m/%Y")):
                                        i = int(date.strftime("%d"))-1
                                        while i >= 0:
                                            if int(x[0:2]) == int(int(date.strftime("%d")) - i):
                                                temp.append(x)
                                            i-=1
                                    lmon = str(int(date.strftime("%m"))-1)
                                    if int(lmon) < 10 and int(lmon) != 0:
                                        lmon = "0" + lmon
                                        lmon += str(date.strftime("/%Y"))
                                    elif int(lmon) == 0:
                                        lmon = "12/"
                                        lmon += str(int(date.strftime("%Y"))-1)
                                    elif int(lmon) >= 10 and int(lmon) != 0:
                                        lmon += str(date.strftime("/%Y"))
                                    if x[3:len(x)] == lmon:
                                        i = 6-int(date.strftime("%d"))
                                        if int(int(date.strftime("%m"))-1) in [1,3,5,7,8,10,12]:
                                            md = 31
                                        if int(int(date.strftime("%m"))-1) in [4,6,7,11,9]:
                                            md = 30
                                        if int(int(date.strftime("%m"))-1) == 2:
                                            if int(date.strftime("%Y"))%4 == 0 and int(date.strftime("%Y"))%100 != 0 or int(date.strftime("%Y"))%400 == 0:
                                                md = 29
                                            else:
                                                md = 28
                                        while i >= 0:
                                            if int(x[0:2]) == int(md - i):
                                                temp.append(x)
                                            i-=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[3:5]) > int(temp[j][3:5]):
                                            tmp = str(x)
                                            x = str(temp[j])
                                            temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[3:5]) == int(temp[j][3:5]):
                                            if int(x[0:2]) > int(temp[j][0:2]):
                                                tmp = str(x)
                                                x = str(temp[j])
                                                temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                            data["Day"] = temp.copy()
                            for x in data["Day"]:
                                s = (info["vouch_day"][x] + info["unvouch_day"][x])
                                rate = (info["unvouch_day"][x] / s)*100
                                data["rate"].append(rate)
                            i = 0
                            while i < len(data["Day"]):
                                data["Day"][i] = str(i+1) + ", " + data["Day"][i][0:5]
                                i+= 1
                        df2 = DataFrame(data,columns=["Day","rate"])
                        fig = plt.Figure(figsize=(5,4), dpi=100)
                        ax2 = fig.add_subplot(111)
                        df2 = df2[["Day","rate"]].groupby('Day').sum()
                        if color == "green":
                            ax2.set_title("Vouch Process")
                            df2.plot(kind='line', legend=False, ax=ax2, color='g',marker='o', fontsize=10)
                        elif color == "red":
                            ax2.set_title("Devouch Process")
                            df2.plot(kind='line', legend=False, ax=ax2, color='r',marker='o', fontsize=10)
                        fig.savefig("process.png")
                        
                        Week.style = discord.ButtonStyle.green
                        Week.disabled = True
                        Year.disabled = True
                        emb.set_image(url="attachment://process.png")
                        await intr.response.edit_message(attachments=[discord.File("process.png",filename="process.png")],view=Nview,embed=emb)
                    
                    async def YearCall(intr:discord.Interaction):
                        data = {}
                        data["Month"] = []
                        data["rate"] = []
                        color = None
                        if (info["vouch"] >= info["unvouch"]):
                            date = datetime.datetime.now()
                            color = "green"
                            temp = []
                            if int(date.strftime("%m")) == 12:
                                for x in info["vouch_month"]:
                                    if len(temp) == 12:
                                        break
                                    if x[3:len(x)] == str(date.strftime("%Y")):
                                        i = 12
                                        while i >= 0:
                                            if int(x[0:2]) == int(int(date.strftime("%m")) - i):
                                                temp.append(x)
                                            i-=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[0:2]) > int(temp[j][0:2]):
                                            tmp = str(x)
                                            x = str(temp[j])
                                            temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                            else:
                                for x in info["vouch_month"]:
                                    if len(temp) == 12:
                                        break
                                    if x[3:len(x)] == str(date.strftime("%Y")):
                                        i = int(date.strftime("%m"))-1
                                        while i >= 0:
                                            if int(x[0:2]) == int(int(date.strftime("%m")) - i):
                                                temp.append(x)
                                            i-=1
                                    if x[3:len(x)] == str(int(date.strftime("%Y")) - 1):
                                        i = 12-int(date.strftime("%m"))
                                        while i >= 0:
                                            if int(x[0:2]) == int(12 - i):
                                                temp.append(x)
                                            i-=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[3:len(x)]) > int(temp[j][3:len(x)]):
                                            tmp = str(x)
                                            x = str(temp[j])
                                            temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[3:len(x)]) == int(temp[j][3:len(x)]):
                                            if int(x[0:2]) > int(temp[j][0:2]):
                                                tmp = str(x)
                                                x = str(temp[j])
                                                temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                            data["Month"] = temp.copy()
                            for x in data["Month"]:
                                s = (info["vouch_month"][x] + info["unvouch_month"][x])
                                rate = (info["vouch_month"][x] / s)*100
                                data["rate"].append(rate)
                            i = 0
                            while i < len(data["Month"]):
                                data["Month"][i] = str(i+1) + ", " + data["Month"][i]
                                i+= 1  
                        else:
                            date = datetime.datetime.now()
                            color = "red"
                            temp = []
                            if int(date.strftime("%m")) == 12:
                                for x in info["unvouch_month"]:
                                    if len(temp) == 12:
                                        break
                                    if x[3:len(x)] == str(date.strftime("%Y")):
                                        i = 12
                                        while i >= 0:
                                            if int(x[0:2]) == int(int(date.strftime("%m")) - i):
                                                temp.append(x)
                                            i-=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[0:2]) > int(temp[j][0:2]):
                                            tmp = str(x)
                                            x = str(temp[j])
                                            temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                            else:
                                for x in info["unvouch_month"]:
                                    if len(temp) == 12:
                                        break
                                    if x[3:len(x)] == str(date.strftime("%Y")):
                                        i = int(date.strftime("%m"))-1
                                        while i >= 0:
                                            if int(x[0:2]) == int(int(date.strftime("%m")) - i):
                                                temp.append(x)
                                            i-=1
                                    if x[3:len(x)] == str(int(date.strftime("%Y")) - 1):
                                        i = 12-int(date.strftime("%m"))
                                        while i >= 0:
                                            if int(x[0:2]) == int(12 - i):
                                                temp.append(x)
                                            i-=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[3:len(x)]) > int(temp[j][3:len(x)]):
                                            tmp = str(x)
                                            x = str(temp[j])
                                            temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                                i=0
                                for x in temp:
                                    j = i + 1
                                    while j < len(temp):
                                        if int(x[3:len(x)]) == int(temp[j][3:len(x)]):
                                            if int(x[0:2]) > int(temp[j][0:2]):
                                                tmp = str(x)
                                                x = str(temp[j])
                                                temp[j] = str(tmp)
                                        j+= 1
                                    i+=1
                            data["Month"] = temp.copy()
                            for x in data["Month"]:
                                s = (info["vouch_month"][x] + info["unvouch_month"][x])
                                rate = (info["unvouch_month"][x] / s)*100
                                data["rate"].append(rate)
                            i = 0
                            while i < len(data["Month"]):
                                data["Month"][i] = str(i+1) + ", " + data["Month"][i]
                                i+= 1  
                        df2 = DataFrame(data,columns=["Month","rate"])
                        fig = plt.Figure(figsize=(5,4), dpi=100)
                        ax2 = fig.add_subplot(111)
                        df2 = df2[["Month","rate"]].groupby('Month').sum()
                        if color == "green":
                            ax2.set_title("Vouch Process")
                            df2.plot(kind='line', legend=False, ax=ax2, color='g',marker='o', fontsize=10)
                        elif color == "red":
                            ax2.set_title("Devouch Process")
                            df2.plot(kind='line', legend=False, ax=ax2, color='r',marker='o', fontsize=10)
                        fig.savefig("process.png")
                        
                        Year.style = discord.ButtonStyle.green
                        Week.disabled = True
                        Year.disabled = True
                        emb.set_image(url="attachment://process.png")
                        await intr.response.edit_message(attachments=[discord.File("process.png",filename="process.png")],view=Nview,embed=emb)
                    e = discord.Embed(title="Choose You Process:",description="❶ **Week:** Show your vouch/devouch process for the last 7 days.\n\n ❷ **Years:** Show your vouch/devouch process for the past 1 year.")
                    v = discord.ui.View(timeout=None)
                    Week = discord.ui.Button(label="Week",style=discord.ButtonStyle.gray)
                    Year = discord.ui.Button(label="Years",style=discord.ButtonStyle.gray)
                    Week.callback = WeekCall
                    Year.callback = YearCall
                    v.add_item(Week)
                    v.add_item(Year)
                    await inter.response.edit_message(embed=e,view=v,attachments=[])
                    ViewN["view"] = 0
                
                async def UCallback(inter:discord.Interaction):
                    image = Image.new(mode="RGB",size=(600,200)).convert('RGB')
                    await inter.guild.icon.save("Voucher/user.png")
                    GImage = Image.open("Voucher/user.png")
                    GImage = GImage.crop((0,0,576,192))
                    GImage = ImageOps.contain(GImage, (600,200))
                    GImage = ImageEnhance.Contrast(GImage).enhance(.5)
                    image.paste(GImage,(0,0))
                    font = ImageFont.truetype("arial.ttf",40)
                    draw = ImageDraw.Draw(image)
                    draw.text((180,36), f"{member}",(255,255,255),font=font,stroke_width=1,stroke_fill="black")
                    draw = ImageDraw.Draw(image)
                    color=(0, 255, 0)
                    percent = (info["vouch"] / (info["vouch"] + info["unvouch"]))
                    x = (percent*380)+176
                    y, diam =  100, 21
                    bar = Image.open("Voucher/bar.png").convert("RGBA")
                    bar.thumbnail((380,50))
                    image.paste(bar,(180,100))
                    draw.ellipse([176,100,176+diam,100+diam], fill=(72,75,78))
                    draw.ellipse([550,100,550+diam,100+diam], fill=(72,75,78))
                    draw.ellipse([x,y,x+diam,y+diam], fill=color)
                    ImageDraw.floodfill(image, xy=(176,110), value=color, thresh=40)
                    backfont = ImageFont.truetype("arial.ttf",26)
                    draw.text((180,130),f"Reputation: {int(percent*100)}/100%",font=backfont,stroke_width=1,stroke_fill="black")
                    image.save("Voucher/user.png")
                    background = Editor("Voucher/user.png")
                    img = await load_image_async(str(member.display_avatar.url))
                    img = Editor(img).resize((128,128)).circle_image()
                    background.paste(img,(36,36))
                    background.ellipse((36,36),128,128,outline="white",stroke_width=2)
                    file = discord.File(fp=background.image_bytes,filename="user.png")
                    emb.set_image(url="attachment://user.png")
                    async def home(interac:discord.Interaction):
                        emb.set_image(url="attachment://info.png")
                        await interac.response.edit_message(attachments=[discord.File("Voucher/info.png",filename="info.png")],embed=emb,view = view)
                        ViewN["view"] = 1
                        if ProButton.disabled == False:
                            timer = 15
                            while timer > 0:
                                await asyncio.sleep(1)
                                timer -= 1
                            if ViewN["view"] == 1:
                                ProButton.disabled = True
                                UButton.disabled = True
                                InfoButton.disabled = True
                                await interaction.edit_original_response(view=view)
                            
                    HomeB = discord.ui.Button(label="Home",style=discord.ButtonStyle.green)
                    Nview = discord.ui.View(timeout=None)
                    Nview.add_item(HomeB)
                    HomeB.callback = home
                    await inter.response.edit_message(attachments=[file],embed=emb,view=Nview)
                    ViewN["view"] = 0
                
                async def InfoCallback(inter:discord.Interaction):
                    ViewN["view"] = 0
                    async with aiosqlite.connect("Voucher/main.db") as db:
                        async with db.cursor() as cursor:
                            await cursor.execute('SELECT info FROM vouch WHERE id = ?', (member.id,))
                            vouch = await cursor.fetchone()
                            if vouch:
                                await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                                d = await cursor.fetchone()
                                data = json.loads(str(d)[2:-3].replace("\'","\""))
                                vinfo = json.loads(str(vouch)[2:-3].replace("\'","\""))
                                if len(vinfo) > 10:
                                    mpage = math.ceil(len(mpage)/10)
                                else:
                                    mpage = 1
                                page = 1
                                Pemb = discord.Embed(color=0x0049FF,title="Choose A Day To Show Details:")
                                Pemb.set_footer(text=f"Page: {page}/{mpage}")
                                count = 1
                                Sel = discord.ui.Select(placeholder="Choose one",row=1)
                                for x in vinfo:
                                    if count > page*10:
                                        break
                                    voucht = data["vouch_day"][x]
                                    unvoucht = data["unvouch_day"][x]
                                    Pemb.add_field(name=f"{list(vinfo).index(x)+1}, {x}",value=f"Vouches: {voucht} | Devouches: {unvoucht}",inline=False)
                                    Sel.add_option(label=f"{x}",value=x)
                                    count+=1
                                async def precallback(ins):
                                    nonlocal page
                                    if mpage < page:
                                        page -= 1
                                    Pemb.clear_fields()
                                    Sel.options = []
                                    count=1
                                    for x in vinfo:
                                        if count < ((page-1)*10+1):
                                            count+=1
                                            continue
                                        if count > page*10:
                                            break
                                        voucht = data["vouch_day"][x]
                                        unvoucht = data["unvouch_day"][x]
                                        Pemb.add_field(name=f"{list(vinfo).index(x)+1}, {x}",value=f"Vouches: {voucht} | Devouches: {unvoucht}",inline=False)
                                        Sel.add_option(label=f"{x}",value=x)
                                        count+=1
                                    Pemb.set_footer(text=f"Page: {page}/{mpage}")
                                    await ins.response.edit_message(embed=Pemb)
                                async def nextcallback(ins):
                                    nonlocal page
                                    if mpage > page:
                                        page += 1
                                    Pemb.clear_fields()
                                    Sel.options = []
                                    count=1
                                    for x in vinfo:
                                        if count < ((page-1)*10+1):
                                            count+=1
                                            continue
                                        if count > page*10:
                                            break
                                        voucht = data["vouch_day"][x]
                                        unvoucht = data["unvouch_day"][x]
                                        Pemb.add_field(name=f"{list(vinfo).index(x)+1}, {x}",value=f"Vouches: {voucht} | Devouches: {unvoucht}",inline=False)
                                        Sel.add_option(label=f"{x}",value=x)
                                        count+=1
                                    Pemb.set_footer(text=f"Page: {page}/{mpage}")
                                    await ins.response.edit_message(embed=Pemb)
                                async def home(interac:discord.Interaction):
                                    emb.set_image(url="attachment://info.png")
                                    await interac.response.edit_message(attachments=[discord.File("Voucher/info.png",filename="info.png")],embed=emb,view = view)
                                    ViewN["view"] = 1
                                    if ProButton.disabled == False:
                                        timer = 15
                                        while timer > 0:
                                            await asyncio.sleep(1)
                                            timer -= 1
                                        if ViewN["view"] == 1:
                                            ProButton.disabled = True
                                            UButton.disabled = True
                                            InfoButton.disabled = True
                                            await interaction.edit_original_response(view=view)
                                async def selCall(interac:discord.Interaction):
                                    vi = discord.ui.View(timeout=None)
                                    if len(vinfo[Sel.values[0]]) > 10:
                                        mpage = math.ceil(len(mpage)/10)
                                    else:
                                        mpage = 1
                                    page = 1
                                    PNemb = discord.Embed(color=0x0049FF,title="Choose One To Show:")
                                    PNemb.set_footer(text=f"Page: {page}/{mpage}")
                                    count = 1
                                    SelI = discord.ui.Select(placeholder="Choose one",row=1)
                                    max = len(vinfo[Sel.values[0]]["type"])
                                    i = 0
                                    while i < max:
                                        if count > page*10:
                                            break
                                        tlist = vinfo[Sel.values[0]]["type"][i]
                                        voucher = client.get_channel(chan).guild.get_member(int(vinfo[Sel.values[0]]["voucher"][i])).mention
                                        PNemb.add_field(name=f"{i+1}, {tlist}",value=f"Voucher: {voucher}",inline=False)
                                        SelI.add_option(label=f"{i+1}, {tlist}",value=i)
                                        count+=1
                                        i+=1
                                    async def preIcallback(ins):
                                        nonlocal page
                                        if mpage < page:
                                            page -= 1
                                        PNemb.clear_fields()
                                        SelI.options = []
                                        count=1
                                        i=0
                                        max = len(vinfo[Sel.values[0]]["type"])
                                        while i < max:
                                            if count < ((page-1)*10+1):
                                                count+=1
                                                i+=1
                                                continue
                                            if count > page*10:
                                                break
                                            tlist = vinfo[Sel.values[0]]["type"][i]
                                            voucher = client.get_channel(chan).guild.get_member(vinfo[str(Sel.values[0])]["voucher"][i]).mention
                                            PNemb.add_field(name=f"{i+1}, {tlist}",value=f"Voucher: {voucher}",inline=False)
                                            SelI.add_option(label=f"{i+1}, {tlist}",value=i)
                                            count+=1
                                            i+=1
                                        PNemb.set_footer(text=f"Page: {page}/{mpage}")
                                        await ins.response.edit_message(embed=PNemb)
                                    async def nextIcallback(ins):
                                        nonlocal page
                                        if mpage > page:
                                            page += 1
                                        PNemb.clear_fields()
                                        SelI.options = []
                                        count=1
                                        i=0
                                        max = len(vinfo[Sel.values[0]]["type"])
                                        while i < max:
                                            if count < ((page-1)*10+1):
                                                count+=1
                                                i+=1
                                                continue
                                            if count > page*10:
                                                break
                                            tlist = vinfo[Sel.values[0]]["type"][i]
                                            voucher = client.get_channel(chan).guild.get_member(vinfo[str(Sel.values[0])]["voucher"][i]).mention
                                            PNemb.add_field(name=f"{i+1}, {tlist}",value=f"Voucher: {voucher}",inline=False)
                                            SelI.add_option(label=f"{i+1}, {tlist}",value=i)
                                            count+=1
                                            i+=1
                                        PNemb.set_footer(text=f"Page: {page}/{mpage}")
                                        await ins.response.edit_message(embed=PNemb)
                                    async def back(ins):
                                        await ins.response.edit_message(embed=Pemb,view=v)
                                    async def selICall(ins):
                                        index = int(SelI.values[0])
                                        idata = vinfo[Sel.values[0]]
                                        date = Sel.values[0]
                                        voucher = client.get_channel(chan).guild.get_member(idata["voucher"][index]).mention
                                        vtype = idata["type"][index]
                                        reason = idata["reason"][index]
                                        accept = client.get_channel(chan).guild.get_member(idata["accept"][index]).mention
                                        userD = member.created_at.strftime("%d/%m/%Y")
                                        VoucherD = client.get_channel(chan).guild.get_member(idata["voucher"][index]).created_at.strftime("%d/%m/%Y")
                                        Show = discord.Embed(color=0x00000,title="Vouch/Devouch's Details:",description=f"**User:** {member.mention}\n**Account Create Date:** {userD}\n\n**Voucher:** {voucher}\n**Account Create Date:** {VoucherD}\n\n**Vouch Type:** {vtype}\n\n**Reason:** {reason}\n\n**Accepted by:** {accept}")
                                        Show.set_image(url=idata["image"][index])
                                        Show.set_footer(text=f"At: {date}")
                                        Sv = discord.ui.View(timeout=None)
                                        Sv.add_item(Back)
                                        await ins.response.edit_message(embed=Show,view=Sv)
                                    backIB=discord.ui.Button(label="<",style=discord.ButtonStyle.blurple,row=2)
                                    nextIB=discord.ui.Button(label=">",style=discord.ButtonStyle.blurple,row=2)
                                    Back=discord.ui.Button(label="Back",style=discord.ButtonStyle.gray,row=2)
                                    backIB.callback = preIcallback
                                    nextIB.callback = nextIcallback
                                    SelI.callback = selICall
                                    Back.callback = back
                                    vi.add_item(backIB)
                                    vi.add_item(Back)
                                    vi.add_item(nextIB)
                                    vi.add_item(SelI)
                                    await interac.response.edit_message(embed=PNemb,view=vi)
                                v=discord.ui.View(timeout=None)
                                backB=discord.ui.Button(label="<",style=discord.ButtonStyle.blurple,row=2)
                                nextB=discord.ui.Button(label=">",style=discord.ButtonStyle.blurple,row=2)
                                Home=discord.ui.Button(label="Home",style=discord.ButtonStyle.green,row=2)
                                backB.callback = precallback
                                nextB.callback = nextcallback
                                Home.callback = home
                                Sel.callback = selCall
                                v.add_item(backB)
                                v.add_item(Home)
                                v.add_item(nextB)
                                v.add_item(Sel)
                                await inter.response.edit_message(embed=Pemb,view=v,attachments=[])
                
                UButton.callback = UCallback
                ProButton.callback = ProCallback
                InfoButton.callback = InfoCallback
                
                #thay embed của ông vào phần này
                emb = discord.Embed(color=0x00FFF3,description=f"╭・⌬・Reputation Information\n●▬▬▬▬▬▬▬▬๑۩✰۩๑▬▬▬▬▬▬▬▬●\n> :grinning: **User:** {member.mention}\n> 🟢 **Vouches:** {vouch}\n> 🔴 **Devouches: ** {unvouch}\n●▬▬▬▬▬▬▬▬๑۩✰۩๑▬▬▬▬▬▬▬▬●\n╰・⌬・Reputation Information")
                emb.timestamp = datetime.datetime.now()
                emb.set_footer(icon_url=interaction.guild.icon.url,text=f"{interaction.guild.name} • Requested by {interaction.user}")
                #hết 3 dòng này là hết, phần dưới là phần ảnh được render trong embed
                
                emb.set_image(url="attachment://info.png")
                await interaction.response.send_message(file=image,embed=emb,view=view,ephemeral=True)
                ViewN = {}
                ViewN["view"] = 1
                timer = 15
                while timer > 0:
                    await asyncio.sleep(1)
                    timer -= 1
                if ViewN["view"] == 1:
                    ProButton.disabled = True
                    UButton.disabled = True
                    InfoButton.disabled = True
                    await interaction.edit_original_response(view=view)
            except:
                image = discord.File("Voucher/info.png",filename="info.png")
                names = ["vouch","devouch"]
                marks = np.array([1,0])
                plt.rcParams['figure.facecolor'] = '#2f3136'
                plt.rcParams['axes.facecolor'] = '#2f3136'
                fig, ax = plt.subplots()
                my_circle = plt.Circle((0, 0), 0.7, color='#2f3136')
                plt.pie(marks, autopct="%1.1f%%",colors=['#76FF57', '#EE4848'],startangle=90,pctdistance=0.825)
                p = plt.gcf()
                p.set_size_inches(6,6)
                mpl.rcParams['text.color'] = 'white'
                ax.text(0.5, 0.5, f'0\nVouches',horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,weight="bold",font={'size':15})
                p.gca().add_artist(my_circle)
                plt.legend(names, loc="upper center",ncol=2)
                plt.savefig("Voucher/info.png")
                plt.close()
                view = discord.ui.View(timeout=None)
                
                #User rep
                UButton = discord.ui.Button(label="User",style=discord.ButtonStyle.green,emoji="<:user:1027484498851541022>")
                #Process Button
                ProButton = discord.ui.Button(label="Process",style=discord.ButtonStyle.green,emoji="<:Process:1027479997016969227>")
                #Info Button
                InfoButton = discord.ui.Button(label="Details",style=discord.ButtonStyle.gray,emoji="<:Detail:1027956098377986099>")
                
                view.add_item(ProButton)
                view.add_item(UButton)
                view.add_item(InfoButton)
                
                async def ProCallback(inter:discord.Interaction):
                    
                    async def home(interac:discord.Interaction):
                        emb.set_image(url="attachment://info.png")
                        await interac.response.edit_message(attachments=[discord.File("Voucher/info.png",filename="info.png")],embed=emb,view = view)
                        ViewN["view"] = 1
                        if ProButton.disabled == False:
                            timer = 15
                            while timer > 0:
                                await asyncio.sleep(1)
                                timer -= 1
                            if ViewN["view"] == 1:
                                ProButton.disabled = True
                                UButton.disabled = True
                                InfoButton.disabled = True
                                await interaction.edit_original_response(view=view)
                    HomeB = discord.ui.Button(label="Home",style=discord.ButtonStyle.green)
                    Nview = discord.ui.View(timeout=None)
                    Nview.add_item(HomeB)
                    HomeB.callback = home
                    
                    async def WeekCall(intr:discord.Interaction):
                        data = {}
                        data["Day"] = []
                        data["rate"] = []
                        df2 = DataFrame(data,columns=["Day","rate"])
                        fig = plt.Figure(figsize=(5,4), dpi=100)
                        ax2 = fig.add_subplot(111)
                        df2 = df2[["Day","rate"]].groupby('Day').sum()
                        ax2.set_title("Vouch Process")
                        df2.plot(kind='line', legend=False, ax=ax2, color='g',marker='o', fontsize=10)
                        fig.savefig("process.png")
                        
                        Week.style = discord.ButtonStyle.green
                        Week.disabled = True
                        Year.disabled = True
                        emb.set_image(url="attachment://process.png")
                        await intr.response.edit_message(attachments=[discord.File("process.png",filename="process.png")],view=Nview,embed=emb)
                    
                    async def YearCall(intr:discord.Interaction):
                        data = {}
                        data["Month"] = []
                        data["rate"] = []
                        df2 = DataFrame(data,columns=["Month","rate"])
                        fig = plt.Figure(figsize=(5,4), dpi=100)
                        ax2 = fig.add_subplot(111)
                        df2 = df2[["Month","rate"]].groupby('Month').sum()
                        ax2.set_title("Vouch Process")
                        df2.plot(kind='line', legend=False, ax=ax2, color='g',marker='o', fontsize=10)
                        fig.savefig("process.png")
                        
                        Year.style = discord.ButtonStyle.green
                        Week.disabled = True
                        Year.disabled = True
                        emb.set_image(url="attachment://process.png")
                        await intr.response.edit_message(attachments=[discord.File("process.png",filename="process.png")],view=Nview,embed=emb)
                    e = discord.Embed(title="Choose You Process:",description="❶ **Week:** Show your vouch/devouch process for the last 7 days.\n\n ❷ **Years:** Show your vouch/devouch process for the past 1 year.")
                    v = discord.ui.View(timeout=None)
                    Week = discord.ui.Button(label="Week",style=discord.ButtonStyle.gray)
                    Year = discord.ui.Button(label="Years",style=discord.ButtonStyle.gray)
                    Week.callback = WeekCall
                    Year.callback = YearCall
                    v.add_item(Week)
                    v.add_item(Year)
                    await inter.response.edit_message(embed=e,view=v,attachments=[])
                    ViewN["view"] = 0
                
                
                async def UCallback(inter:discord.Interaction):
                    image = Image.new(mode="RGB",size=(600,200)).convert('RGB')
                    await inter.guild.icon.save("Voucher/user.png")
                    GImage = Image.open("Voucher/user.png")
                    GImage = GImage.crop((0,0,576,192))
                    GImage = ImageOps.contain(GImage, (600,200))
                    GImage = ImageEnhance.Contrast(GImage).enhance(.5)
                    image.paste(GImage,(0,0))
                    font = ImageFont.truetype("arial.ttf",40)
                    draw = ImageDraw.Draw(image)
                    draw.text((180,36), f"{member}",(255,255,255),font=font,stroke_width=1,stroke_fill="black")
                    draw = ImageDraw.Draw(image)
                    color=(0, 255, 0)
                    percent = 0
                    x = (percent*380)+176
                    y, diam =  100, 21
                    bar = Image.open("Voucher/bar.png").convert("RGBA")
                    bar.thumbnail((380,50))
                    image.paste(bar,(180,100))
                    draw.ellipse([176,100,176+diam,100+diam], fill=(72,75,78))
                    draw.ellipse([550,100,550+diam,100+diam], fill=(72,75,78))
                    draw.ellipse([x,y,x+diam,y+diam], fill=color)
                    ImageDraw.floodfill(image, xy=(176,110), value=color, thresh=40)
                    backfont = ImageFont.truetype("arial.ttf",26)
                    draw.text((180,130),f"Reputation: {int(percent*100)}/100%",font=backfont,stroke_width=1,stroke_fill="black")
                    image.save("Voucher/user.png")
                    background = Editor("Voucher/user.png")
                    img = await load_image_async(str(member.display_avatar.url))
                    img = Editor(img).resize((128,128)).circle_image()
                    background.paste(img,(36,36))
                    background.ellipse((36,36),128,128,outline="white",stroke_width=2)
                    file = discord.File(fp=background.image_bytes,filename="user.png")
                    emb.set_image(url="attachment://user.png")
                    async def home(interac:discord.Interaction):
                        emb.set_image(url="attachment://info.png")
                        await interac.response.edit_message(attachments=[discord.File("Voucher/info.png",filename="info.png")],embed=emb,view = view)
                        ViewN["view"] = 1
                        if ProButton.disabled == False:
                            timer = 15
                            while timer > 0:
                                await asyncio.sleep(1)
                                timer -= 1
                            if ViewN["view"] == 1:
                                ProButton.disabled = True
                                UButton.disabled = True
                                InfoButton.disabled = True
                                await interaction.edit_original_response(view=view)
                            
                    HomeB = discord.ui.Button(label="Home",style=discord.ButtonStyle.green)
                    Nview = discord.ui.View(timeout=None)
                    Nview.add_item(HomeB)
                    HomeB.callback = home
                    await inter.response.edit_message(attachments=[file],embed=emb,view=Nview)
                    ViewN["view"] = 0
                
                async def InfoCallback(inter:discord.Interaction):
                    ViewN["view"] = 0
                    Pemb = discord.Embed(color=0x0049FF,title="Choose A Day To Show Details:")
                    Pemb.set_footer(text=f"Page: 1/1")
                    v=discord.ui.View(timeout=None)
                    Sel = discord.ui.Select(placeholder="Choose one")
                    backB=discord.ui.Button(label="<",style=discord.ButtonStyle.blurple,row=2)
                    nextB=discord.ui.Button(label=">",style=discord.ButtonStyle.blurple,row=2)
                    Home=discord.ui.Button(label="Home",style=discord.ButtonStyle.green,row=2)
                    async def precallback(ins):
                        await ins.response.defer()
                    async def nextcallback(ins):
                        await ins.response.defer()
                    async def selCall(interac:discord.Interaction):
                        await interac.response.defer()
                    async def home(interac:discord.Interaction):
                        emb.set_image(url="attachment://info.png")
                        await interac.response.edit_message(attachments=[discord.File("Voucher/info.png",filename="info.png")],embed=emb,view = view)
                        ViewN["view"] = 1
                        if ProButton.disabled == False:
                            timer = 15
                            while timer > 0:
                                await asyncio.sleep(1)
                                timer -= 1
                            if ViewN["view"] == 1:
                                ProButton.disabled = True
                                UButton.disabled = True
                                InfoButton.disabled = True
                                await interaction.edit_original_response(view=view)
                    backB.callback = precallback
                    nextB.callback = nextcallback
                    Home.callback = home
                    Sel.callback = selCall
                    Sel.add_option(label="No Data",value="No Data")
                    v.add_item(backB)
                    v.add_item(Home)
                    v.add_item(nextB)
                    v.add_item(Sel)
                    await inter.response.edit_message(embed=Pemb,view=v,attachments=[])
                
                UButton.callback = UCallback
                ProButton.callback = ProCallback
                InfoButton.callback = InfoCallback
                
                #thay embed của ông vào phần này
                emb = discord.Embed(color=0x00FFF3,description=f"╭・⌬・Reputation Information\n●▬▬▬▬▬▬▬▬๑۩✰۩๑▬▬▬▬▬▬▬▬●\n> :grinning: **User:** {member.mention}\n> 🟢 **Vouches:** {vouch}\n> 🔴 **Devouches: ** {unvouch}\n●▬▬▬▬▬▬▬▬๑۩✰۩๑▬▬▬▬▬▬▬▬●\n╰・⌬・Reputation Information")
                emb.timestamp = datetime.datetime.now()
                emb.set_footer(icon_url=interaction.guild.icon.url,text=f"{interaction.guild.name} • Requested by {interaction.user}")
                #hết 3 dòng này là hết, phần dưới là phần ảnh được render trong embed
                
                emb.set_image(url="attachment://info.png")
                await interaction.response.send_message(file=image,embed=emb,view=view,ephemeral=True)
                ViewN = {}
                ViewN["view"] = 1
                timer = 15
                while timer > 0:
                    await asyncio.sleep(1)
                    timer -= 1
                if ViewN["view"] == 1:
                    ProButton.disabled = True
                    UButton.disabled = True
                    InfoButton.disabled = True
                    await interaction.edit_original_response(view=view)
            

    client.tree.clear_commands(guild=None)
    reset_dtb(client)
    client.tree.add_command(vouch)
    client.tree.add_command(devouch)
    client.tree.add_command(info)