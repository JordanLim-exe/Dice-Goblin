import discord
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command(name="roll")
async def roll(ctx):
    #[x]d[y] +/- [z]
    message = ctx.message.content.split(' ') #">roll","xdy","=/-","z"
    #place protectionary code here
    crit = False; #to check if a die rolls max value

    dice = message[1].split('d') #getting how many and what size of dice
    dice = [int(n) for n in dice] #making them ints

    modifier = 0;
    if (len(message) > 2): #checking if a modifier was added
        modifier = int(message[3])
        if (message[2] == "-"):
            modifier *= -1; #making the mod negative if there's a minus sign
    
    total = 0; #for the running total of dice

    for i in range(dice[0]): # loops through the number of dice
        total += random.randint(1,(int)(dice[1])) #adds a random value up to the size of dice
    
    if (dice[0] == 1 and dice[1] == total): #checking if the max value is rolled (only works for if there's only one die atm)
        crit = True;
    
    total += modifier

    output = str(total) #making the output a separate string so it can be modified easier

    if(crit):
        output = "**" + output + "**" #making the output bold if there's a crit
    
    await ctx.reply(output)
    
@bot.command(name="ping")
async def ping(ctx):
    ret = ('@' + str(ctx.author))
    await ctx.send(ctx.author.mention)



bot.run('OTcyMjkzNzY4MDcyMDMyMzQ2.GLRXuK.kcvXKYYuOquzE0CdOzufDS-WWfMHYt7GUfYHMQ')
