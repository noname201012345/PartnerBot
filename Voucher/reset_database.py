import discord
from discord.ext import commands
import aiosqlite
from Voucher.config import onwer

def reset_dtb(client:commands.Bot):
    @client.tree.command(name="reset_data",description="Reset database")
    async def reset_data(interaction: discord.Interaction,member:discord.Member=None):
        if interaction.user.id == onwer:
            async with aiosqlite.connect("Voucher/main.db") as db:
                async with db.cursor() as cursor:
                    if member is not None:
                        await cursor.execute('SELECT info FROM users WHERE id = ?', (member.id,))
                        data = await cursor.fetchone()
                        if data is not None:
                            await cursor.execute('DELETE FROM users WHERE id= ?',(member.id,))
                            await cursor.execute('DELETE FROM vouch WHERE id= ?',(member.id,))
                        else:
                            await interaction.response.send_message(ephemeral=True, content=f"{member} doesn't have data")
                    else:
                        await cursor.execute('SELECT id FROM users')
                        data = await cursor.fetchall()
                        if data:
                            for x in range(len(list(data))):
                                id = list(data)[x][0]
                                await cursor.execute('DELETE FROM users WHERE id= ?',(id,))
                                await cursor.execute('DELETE FROM vouch WHERE id= ?',(id,))
                            await interaction.response.send_message(ephemeral=True, content="Reseted all database")
                        else:
                            await interaction.response.send_message(ephemeral=True, content="There's no data to reset")
                await db.commit()
        else:
            await interaction.response.send_message(ephemeral=True,content="You are not my onwer!")
    client.tree.clear_commands(guild=None)
    client.tree.add_command(reset_data)