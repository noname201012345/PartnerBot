import discord
from discord.ext import commands
import json
import asyncio
from datetime import datetime
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
    
    

rtoken = os.getenv("rtoken")
header = {"Authorization": "Bearer {}".format(rtoken)}
link="https://api.github.com/repos/noname201012345/PartnerBot/contents/"
    
def Sell(client:commands.Bot):
    @client.command(aliases=["as"])
    async def AddSell(ctx, mem: discord.Member, id):
        if ctx.author.guild_permissions.administrator:
            Mess = await client.get_channel(ctx.channel.id).fetch_message(id)
            with open("SellDat.json","r") as f:
                data = json.load(f)
            data["array"].append({"Seller":mem.id,"Content":f"{Mess.content}","Level":1})
            with open("SellDat.json","w") as f:
                json.dump(data,f)
            r = requests.get(link+"SellDat.json",headers=header)
            sh=r.json()["sha"]
            base64S= base64.b64encode(bytes(json.dumps(data), "utf-8"))
            rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
            response = requests.put(link+"SellDat.json", data=json.dumps(rjson), headers=header)
            await ctx.send("Thêm Seller thành công!")
        else:
            await ctx.send("Bạn phải có quyền quản lý để dùng lệnh!")
    
    
    @client.command(aliases=["sl"])
    async def SellEdit(ctx, mem: discord.Member, lvl, id):
        if ctx.author.guild_permissions.administrator:
            Mess = await client.get_channel(ctx.channel.id).fetch_message(id)
            with open("SellDat.json","r") as f:
                data = json.load(f)
            for x in data["array"]:
                if x["Seller"] == mem.id:
                    x["Level"] = int(lvl)
                    x["Content"] = Mess.content
            with open("SellDat.json","w") as f:
                json.dump(data,f)
            r = requests.get(link+"SellDat.json",headers=header)
            sh=r.json()["sha"]
            base64S= base64.b64encode(bytes(json.dumps(data), "utf-8"))
            rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
            response = requests.put(link+"SellDat.json", data=json.dumps(rjson), headers=header)
            await ctx.send("Edit Seller thành công!")
        else:
            await ctx.send("Bạn phải có quyền quản lý để dùng lệnh!")
            
    
    Selling = True
    @client.command(aliases=["ss"])            
    async def SellStart(ctx):
        if ctx.author.guild_permissions.administrator:
            nonlocal Selling
            Selling = True
            while Selling:
                with open("SellDat.json","r") as f:
                    data = json.load(f)
                view = discord.ui.View(timeout=None)
                CT = discord.ui.Button(label="Create Ticket",emoji="📩",style=discord.ButtonStyle.gray)
                async def callback(interaction: discord.Interaction):
                    cater = client.get_channel(1011207865421287488)
                    no = 0
                    for x in cater.text_channels:
                        if x.name.startswith("seller"):
                            if int(x.name[x.name.find("no")+2:len(x.name)]) >= no:
                                no = int(x.name[x.name.find("no")+2:len(x.name)]) + 1
                    over = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                    over[interaction.user] = discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
                    over[mem] = discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
                    chan = await cater.create_text_channel(name=f"seller no{no}",overwrites=over)  
                    embed = discord.Embed(description="Close This Ticket by reach 🔒",color=mem.color)
                    v = discord.ui.View(timeout=None)
                    close = discord.ui.Button(style=discord.ButtonStyle.gray,emoji="🔒",label="Close")
                    async def closeC(inter: discord.Interaction):
                        await inter.response.send_message("Ticket will closed in a few sec!")
                        await asyncio.sleep(5)
                        await inter.channel.delete()
                    close.callback = closeC
                    v.add_item(close)
                    await chan.send(f"<@{interaction.user.id}> Please wait, <@{mem.id}> is coming",embed=embed,view=v)
                    await interaction.response.send_message(f"Ticket Created <#{chan.id}>",ephemeral=True)
                CT.callback = callback          
                view.add_item(CT)
                mem = client.get_guild(ctx.guild.id).get_member(data["array"][data["index"]]["Seller"])
                emb = discord.Embed(color=mem.color,description=data["array"][data["index"]]["Content"],timestamp=datetime.now())
                emb.set_author(name=mem.display_name,icon_url=mem.display_avatar.url,url="http://discord.gg/gamerhedan")
                await client.get_channel(1041689519835054140).send(view=view,embed=emb)
                await asyncio.sleep(600*data["array"][data["index"]]["Level"])
                if data["index"] != len(data["array"])-1:
                    data["index"] += 1
                else:
                    data["index"] = 0
                with open("SellDat.json","w") as f:
                    json.dump(data,f)
                r = requests.get(link+"SellDat.json",headers=header)
                sh=r.json()["sha"]
                base64S= base64.b64encode(bytes(json.dumps(data), "utf-8"))
                rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
                response = requests.put(link+"SellDat.json", data=json.dumps(rjson), headers=header)
        else:
            await ctx.send("Bạn phải có quyền quản lý để dùng lệnh!")
            
    @client.command(aliases=["st"])            
    async def SellStop(ctx):
        if ctx.author.guild_permissions.administrator:
            nonlocal Selling
            Selling = False
            await ctx.send("Stop Successfully!")
        else:
            await ctx.send("Bạn phải có quyền quản lý để dùng lệnh!")
        
