import discord
import json

from discord.ext import commands
from utilities import embed

utils = embed.API()

with open("authentication/config.json", "r") as file:
    token = json.load(file)["token"]

bot = commands.Bot(
    command_prefix='+', 
    intents=discord.Intents.all(),
)
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name="+help | %s Guilds" % (len(bot.guilds)), url="https://twitch.tv/discord"))

#Help
@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = utils.embed("Help", None)
    embed.add_field(name="**`+help info`**", value="**Shows information related commands.**", inline=False)
    embed.add_field(name="**`+help moderation`**", value="**Shows moderation related commands.**", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def info(ctx):
    embed = utils.embed("Information", None)
    embed.add_field(name="**`+serverinfo`**", value="**Returns information about the current server.**", inline=False)
    embed.add_field(name="**`+botinfo`**", value="**Shows information about the bot.**", inline=False)
    embed.add_field(name="**`+userinfo (@user]`**", value="**Shows information about the mentioned user.**", inline=False)
    embed.add_field(name="**`+avatar (@user]`**", value="**Returns the mentioned user's avatar.**", inline=False)
    embed.add_field(name="**`+membercount`**", value="**Returns the server's member count.**", inline=False)
    embed.add_field(name="**`+banner`**", value="**Returns the server banner.**", inline=False)
    embed.add_field(name="**`+serverpfp`**", value="**Returns the server icon.**", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def moderation(ctx):
    embed = utils.embed("Moderation", None)
    embed.add_field(name="**`+ban (@user)`**", value="**Bans the specified user.**", inline=False)
    embed.add_field(name="**`+kick (@user)`**", value="**Kicks the specified user.**", inline=False)
    embed.add_field(name="**`+slowmode (time)`**", value="**Sets slowmode to specified time.**", inline=False)
    embed.add_field(name="**`+unslowmode`**", value="**Disables slowmode.**", inline=False)
    embed.add_field(name="**`+purge (amount)`**", value="**Purges specified amount of messages.**", inline=False)
    await ctx.send(embed=embed)

#Commands
@bot.command()
async def serverinfo(ctx):
    embed = utils.embed("Server Info (%s)" % (ctx.guild.name), None)
    embed.add_field(name="**Server ID**", value="**`%s.`**" % (ctx.guild.id), inline=False)
    embed.add_field(name="**Server Name**", value="**`%s.`**" % (ctx.guild.name), inline=False)
    embed.add_field(name="**Server Owner**", value="**`%s.`**" % (ctx.guild.owner), inline=False)
    embed.add_field(name="**Created at**", value="**`%s.`**" % (ctx.guild.created_at), inline=False)
    embed.add_field(name="**Roles**", value="**`%s.`**" % (len(ctx.guild.roles)), inline=False)
    embed.add_field(name="**Total Members**", value="**`%s.`**" % (len(ctx.guild.members)), inline=False)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    else:
        pass
    await ctx.send(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed = utils.embed("Bot Info", None)
    embed.add_field(name="**Latency**", value="**`%sms.`**" % (bot.latency*1000), inline=False)
    embed.add_field(name="**Server Count**", value="**`%s.`**" % (len(bot.guilds)), inline=False)
    embed.add_field(name="**Developers**", value="**`Alvi.`**", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = utils.embed("User Info (%s)" % (member.name), None)
    embed.add_field(name="**Username**", value="**`%s`**." % (str(member)), inline=False)
    embed.add_field(name="**User ID**", value="**`%s`**." % (member.id), inline=False)
    embed.add_field(name="**Joined at**", value="**`%s`**." % (member.joined_at.strftime("%Y-%m-%d %H:%M:%S")), inline=False)
    embed.add_field(name="**Created at**", value="**`%s`**." % (member.created_at.strftime("%Y-%m-%d %H:%M:%S")), inline=False)
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(embed=utils.embed("Avatar (%s)" % (member), None).set_image(url=member.avatar.url))

@bot.command()
async def banner(ctx):
    if len(ctx.guild.banner_url) == 0:
        await ctx.send(embed=utils.embed("Banner (%s)" % (ctx.guild.name), "**`No Banner Found.`**"))
    await ctx.send(embed=utils.embed("Banner (%s)" % (ctx.guild.name)).set_image(url=ctx.guild.banner_url))

@bot.command()
async def serverpfp(ctx):
    if ctx.guild.icon_url == None:
        await ctx.send(embed=utils.embed("Sever pfp (%s)" % (ctx.guild.name), "**`No Server pfp Found.`**"))
    await ctx.send(embed=utils.embed("Sever pfp (%s)" % (ctx.guild.name)).set_image(url=ctx.guild.icon_url))

@bot.command()
async def membercount(ctx):
    await ctx.send(embed=utils.embed("Total Member (%s)" % (ctx.guild.name), None).add_field(name="Members", value="**`%s`**" % (len(ctx.guild.members))))

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members: 
        await member.ban(reason=reason)
        await ctx.send(embed=utils.embed("Ban", "**`Succesfully Banned (%s)`**" % (member)))
    else:
        await ctx.send(embed=utils.embed("Ban", "**`You don't have the necessary permissions to use this command.`**" % (member)))

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members: 
        await member.kick(reason=reason)
        await ctx.send(embed=utils.embed("Kick", "**`Succesfully Kicked (%s)`**" % (member)))
    else:
        await ctx.send(embed=utils.embed("Kick", "**`You don't have the necessary permissions to use this command.`**" % (member)))

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, duration: int, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.edit(slowmode_delay=duration)
    await ctx.send(embed=utils.embed("Slowmode", "**`Slow mode has been enabled in %s with a duration of %s seconds.`**" % (channel.mention, duration)))

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unslowmode(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.edit(slowmode_delay=0)
    await ctx.send(embed=utils.embed("Unslowmode", "**`Slow mode has been disabled in %s`**" % (channel.mention)))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(embed=utils.embed("Purge", "**`Successfully purged %s messages`**" % (amount)))

if __name__ == "__main__":
    bot.run(token)
