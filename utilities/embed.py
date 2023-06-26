import asyncio
import aiohttp
import discord
from discord.ext import commands

class API:
    def embed(self, title, description):
        embed = discord.Embed(title=title, description=description, color=0x1e2124)
        return embed
    