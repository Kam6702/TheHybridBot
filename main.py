
import discord
from keep_alive import keep_alive
from discord.utils import get
from discord.ext import commands, tasks
import random, os
from replit import db
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions
import json
import inspect
import resource, psutil
import time
import datetime
import country_converter as coco
from discord import Color
import logging
import flask
import pip
from discord.ext import commands
from discord.ext.commands import check
import motor.motor_asyncio
import sys
import urllib.request
import re
import requests
import aiohttp
import math
import re
import numpy
import requests
from discord.ext import commands
import contextlib
import io
import os
import discord
import random
from random import shuffle
from dotenv import load_dotenv
from discord.ext import commands
from collections import Counter
from jishaku.cog import STANDARD_FEATURES

bad_words = []



#status and ready
#prefix
def get_prefix(bot, msg):

	if str(msg.guild.id) not in db.keys():
		db[str(msg.guild.id)] = '.'
		return '.'

	else:
		prefixes = db[str(msg.guild.id)]
		return prefixes

# Configure intents (1.5.0)
intents = discord.Intents.default()
intents.members = True
description = '''__A custom discord bot for moderation!__'''


client = commands.Bot(command_prefix=get_prefix, description=description, case_insensitive=True, intents=discord.Intents.all(), help_command=None)



target = ()
scoreboard = {}

@client.command(name='scramble', help='Play a simple word scramble game. Guess the word to win.')
async def playScramble(ctx):

	global target
	if target:
		await ctx.send('The current word is {}. If you would like a different one, first !reset and !scramble again.'.format(target[0]))
	else:
		target = chooseWord()
		await ctx.send('Your scrambled word is: {}. Good Luck!'.format(target[0]))

@client.command(name='unscramble', help='Make a guess on the word. Use in the form guess <Your Guess>')
async def guessScramble(ctx, userGuess):

	global target
	global scoreboard

	if not target:
		await ctx.send('There is no current word, please !scramble to play')
		return

	if userGuess == target[1]:
		winner = ctx.author.name
		await ctx.send('CORRECT, YOU GOT 5 POINTS')
		if winner not in scoreboard:
			scoreboard[winner] = 0
		scoreboard[winner] += 5
		await ctx.send('Current Score for {}: {}'.format(winner, scoreboard[winner]))
		reset()


@client.command(name='reset', help='Use this to reset the scrambled word, must !scramble again after')
async def resetScramble(ctx):

	reset()
	await ctx.send('Word has been reset, must !scramble again for new word')

@client.command(name='resetscore', help='Reset the Scoreboard, this is irreversible, use with care')
@has_permissions(manage_channels=True)
async def resetScoreboard(ctx):
	global scoreboard
	scoreboard = {}

	await ctx.send('The scores have been reset')


@client.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: {args[0]}\n')
		else:
			raise

def chooseWord():
	lines = open('wordbank.txt').read().splitlines()
	scrambled = [shuffleWord(word) for word in lines]
	return random.choice(scrambled)

def shuffleWord(word):
	original = word
	word = list(word)
	shuffle(word)
	return ''.join(word), original

def reset():
	global target
	target = ()







class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

client.help_command = MyHelpCommand()


@client.command()
async def embed(ctx):#
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('Waiting for a title.')
    title = await client.wait_for('message', check=check)
  
    await ctx.send('Waiting for a description.')
    desc = await client.wait_for('message', check=check)

    embed = discord.Embed(title=title.content, description=desc.content, color=0x72d345)
    await ctx.send(embed=embed)


        
@client.command()
@has_permissions(manage_channels=True)
async def createchannel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        await ctx.send(f'Created a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@client.event
async def on_member_join(member): 
  
  
    embed=discord.Embed(
        title="Welcome "+member.name+"!",
        description="We hope you brought ice cream!",
        color=discord.Color.red())
    
    channel = await client.get_channel(867679274559471647)
    

    await channel.send(embed=embed)
    
 
@client.command()
async def invites(ctx, usr: discord.Member=None):
    if usr == None:
       user = ctx.author
    else:
       user = usr
    total_invites = 0
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == user:
            total_invites += i.uses
    await ctx.send(f"{user.name} has invited {totalInvites} member{'' if totalInvites == 1 else 's'}!")
 
@client.command()
async def calc(ctx, *, arg):
      result = eval(arg)
      await ctx.send(result)
    
@client.command()
async def rolldice(ctx):
    message = await ctx.send("Choose a number:\n**4**, **6**, **8**, **10**, **12**, **20** ")
    
    def check(m):
        return m.author == ctx.author

    try:
        message = await client.wait_for("message", check = check, timeout = 30.0)
        m = message.content

        if m != "4" and m != "6" and m != "8" and m != "10" and m != "12" and m != "20":
            await ctx.send("Sorry, invalid choice.")
            return
        
        coming = await ctx.send("Here it comes...")
        time.sleep(1)
        await coming.delete()
        await ctx.send(f"**{random.randint(1, int(m))}**")
    except asyncio.TimeoutError:
        await message.delete()
        await ctx.send("Procces has been canceled because you didn't respond in **30** seconds.")





@client.command()
@has_permissions(kick_members=True)
async def report(ctx, member:discord.Member, *, arg):
    author = ctx.author
    guild = ctx.guild
    channel = get(guild.text_channels, name='warn-logs')
    if channel is None:
        channel = await guild.create_text_channel('warn-logs')
    await channel.send(f'{member.mention} warned for: {arg} warned by: {author.mention}')
    await member.send(f'{author.mention} warned you for: {arg}')
    await ctx.message.delete()

async def presence():
    while True:
	        servers = len(client.guilds)
	        members = 0
	        for guild in client.guilds:
		          members += guild.member_count - -0


	        await client.change_presence(activity=discord.Activity(
	        type=discord.ActivityType.watching,
	        name=f'{servers} servers and {members} members'))
	        
	        
	        await asyncio.sleep(10)
	        

	        await client.change_presence(activity=discord.Activity(
	        type=discord.ActivityType.playing,
	        name=f'hybridbot.app | help'))
	        
	        await asyncio.sleep(10)




@client.event
async def on_ready():
  
  
  
 
   print('Bot up')
   
  


   await client.loop.create_task(presence())

@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@client.command(pass_context=True)
async def say(ctx, *, message):

	await ctx.message.delete()
	await ctx.send(message)


@client.command()
async def args(ctx, *args):
    no_args = len(args)
    await ctx.send(f"{no_args} args")




@client.command()
async def removechannel(ctx, channel: discord.TextChannel):
    await channel.delete()
    await ctx.send("Successfully deleted the channel!")

@client.command()
async def editchannel(ctx, channel: discord.TextChannel, new_name):
  await channel.edit(name=new_name)
  await ctx.send(f'Channel name changed to {new_name}')


def restart_client():
	os.execv(sys.executable, ['python'] + sys.argv)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def restart(ctx):
	await ctx.send("Restarting bot...")
	
	await asyncio.sleep(2)
	
	await ctx.send('Bot sucessfully restarted')
	restart_client()



@client.command(pass_context=True)
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')



@client.listen()
async def on_message(message):
  if message.content == ('prefix?'):
    await message.channel.send(f'Prefix = `{db[str(message.guild.id)]}`')


@client.command()
async def addpremium(ctx, user : discord.Member):
    if ctx.author.id != 637884461161381899: #put your user id on discord here
        return

    with open("premium_users.json") as f:
        premium_users_list = json.load(f)

    if user.id not in premium_users_list:
        premium_users_list.append(user.id)

    with open("premium_users.json", "w+") as f:
        json.dump(premium_users_list, f)

    await ctx.send(f"{user.mention} has been added!")
    

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

@client.command()
async def server(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)
  text_channels = len(ctx.guild.text_channels)
  voice_channels = len(ctx.guild.voice_channels)
  categories = len(ctx.guild.categories)
  roles = len(ctx.guild.roles)
  channels = text_channels + voice_channels

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.blue()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)
  embed.add_field(name="Channel Count", value=f"Channels: {channels}, Channels; {text_channels}: Text, {voice_channels}: Voice, {categories}: Categories")
  embed.add_field(name='Verification Level', value=f'Verification: {str(ctx.guild.verification_level).upper()}')
  embed.add_field(name='Creation Date', value=f'Creation: {ctx.guild.created_at.strftime(format)}')
  embed.add_field(name='Roles', value=f'Roles: {roles}')

  await ctx.send(embed=embed)





@client.command(pass_context=True)
async def badges(ctx, user: discord.Member):
    # Remove unnecessary characters
    hypesquad_class = str(user.public_flags.all()).replace('[<UserFlags.', '').replace('>]', '').replace('_',
                                                                                                         ' ').replace(
        ':', '').title()

    # Remove digits from string
    hypesquad_class = ''.join([i for i in hypesquad_class if not i.isdigit()])

    # Output
    test = discord.Embed(title=f"{user.name} User's Badges", description=f"{hypesquad_class}", color=0xff0000)
    await ctx.channel.send(embed=test)



ban_list = []
day_list = []
server_list = []

#This is a background process
async def countdown():
    await client.wait_until_ready()
    while not client.is_closed:
        await asyncio.sleep(1)
        day_list[:] = [x - 1 for x in day_list]
        for day in day_list:
            if day <= 0:
                try:
                    await client.unban(server_list[day_list.index(day)], ban_list[day_list.index(day)])
                except:
                    print('Error! User already unbanned!')
                del ban_list[day_list.index(day)]
                del server_list[day_list.index(day)]
                del day_list[day_list.index(day)]
               
#Command starts here
@client.command(pass_context = True)
@has_permissions(ban_members=True)
async def tempban(ctx,member:discord.Member, days = 1):
            await client.ban(member, delete_message_days=0)
            await ctx.send('User banned for **' + str(days) + ' day(s)**')
            ban_list.append(member)
            day_list.append(days * 24 * 60 * 60)
            server_list.append(ctx.message.server)
    

client.loop.create_task(countdown())








@client.command(help="Play with .rps then type [your choice]")
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"Rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await client.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock':
        if comp_choice == 'rock':
            await ctx.send(f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'paper':
        if comp_choice == 'rock':
            await ctx.send(f'The pen beats the sword? More like the paper beats the rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw man, you actually managed to beat me.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'scissors':
        if comp_choice == 'rock':
            await ctx.send(f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Bruh. >: |\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")




@client.command()
async def removepremium(ctx, user : discord.Member):
    if ctx.author.id != 637884461161381899: #put your user id on discord here
        return

    with open("premium_users.json") as f:
        premium_users_list = json.load(f)

    if user.id in premium_users_list:
        premium_users_list.remove(user.id)
    else:
        await ctx.send(f"{user.mention} is not in the list, so they cannot be removed!")
        return

    with open("premium_users.json", "w+") as f:
        json.dump(premium_users_list, f)

    await ctx.send(f"{user.mention} has been removed!")

def check_if_user_has_premium(ctx):
    with open("premium_users.json") as f:
        premium_users_list = json.load(f)
        if ctx.author.id not in premium_users_list:
            return False

    return True

@client.command()
@check(check_if_user_has_premium)
async def apremiumcommand(ctx):
    await ctx.send("Hello premium user!")


@client.command()
@has_permissions(manage_messages=True)
async def userinfo(ctx, *, user: discord.Member = None): # b'\xfc'
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)


@client.command()
@has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")




@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member):
	role = discord.utils.get(ctx.guild.roles, name="Muted")
	guild = ctx.guild
	if role not in guild.roles:
		perms = discord.Permissions(send_messages=False, speak=False)
		await guild.create_role(name="Muted", permissions=perms)
		await member.add_roles(role)
		await ctx.send(
		    "Successfully created Muted role and assigned it to mentioned user."
		)
	else:
		await member.add_roles(role)
		await ctx.send(f"Successfully muted {member}")


@mute.error
async def mute_error(ctx, error):
	if isinstance(error, commands.MissingRole):
		await ctx.send("You don't have the 'staff' role")
	elif isinstance(error, commands.BadArgument):
		await ctx.send("That is not a valid member")

''''
@client.event
async def on_ready():


 role = discord.utils.get(ctx.guild.roles, name="💰Patron")
 with open("premium_users.json") as f:
        premium_users_list = json.load(f)

guild = ctx.guild
if role in guild.roles:
   with open("premium_users.json", "w+") as f:
        json.dump(premium_users_list, f)

'''




@client.listen()
async def on_message(message):

  msg = message.content

  if any(word in msg for word in bad_words):

      await message.delete()
      
      await message.channel.send('No swearing, please read the server rules')

@client.command()
async def prefix(ctx, *, prefix):
	if ctx.message.author.guild_permissions.administrator:
		db[ctx.guild.id] = prefix

		await ctx.channel.send(f"Prefix has been changed to `{prefix}`")
	else:
		await ctx.channel.send(
		    "You don't have the sufficient permissions to do that")







    
 
    
    
    
@client.command(pass_context = True)
async def randomnumber(ctx):

   embed = discord.Embed(title= 'Ramdom Number', description = (random.randint(1,101)), color = (0xF85252))
   await ctx.send(embed=embed)


determine_flip = [1, 0]

@client.command()
async def flip(ctx):
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(title="Coinflip :coin:", description=f"{ctx.author.mention} Flipped coin, we got **Heads**!")
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Coinflip :coin:", description=f"{ctx.author.mention} Flipped coin, we got **Tails**!")
        await ctx.send(embed=embed)


@client.command(name='8ball',
            description="Answers a yes/no question.",
            brief="Answers from the beyond.",
            aliases=['eight_ball', 'eightball', '8-ball'],
            pass_context=True)

async def eight_ball(context):
    possible_responses = [

        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'Maybe so.'

    ]
    await context.channel.send(random.choice(possible_responses) + ", " + context.message.author.mention)



#kick
@client.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
	await user.kick(reason=reason)
	kick = discord.Embed(
	    title=f":boot: Kicked {user.name}!",
	    description=f"Reason: {reason}\nBy: {ctx.author.mention}")
	await ctx.message.delete()
	await ctx.channel.send(embed=kick)
	await user.send(embed=kick)


@client.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
	await user.ban(reason=reason)
	ban = discord.Embed(
	    title=f":boom: Banned {user.name}!",
	    description=f"Reason: {reason}\nBy: {ctx.author.mention}")
	await ctx.message.delete()
	await ctx.channel.send(embed=ban)
	await user.send(embed=ban)






#unmute
@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, reason: str = None):
	role = discord.utils.get(ctx.guild.roles, name="Muted")
	await member.remove_roles(role)
	await ctx.send(f"{member} has been unmuted.")


#unban
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, member: int):
	member = await client.fetch_user(str(member))
	banned_users = await ctx.guild.bans()
	for ban_entry in banned_users:
		user = ban_entry.user
		if user.id == member.id:
			try:
				message2 = f"You have been unbanned from {ctx.guild.name}"

				await member.send(message2)
			except:
				pass

			await ctx.guild.unban(user)
			await ctx.send(f"{member} has been unbanned!")


@client.command(name='purge', help='Purges a number of messages in a channel')
@commands.has_permissions(administrator=True)
async def purge(ctx, amount=100):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages cleared by {ctx.author.mention}')
        await ctx.message.delete()

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
  
 


  

#say






#embed links


@client.command()
async def links(ctx):
	embed = discord.Embed(
	    title='All links',
	    description=
	    '[Click here for our Twitter](https://twitter.com/bot_hybrid) \n [Click here for our Instagram](https://instagram.com/hybridsupportbot) \n [Click here for website](https://www.hybridbot.app) \n [Invite Hybrid to your server](https://discord.com/api/oauth2/authorize?client_id=851572977195941899&permissions=8&scope=bot%20applications.commands) \n [Join our support server](https://discord.gg/n4QwhDbm4M)'
	)
	await ctx.send(embed=embed)


#staff
@client.command()
async def staff(ctx):
	embed = discord.Embed(
	    title=
	    'Everyone who contributed to the bot, site, and/or suppport server',
	    description=
	    'Creators- Kam, \n Devs- Kam, Kaz, Coder N, applepro223 \n Discord Admins- Kam, Kaz, applepro223 \n Discord Staff- Kam, Kaz, Coder N, Nicholas Wang, applepro223'
	)
	await ctx.send(embed=embed)


cc = coco.CountryConverter()
global main_up
main_up = time.time()

cc = coco.CountryConverter()





@client.event
async def on_member_join(member):
    if int(member.guild.id) == 867679274559471647:
      channel = await client.get_channel(867679274559471647)
      
      await channel.send(f"{member.mention} has joined")


@client.event
async def on_member_remove(member):
    if int(member.guild.id) == 867679274559471647:
      channel = await client.get_channel(867679274559471647)
      
      await channel.send(f"{member.name} has left")


@client.command()
async def history(ctx, member: discord.Member):
    counter = 0
    async for message in ctx.channel.history(limit = 100):
        if message.author == member:
            counter += 1

    await ctx.send(f'{member.mention} has sent **{counter}** messages in this channel.')

@client.listen()
async def on_message(message):
  if message.content == '.history':
    await message.channel.send('Please mention a user')




  

@client.command()
async def botinfo(ctx):
  current_process = psutil.Process()
  cpu_usage = current_process.cpu_percent()
  memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000
  current_time = time.time()
  difference = int(round(current_time - main_up))
  text = str(datetime.timedelta(seconds=difference))
  guild=discord.guild
  embed = discord.Embed(title="__Bot info__", color = Color.red())

  
  embed.add_field(name='Servers', value=f'''```css
[{len(client.guilds)} servers]
```''')

  embed.add_field(name='CPU usage', value=f'''```css
[{cpu_usage}%]
```''', inline=True)
  
  embed.add_field(name='Uptime', value=f'''```css
[{text}]
```''')
  embed.add_field(name='Memory usage', value=f'''```ini
[{memory} kb]
```''')


  embed.add_field(name='Creator', value=f'''```ini
[Kam#7171, Hybrid Bot Development Team]
```''', inline=True)

  embed.add_field(name='Websocket Ping', value=f'''```ini
[{client.latency * 1000} ms]
```''')

  embed.add_field(name='Commands', value=f'''```css
  [{len(client.commands)}]```''')
  
  embed.add_field(name='Premium Users', value=f'''```ccs
  [3]```''')

  await ctx.send(embed=embed)



  


@client.command()
async def guess(ctx, *, number=0):
	number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	correct_number = random.choice(number_list)

	if number == correct_number:
		embedVar = discord.Embed(title=f'Your Number Is {number}',
		                         color=0x00FF00)
		embedVar.add_field(name='You Picked The Correct Number! You Won',
		                   value="Thanks For Playing!")
		await ctx.send(embed=embedVar)

	else:
		embedVar = discord.Embed(title=f'Your Number Is {number}',
		                         color=0xFF0000)
		embedVar.add_field(
		    name=
		    f"Sorry, You Picked The Wrong Number. The correct number was {correct_number}.",
		    value="Thanks For Playing")
		await ctx.send(embed=embedVar)






@client.command(pass_context=True)
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')


@client.command()
@has_permissions(manage_channels=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")

@client.command()
@has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")




player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver
    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            myEmbed = discord.Embed(title= "GAME IN PROGRESS",description="IT IS <@" + str(player1.id) + ">'s TURN.",color=0xe74c3c)
            await ctx.send(embed=myEmbed)
        elif num == 2:
            turn = player2
            myEmbed = discord.Embed(title= "GAME IN PROGRESS",description="IT IS <@" + str(player2.id) + ">'s TURN.",color=0xe74c3c)
            await ctx.send(embed=myEmbed)
    else:
        myEmbed = discord.Embed(title= "GAME IN PROGRESS",description="A GAME IS STILL IN PROGRESS. FINISH IT BEFORE STARTING A NEW ONE",color=0xe74c3c)
        await ctx.send(embed=myEmbed)

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    myEmbed = discord.Embed(title= "WINNER!",description=mark + " :crown: ",color=0xf1c40f)
                    await ctx.send(embed=myEmbed)
                elif count >= 9:
                    gameOver = True
                    myEmbed = discord.Embed(title= "TIE",description="IT'S A TIE :handshake:",color=0xf1c40f)
                    await ctx.send(embed=myEmbed)

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                myEmbed = discord.Embed(title= "PLACE ERROR!",description="BE SURE TO CHOOSE AN INTEGER BETWEEN 1 AND 9 (INCLUSIVE) AND AN UNMARKED TILE. ",color=0xe74c3c)
                await ctx.send(embed=myEmbed)
        else:
            myEmbed = discord.Embed(title= "TURN ERROR!",description="IT'S NOT YOUR TURN",color=0xe74c3c)
            await ctx.send(embed=myEmbed)
    else:
        myEmbed = discord.Embed(title= "START GAME",description="TO START A NEW GAME, USE -tictactoe COMMAND",color=0x2ecc71)
        await ctx.send(embed=myEmbed)


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        myEmbed = discord.Embed(title= "MENTION ERROR!",description="PLEASE MENTION 2 USERS",color=0xe74c3c)
        await ctx.send(embed=myEmbed)
    elif isinstance(error, commands.BadArgument):
        myEmbed = discord.Embed(title= "ERROR!",description="PLEASE MAKE SURE TO MENTION/PING PLAYERS (ie. <@688534433879556134>)",color=0xe74c3c)
        await ctx.send(embed=myEmbed)

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        myEmbed = discord.Embed(title= "NO POSITION",description="PLEASE ENTER A POSITION TO MARK",color=0xe74c3c)
        await ctx.send(embed=myEmbed)
    elif isinstance(error, commands.BadArgument):
        myEmbed = discord.Embed(title= "INTEGER ERROR!",description="PLEASE MAKE SURE IT'S AN INTEGER",color=0xe74c3c)
        await ctx.send(embed=myEmbed)



@client.command()
async def end(ctx):
        # We need to declare them as global first
        global count
        global player1
        global player2
        global turn
        global gameOver
        
        # Assign their initial value
        count = 0
        player1 = ""
        player2 = ""
        turn = ""
        gameOver = True
        
        await ctx.send('Game Over')



@client.command(pass_context = True)
async def warnings(ctx,user:discord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.send(f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}")
      break
  else:
    await ctx.send(f"{user.name} has never been reported")  



@client.command()
async def premiumrates(ctx):
  embed = discord.Embed(title='Premium Rates', description='Hybrid Bot Premium will be available on Patreon for $5/month starting in early August')

  await ctx.send(embed=embed)
  

@client.command()
async def calendar(self, ctx, month: str = None, year: int = None):

        months = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }
        # In month was not passed, use the current month
        if month is None:
            month = datetime.date.today().month
        else:
            month = months.get(month.lower())
            if month is None:
                await ctx.send("Please provide a valid Month!")
                return
        # If year was not passed, use the current year
        if year is None:
            year = datetime.datetime.today().year
        # Here we create the actual "text" calendar that we are printing
        cal = calendar.TextCalendar().formatmonth(year, month)
        await ctx.send("```\n{}```".format(cal))


@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)




@client.command()
async def back(ctx, *, arg):
  
  await ctx.message.delete()
  
  await ctx.send(arg[::-1].strip('@'))


player1 = ""
player2 = ""
turn = ""
numturn = 0
count_render = 0
board_render = []
board = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]
gameOver = True
modes = 1

@client.command(aliases=['connect'])
async def connectfour(ctx,p1:discord.Member,p2:discord.Member):
    global player1
    global player2
    global gameOver
    global turn
    global modes

    if gameOver:
        global board
        global numturn
        board = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]
        player1 = p1.name
        player2 = p2.name

        board_render = []
        count_render = 0
        num = random.randint(1,2)
        if num == 1:
            numturn = 1
            turn = player1
        elif num == 2:
            numturn = 2
            turn = player2
        for count, i in enumerate(board):
            if ([0, 0, 0, 0, 0, 0, 0, 0]== i) and count_render <= 3:
                count_render +=1
                board_render.append(i)
            elif count_render <= 3:
                board_render.append(i)
            
        board_render.reverse()
        await ctx.send(render(board_render))
        await ctx.send("{} Turn!".format(turn))
        board_render.reverse()
        gameOver = False
    else:
        await ctx.send("Game is already start.")
    
        
@client.command(aliases=['d'])
async def drop(ctx,num:int):
    global player1
    global player2
    global gameOver
    global turn
    global modes

    if not gameOver:
        global board
        global numturn

        counts = 0
        count_render = 0
        board_render = []
        count_tie = 0
        if turn == ctx.author.name:
            for count, i in enumerate(board):
                if ([0, 0, 0, 0, 0, 0, 0, 0]== i) and count_render <= 3:
                    count_render +=1
                    board_render.append(i)
                elif count_render <= 3:
                    board_render.append(i)
            for count, i in enumerate(board):
                if i[num-1] == 0:
                    counts += 1
                    board[count][num-1] = numturn
                    win = windetect(board,turn)
                    if win:
                        board_render.reverse()
                        line = ''
                        await ctx.send(render(board_render))
                        gameOver = True
                            # time.sleep(0.3)
                        await ctx.send("{} win!".format(turn))
                        await ctx.send(":partying_face: Congratulations!")
                        board_render.reverse()
                        return
                    if turn == player1:
                        numturn= 2
                        turn = player2
                    else:
                        numturn = 1
                        turn = player1
                    board_render.reverse()
                    for i in board:
                        print(i)
                    line = ''
                    await ctx.send(render(board_render))
                    await ctx.send("{} Turn!".format(turn))
                    print("{} Turn!".format(turn))
                    print()
                    board_render.reverse()
                    return
                for y in i:
                    if y == 0:
                        count_tie += 1
                if count_tie == 0:
                    counts += 1
                    if modes == 1:
                        await ctx.send(render(board_render))
                    elif modes == 2:
                        await ctx.send(embed=render(board_render))
                    await ctx.send("Tie!")
                    return
        else:
            await ctx.send("It's not your turn")
            counts += 1
        if counts == 0:
            await ctx.send("Column is full please select anothor column.")
    else:
        await ctx.send("Please start with .connectfour command.")

def render(board_render):
    line=''
    global modes
    for count,x in enumerate(board_render):
        for y in x:
            if y == 0:
                line += (":white_medium_square:" + ' ')
            elif y == 1:
                line += (":red_circle:" + ' ')
            elif y == 2:
                line += (":yellow_circle:" + ' ')
        if count <= len(board_render)-2:
            line += "\n"
    return line


def windetect(board,turn):
    global numturn
    boardHeight = len(board)
    boardWidth = len(board[0])
    tile = numturn

    # check horizontal spaces
    for y in range(boardHeight):
        for x in range(boardWidth - 3):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
    
    # check vertical spaces
    for x in range(boardWidth):
        for y in range(boardHeight - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True
    
    # check / diagonal spaces
    for x in range(boardWidth - 3):
        for y in range(3, boardHeight):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True

    # check \ diagonal spaces
    for x in range(boardWidth - 3):
        for y in range(boardHeight - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False   

@client.command()
async def stop(ctx):
    global gameOver
    if not gameOver:
        gameOver = True
        await ctx.send("The Game is stop.")
        print("The Game is stop.")
    else:
        await ctx.send("The Game has stopped")
        print("The Game has stopped")

@client.command()
async def mode(ctx,mode):
    global modes
    if mode == '1':
        modes = 1
        await ctx.send("Change to mode 1.")
    if mode == '2':
        modes = 2
        await ctx.send("Change to mode 2.")


@mode.error
async def mode_error(ctx,error):
    global modes
    text = "Mode:\n    1. Play in 1 device\n    2. Play with your friend\nCurrent: {}".format(modes)
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(text)
      
def setup(client):
    client.load_extension('cogs.Moderation')
    client.load_extension('jishaku')


keep_alive()
setup(client)
client.run(os.environ['TOKEN'])

#__author__ = "Kamran Noei"
#__copyright__ = "Copyright (C) 2021 Kamran Noei”
#__license__ = "Private Domain"
#__version__ = "1.0"


#imports


