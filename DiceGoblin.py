import discord
import random
import os.path
from os import path
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

def readData(server): #returns list with server data
    data = []
    if not path.exists(server + ".txt"): #checking to see if file exists for server, create it if not
        file = open(server + ".txt", "w")
        file.close
        print(data)
        return data
    else:
        file = open(server + ".txt", "r")
        data = file.readlines()
        file.close()
        print(data)
        return data

def writeData(data, server): #writes list to file
    file = open(server + ".txt", "w")
    file.writelines(data)
    file.close()


def getNick(server, user):
    data = readData(server) #reads lines of file into list
    
    for entry in data: #searches for user id in file, if it exists returns nickname
        x = entry.split(" ")
        if x[0] == str(user):
            return x[1]
    return ("Guest")

@bot.command(name="roll")
async def roll(ctx):
    #[x]d[y] +/- [z]
    message = ctx.message.content.split(' ') #">roll","xdy","+/-","z"
    #place protectionary code here
    crit = False #to check if a die rolls max value

    if(not 'd' in message[1]):
        return
    
    dice = message[1].split('d') #getting how many and what size of dice

    try:
        modifier = 0
        if (len(message) == 2): #for either xdy or xdy+z (not spaces)
            nums = message[1]
            mod_sign = "/" #to note if there is a mod and its sign, '/' means there's no mod
            if nums.__contains__("+"):
                mod_sign = "+"
            elif nums.__contains__("-"):
                mod_sign = "-"
            
            if mod_sign == "/":
                dice = [int(n) for n in dice] #making the dice ints to be rolled from having no mod
            else:
                modifier = int( nums[nums.index(mod_sign):len(nums)] ) #getting the modifier number after the found sign
                dice[0] = int(dice[0])
                dice[1] = int(dice[1][0:dice[1].index(mod_sign)]) #making the dice ints for rolling while cutting off the sign and the modifier
        elif (len(message) > 2): #checking if a modifier was added
            dice = [int(n) for n in dice]
            modifier = int(message[3])
            if (message[2] == "-"):
                modifier *= -1 #making the mod negative if there's a minus sign
        total = 0 #for the running total of dice

        for i in range(dice[0]): # loops through the number of dice
            total += random.randint(1,(int)(dice[1])) #adds a random value up to the size of dice
        
        if (dice[0] == 1 and dice[1] == total): #checking if the max value is rolled (only works for if there's only one die atm)
            crit = True
        
        total += modifier

        output = str(total) #making the output a separate string so it can be modified easier

        if(crit):
            output = "**" + output + "**" #making the output bold if there's a crit
        
    except:
        output = "failed to roll correctly"
    
    await ctx.reply(output)
    
@bot.command(name="stats")
async def stats(ctx):
    message = ctx.message.content
    reroll = [message.__contains__("reroll 1s"),message.__contains__("once")] #if 1s are rerolled and if it's once

    num_dice = 4 if message.__contains__("4") else 3;
    output = "{} {} {}\n".format("4d6 drop lowest" if num_dice==4 else "3d6","reroll 1s" if reroll[0] else "","once" if reroll[1] else "")
    dice_rolls = []
    for s in range(6):
        dice_sum = 0
        if (num_dice== 3):
            for d in range(num_dice):
                num = random.randint(1,6)
                if reroll[0]:
                    if (num == 1):
                        output += "~~{}~~ ".format(str(num))
                        num = random.randint(1 if reroll[1] else 2,6)
                output += str(num) + " "
                dice_sum += num
        else:
            for d in range(num_dice):
                num = random.randint(1,6)
                if reroll[0]:
                    if (num == 1):
                        output += "~~{}~~ ".format(str(num))
                        num = random.randint(1 if reroll[1] else 2,6)
                #a = [1,2,3,4,1,2,1]
                #>> del a[a.index(min(a))]
                
        output += " = (**{}**) \n".format(dice_sum)
    await ctx.send(output)
    

@bot.command(name="ping")
async def ping(ctx):
    ret = "test: " + str(getNick(ctx.guild.id, ctx.author.id))
    print("We got here")
    await ctx.send(ret)
    
@bot.command(name="iam") #register a nickname to a user id
async def iam(ctx):
    server = str(ctx.guild.id) #gets server id
    data = readData(server) #reads current server data into a list

    x = ctx.message.content.split(" ") #splits message into list
    nick = x[1] #isolates nickname from message
    exists = False

    if "|" in nick: #ensure nickname does not contain seperator character
        reply = "Sorry, nicknames may not contain '|'."
        await ctx.reply(reply)
    else:
        if not data == []: #checks to see if the list is not empty
            for i in range(len(data)): #checks to see if user already in file, overwrites nickname if they are
                temp = data[i].split("|")
                #print(temp[0])
                if str(temp[0]) == str(ctx.author.id):
                    #print ("ID in use")
                    temp[1] = nick
                    edited = '|'.join(temp) + "\n"
                    data[i] = edited
                    exists = True

        if exists == True: #if the user existed, overwrite file
            writeData(data, server)
        else: #if not, add user to data and write to file
            out = str(ctx.author.id) + "|" + nick + "\n" #writes to file, format: [userid]|[nickname]
            data.append(out)
            writeData(data, server)
        reply = nick + " " + "has been registered!"
        await ctx.reply(reply)
        



bot.run('OTcyMjkzNzY4MDcyMDMyMzQ2.GLRXuK.kcvXKYYuOquzE0CdOzufDS-WWfMHYt7GUfYHMQ')
