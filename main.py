import discord
from discord.ext import commands
from Websocket.websocket import Websocket

class Vedantu(commands.Cog, Websocket):
    
    def __init__(self, client):
        super().__init__()
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready!")
        
    @commands.command(aliases = ["quiz", "nextved", "nextvedantu", "nextvd"])
    async def nextquiz(self, ctx):
        await self.quiz_details()
    
    @commands.command(aliases = ["open"])
    async def start(self, ctx):
        if not self.ws_is_opened:
            await self.send_hook("**Websocket Opened!**")
            await self.hook_start()
        else:
            await self.send_hook("**Websocket Already Opened!**")
            
    @commands.command()
    async def close(self, ctx):
        if self.ws_is_opened:
            await self.hook_close()
        else:
            await self.send_hook("**Websocket Already Closed!**")
            
client = commands.Bot(command_prefix = "-")
client.add_cog(Vedantu(client))
            
client.run("ODAzMTc1OTQ1OTMwMTQ1Nzky.YA594w.Hzq49nLxp-KzwFRKh9mqDvi3Mqg")
