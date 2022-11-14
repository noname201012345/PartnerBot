import discord
from discord.ext import commands
   
    
def Team(client:discord.Client):
    @client.command(aliases=["cteam","ct"])
    async def CreateTeam(ctx, mem: discord.Member , *tup):
        name = " ".join(tup)
        tname = name[0:name.find(" 0x")]
        color = name[name.find("0x"):len(name)]
        if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_channels:
            Role = await ctx.guild.create_role(name=f"CLB • {tname}",color=int(color,16),mentionable=True)
            perm = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
            perm[Role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
            perm[mem] = discord.PermissionOverwrite(manage_nicknames=True,mute_members=True,manage_channels=True,manage_messages=True)
            CLB = await client.get_channel(1011645607447896164).create_text_channel(f"🏫┃{tname} chat",overwrites=perm)
            await mem.add_roles(Role)
            await ctx.send(f"Tạo Team <@&{Role.id}> thành công")
        else:
            await ctx.send(f"Bạn phải là quản lý hoặc có quyền tạo phòng để tạo Team mới!")
            
    @client.command(aliases=["am","addm"])
    async def AddMem(ctx,mem:discord.Member):
        find = None
        for x in client.get_channel(1011645607447896164).channels:
            if x.name.startswith("🏫┃"):
                for y in x.overwrites:
                    if type(y) == discord.Member:
                        if y.id == ctx.author.id:
                            find = x
        if find is not None:
            for x in find.overwrites:
                if type(x) == discord.Role:
                    if x is not ctx.guild.default_role:
                        await mem.add_roles(x)
            await ctx.send("Thêm thành viên mới thành công!")
        else:
            await ctx.send("Bạn không phải chủ của một team!")