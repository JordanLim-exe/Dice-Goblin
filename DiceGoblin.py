import discord
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command(name="roll")
async def roll(ctx):
    x = ctx.message.content.split(' ')
    num = x[1]
    out = str(random.randint(1,(int(num))))
    #place protectionary code here
    await ctx.reply(out)
    
@bot.command(name="ping")
async def ping(ctx):
    ret = ('@' + str(ctx.author))
    await ctx.reply(ret)



bot.run('OTcyMjkzNzY4MDcyMDMyMzQ2.GLRXuK.kcvXKYYuOquzE0CdOzufDS-WWfMHYt7GUfYHMQ')
