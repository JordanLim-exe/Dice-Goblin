import discord
import random
import os.path
from os import path
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

#class Events(commands.Cog):
#    def __init__(self, client):
#        self.client = client
#    
#    commands.Cog.listener()
#    async def on_guild_join(self, guild):
#        await 

def readData(server): #returns list with server data
    data = []
    if not path.exists(str(server) + ".txt"): #checking to see if file exists for server, create it if not
        file = open(str(server) + ".txt", "w")
        file.close
        return data
    else:
        file = open(str(server) + ".txt", "r")
        data = file.readlines()
        file.close()
        return data

def writeData(data, server): #writes list to file
    file = open(server + ".txt", "w")
    file.writelines(data)
    file.close()


def getNick(server, user):
    data = readData(server) #reads lines of file into list
    
    for entry in data: #searches for user id in file, if it exists returns nickname, else returns Guest
        x = entry.split("|")
        if str(x[0]) == str(user):
            if (len(x) == 2):
                return x[1][:-1]
            else:
                return x[1]
    return ("Guest")


def rollHelper(content, user, server):
    message = content.split(' ')
    save = message[1:]
    
    if len(save) > 1:
        save = ' '.join(save)
    else:
        save = ''.join(save)
    #place protectionary code here
    crit = False #to check if a die rolls max value

    if(not 'd' in message[1]):
        return
    
    dice = message[1].split('d') #getting how many and what size of dice

    #try:
    #making the modifer
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
    elif (len(message) > 2 and (message[2] != "adv" and message[2] != "dis")): #checking if a modifier was added
        dice = [int(n) for n in dice]
        modifier = int(message[3])
        if (message[2] == "-"):
            modifier *= -1 #making the mod negative if there's a minus sign
    #end making the modfier
    total = 0 #for the running total of dice

    output = ""

    for i in range(int(dice[0])): # loops through the number of dice
        if (message[len(message)-1] == "adv"):
            nums = [random.randint(1,(int)(dice[1])),random.randint(1,(int)(dice[1]))]
            total += max(nums[0],nums[1])
            nums = sorted(nums)
            output += "`~~{}~~ __{}__ ".format(nums[0],nums[1])
        elif (message[len(message)-1] == "dis"):
            nums = [random.randint(1,(int)(dice[1])),random.randint(1,(int)(dice[1]))]
            total += min(nums[0],nums[1])
            nums = sorted(nums)
            output += "~~{}~~ __{}__ ".format(nums[1],nums[0])
        else:
            total += random.randint(1,(int)(dice[1])) #adds a random value up to the size of dice
    
    if (dice[0] == 1 and dice[1] == total): #checking if the max value is rolled (only works for if there's only one die atm)
        crit = True
    
    total += modifier
    
    

    output += ("\n" if len(output)>0 else "") + str(total) #making the output a separate string so it can be modified easier
    
    if(crit):
        output = "**" + output + "**" #making the output bold if there's a crit
    
    nick = getNick(server, user)
    output = nick + " rolled a " + output
    
    data = readData(server)
    
    exists = False
    
    for i in range(len(data)): #checks to see if user already in file, overwrites nickname if they are
            temp = data[i].split("|")
            #print(temp[0])
            if str(temp[0]) == str(user):
                #print ("ID in use")
                if len(temp) < 2:
                    temp[1] = temp[1][:-1]
                    temp.append(save + "|" + str(total))
                    edited = '|'.join(temp) + "\n"
                    data[i] = edited
                else:
                    temp[2] = save
                    temp[3] = str(total)
                    edited = '|'.join(temp) + "\n"
                    data[i] = edited
                exists = True
    
    if exists == True:
        writeData(data, str(server))
    
    return output
        
    #except:
        #output = "failed to roll correctly"
        
        #return output

@bot.command(name="roll", help = "Rolls specified dice, >roll [x]d[y][+/-][z] [adv/dis]")
async def roll(ctx):
    #[x]d[y] +/- [z]
    output = rollHelper(str(ctx.message.content), ctx.author.id, ctx.guild.id)
    
    await ctx.reply(output)
    
@bot.command(name="stats", help= "Rolls stats for a new character, >stats [4d6] (default is 3d6) [reroll ones][once]")
async def stats(ctx):
    message = ctx.message.content
    reroll = [message.__contains__("reroll 1s") or message.__contains__("reroll ones"),message.__contains__("once")] #if 1s are rerolled and if it's once

    num_dice = 4 if message.__contains__("4") else 3;
    output = "{} {} {}\n".format("4d6 drop lowest" if num_dice==4 else "3d6","reroll 1s" if reroll[0] else "","once" if reroll[1] else "")
    for s in range(6):
        dice_rolls = []
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
                dice_rolls.append(num)
            dice_rolls = sorted(dice_rolls)
            for d in range(len(dice_rolls)):
                if (d == 0):
                    output += "~~{}~~".format(str(dice_rolls[d]))
                else:
                    output += " {}".format(str(dice_rolls[d]))
                    dice_sum += dice_rolls[d]
        output += " = (**{}**) \n".format(str(dice_sum))
    await ctx.send(output)    

@bot.command(name="ping", help = "Pong.")
async def ping(ctx):
    await ctx.reply("pong")
    
@bot.command(name="iam", help = "Registers a username, >iam [nickname]") #register a nickname to a user id
async def iam(ctx):
    server = str(ctx.guild.id) #gets server id
    data = readData(server) #reads current server data into a list

    x = ctx.message.content.split(" ") #splits message into list
    nick = x[1] #isolates nickname from message
    exists = False

    if "|" in nick or "\n" in nick: #ensure nickname does not contain seperator character
        reply = "Sorry, name may not contain invalid characters"
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

@bot.command(name="whoami", help = "Returns nickname of user if one is registered") #returns nickname of user if one is registered, otherwise returns Guest
async def whoami(ctx):
    ret = "You are " + str(getNick(ctx.guild.id, ctx.author.id)) + "!"
    await ctx.reply(ret)

@bot.command(name="prevres", help="Returns the result of the previous roll the user made") #returns result of last roll made by registered user
async def prevres(ctx):
    exists = False

    data = readData(ctx.guild.id) #reads data from saved file

    prevResult = ""
    rolled = ""
    nick = ""

    for entry in data: #checks to see if user is registered, grabs info if they are
        entry = entry.split('|')
        if str(entry[0]) == str(ctx.author.id):
            exists = True
            nick = entry[1]
            if len(entry) > 2:
                rolled = entry[2]
                prevResult = entry[3]
            else:
                nick = nick[:-1]
            
    
    if exists == True:
        if not prevResult == "": #user registered and has previous roll
            out = nick + " rolled " + rolled + " and got a result of " + prevResult
            await ctx.reply(out)
        else: #user registered but no previous rolls
            out = nick + " has made no previous rolls"
            await ctx.reply(out)
    else: #user not registered
        out = "Please register a nickname to save previous rolls and results!"
        await ctx.reply(out)


@bot.command(name="prevroll", help = "Repeats the last roll the user made") #repeats user's previous roll
async def prevroll(ctx):
    data = readData(ctx.guild.id)

    exists = False
    rolled = ""
    nick = ""

    for entry in data: #data collection
        entry = entry.split('|')
        if str(entry[0]) == str(ctx.author.id):
            exists = True
            nick = entry[1]
            if len(entry) > 2:
                rolled = entry[2]
            else:
                nick = nick[:-1]
    
    if exists == True:
        if not rolled == "": #user exists and has previous roll
            rolled = "roll " + rolled
            output = rollHelper(rolled, ctx.author.id, ctx.guild.id)
            await ctx.reply(output)
        else: #user exists but has no previous roll
            output = "There is no previous roll saved for " + nick
            await ctx.reply(output)
    else: #user is not registered
        output = "Please register a nickname to save previous rolls and results!"
        await ctx.reply(output)

# @bot.command(name="h")
# async def h(ctx):
#     output = ">roll [x]d[y][+/-][z] [adv/dis]\n>stats [4d6] (default is 3d6) [reroll ones][once]\n>iam [nickname]\n>whoami\n>prevroll\n>prevres"
#     await ctx.reply(output)

bot.run('OTcyMjkzNzY4MDcyMDMyMzQ2.GLRXuK.kcvXKYYuOquzE0CdOzufDS-WWfMHYt7GUfYHMQ')
