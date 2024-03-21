import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from wereComm import wereComm
from MultiChat import MultiChat
from team import Team
from Voucher.main import Vouching
from seller import Sell
from PIL import Image

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='s.', intents=intents,help_command=None)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} ({client.user.id})')
  
  
'''
@client.command()
async def help(ctx):
    helpEmbed = discord.Embed(title="Các lệnh của Bot:",color=0x00FFF3,description=f"**Prefix:** {client.command_prefix}\n\n> **Lệnh MultiChat:**\n\n• **msview** - Xem các phòng chat liên server\n• **join** __*tên phòng chat*__ - Tham gia một phòng chat\n• **leave** - Rời phòng chat hiện tại\n• **msban** __*id*__ - Ban người có id trong câu lệnh khỏi phòng chat\n• **create** __*tên phòng chat*__ - Tạo phòng chat liên server mới\n\n> **Lệnh Ma Sói:**\n\n• **wwcreate** - Tạo danh mục ma sói (bắt buộc phải tạo nếu muốn chơi ma sói)\n• **werewolf** __*tên phòng*__ - Tạo phòng ma sói\n• **joinww** __*tên phòng*__ - Tham gia phòng ma sói\n• **delww** - Xóa phòng ma sói bạn là chủ phòng\n• **leadww** __*người chơi*__ - Chuyển chủ phòng cho người khác\n• **leaveww** - Rời khỏi phòng ma sói\n• **roomww** - Kiểm tra các phòng ma sói hiện có\n• **setupww** - Setup phòng ma sói của bạn\n• **wwstart** - Bắt đầu game ma sói")
    helpEmbed.set_author(name="Gamer Hệ Đần",icon_url=client.get_guild(1010936069329522731).icon.url,url="https://discord.gg/gamerhedan")
    await ctx.send(embed=helpEmbed)
    '''
    
    
#wereComm(client=client)
#MultiChat(client=client)
#Team(client=client)
#Vouching(client=client)
#Sell(client=client)
       
token = os.getenv("token")
client.run(token)