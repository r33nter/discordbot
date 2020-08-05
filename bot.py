import discord
from discord.ext import commands
import random
import asyncio
import time
import urbandictionary
import traceback
import bs4
from selenium import webdriver
import sys
from apiclient.discovery import build
from discord.ext.commands.cooldowns import BucketType




client = commands.Bot(command_prefix = '.')
client.remove_command('help')


######## error handling
@client.event
async def on_command_error(ctx, error):
	
	if isinstance(error, commands.BotMissingPermissions):
		await ctx.send("Hey! I can't do this command unless you give me some perms!")
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Missing required argument!")
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("Hey! You do not have the required permissions to preform this command!")
	if isinstance(error, commands.TooManyArguments):
		await ctx.send("Too many arguments!")
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Command doesn't exist buddy. Refer to .help")
	if isinstance(error, commands.MissingRole):
		await ctx.send("You do not have permission to use this command!")
	if isinstance(error, commands.CommandOnCooldown):
		if ctx.message.author.guild_permissions.manage_roles:
			await ctx.reinvoke()
			return
		await ctx.send(error)
	# get data from exception
	etype = type(error)
	trace = error.__traceback__

# the verbosity is how large of a traceback to make
# more specifically, it's the amount of levels up the traceback goes from the exception source
	verbosity = 4

# 'traceback' is the stdlib module, `import traceback`.
	lines = traceback.format_exception(etype, error, trace, verbosity)

# format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
	traceback_text = ''.join(lines)

# now we can send it to the user
# it would probably be best to wrap this in a codeblock via e.g. a Paginator
	print(traceback_text)
	
	
### EVENTS
@client.event
async def on_ready():
    print('bot is ready')

#reactionroles


client.checkonetwo = True

client.guild_reactions = {
	
}
@client.event
async def on_raw_reaction_add(payload):
	
	print(payload.message_id)
	print(client.guild_reactions[payload.guild_id])
	if payload.message_id == client.guild_reactions[payload.guild_id]:
		if 1==1:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

			role = discord.utils.get(guild.roles, name=str("r33nterbot"))
			if role != None:
				member = discord.utils.find(lambda m : m.id == payload.member.id, guild.members)
				if member != None:
					await member.add_roles(role)
					print("done")
				else:
					print("member not found")
			else:
				print("role not found")
		else:
			print("something went wrong")
@client.event
async def on_raw_reaction_remove(payload):
	guild_id = payload.guild_id
	guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
	role = discord.utils.get(guild.roles, name=str("Muted"))
	if role != None:
		if guild.get_member(payload.user_id) != None:
			await guild.get_member(payload.user_id).remove_roles(role)
			print("done")
		else:
			print(repr(guild.get_member))
	else:
		print("role not found")




@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome", topic="welcome")
    await channel.send(f'{member.mention} has joined')

@client.event
async def on_member_remove(member):
    
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    await channel.send(f'{member.mention} has left')

########## COMAMNDS


#reactionroles
#setup
@client.command()
async def reactionrolesetup(ctx):
	await ctx.send(
		"""Documentation on reaction roles in r33nterbot. Step 1 is you need the message id of the message that you to be the react role message. Type .messid [id]
		 . Next the emoji name and the name of the role you want to assign MUST be the same. Then get the bot to react to the message of choice by doing  .react [emoji] [id] 
		 Once the bot has reacted to the message of choice with the correct emoji, reaction roles is ready for use!""")

#messageid
@client.command()
async def messid(ctx, test):
	client.guild_reactions[ctx.guild] = test
	for key, value in client.guild_reactions.items():
		if value == test:

			the_key = key
	await ctx.send(f'{test} is your id for your reaction role message for {the_key}')
#check messageid for reaction roles
@client.command()
async def messidcheck(ctx):
	await ctx.send(f'{client.guild_reactions.get(ctx.guild)} is the message id for reaction roles')
#react to message
@client.command()
async def react(ctx, emoji, id: discord.Message):
	message = id
	await message.add_reaction(emoji)
	await ctx.send(f"Reacted {emoji} to message")
#unreact
@client.command()
async def unreact(ctx, emoji, id:discord.Message):
	message=id
	await message.remove_reaction(emoji)
	await ctx.send(f'Unreacted {emoji} to message')
#games
#coinflip
@client.command()

async def coinflip(ctx):
	rand = random.randint(0,1)
	if rand == 1:

		outcome = 'Heads'
	else: 
		outcome = 'Tails'
	embed2 = discord.Embed(title="Coin Flip", description=outcome, color=discord.Color.blue())
	await ctx.send(embed=embed2)
#roll
@client.command()
async def roll(ctx):
	roll=random.randint(1,6)
	rollembed = discord.Embed(title="Roll", description=(f"You rolled a {roll}!"), color=discord.Color.blue())
	await ctx.send(embed=rollembed)
#utilities
#search
@commands.cooldown(1, 1800, BucketType.user)
@client.command()
async def search(ctx, *,search):
	api_key = ""
	ressource = build("customsearch", 'v1', developerKey=api_key).cse()
	result = ressource.list(q=search, cx='013543553084045992112:iq8yph27jiz').execute()
	for item in result['items']:
		await ctx.send(item['title'] and item['link'])
	result['items']
#define
@client.command()
async def define(ctx, *, definition):
	#api_key = ""
	#ressource = build("customsearch", 'v1', developerKey=api_key).cse()
	#result = ressource.list(q=definition, cx="013543553084045992112:nbzqsqza4p0").execute()
	#for item in result['items']:
		#await ctx.send(item['title'] and item['link'])
	await ctx.send("commmand broken")


#ping
@client.command()
async def ping(ctx):
	ping  = round(client.latency * 1000)
	embed3 = discord.Embed(title="Pong!", description=ping, color=discord.Color.blue())
	await ctx.send(embed=embed3)

#randdomnumber
@client.command()
async def randomnum(ctx, i: int, e: int):
	rand = random.randint(i,e)
	randomnume = discord.Embed(
		title = f"Number between {i} and {e}",
		description=rand  ,
		color=discord.Color.blue()
	)
	await ctx.send(embed=randomnume)
#dm
@commands.cooldown(1, 5, BucketType.user)
@client.command()
@commands.has_permissions(manage_messages=True)
async def dm(ctx, user: discord.User, message):
	await user.send(message)
	await ctx.send(f"Sent {message} to {user}")
	
#say
@commands.cooldown(1, 600, BucketType.user)
@client.command()
async def say(ctx, title, description):
	saye = discord.Embed(
		title=title,
		description=description,
		color=discord.Color.blue())
	await ctx.send(embed=saye)
	

##FUN COMMANDS
#pinguser
@client.command()
@commands.has_permissions(manage_roles=True)
async def pinguser(ctx, member: discord.Member, i: int):
	e = 0
	if i > 10000000000:
		await ctx.send("WOAH WOAH WOAH @admin WILL BE DEALING WITH YOU")

	
	else:
		while i > e:
			await ctx.send(member.mention)
			e=e+1
	if not member:
		await ctx.send("Please specify a member")
	
	#dmspam
@client.command()
@commands.has_permissions(manage_roles=True)
@commands.cooldown(1, 10, BucketType.default)
async def dmspam(ctx, member: discord.Member, i:int, message="spam"):
	e=0
	if i > 10:
		await ctx.send("WOAH WOAH WOAH @admin WILL HAVE A WORD WITH YOU")
	else:
		while i > e:
			await member.send(message)
			e = e+1
#fakeddos
@client.command()
async def hackaccount(ctx, member: discord.Member,**kwargs):
	await asyncio.sleep(2)
	await ctx.send("```bash ----------------ENTERING SECURE KONSOLE---------------```")
	await asyncio.sleep(1)
	randomnum2 = random.randint(1000000,9999999999999)
	await ctx.send(f"```---------------- SUCCESSFULLY ENTERED SECURE KONSOLE @{randomnum2}------------```" )
	await asyncio.sleep(2)
	await ctx.send(f"```---------------HACK ON {member.mention} COMMENCING...--------------```")
	await asyncio.sleep(2)
	await ctx.send(f"```----------------WARNING ALL DATA ON {member}'S ACCOUNTS WILL BE COMPROMISED------------```")
	i=0
	await asyncio.sleep(3)
	await ctx.send(f"```--------------------HACKING INTO THE MAINFRAME--------------------------```")
	await asyncio.sleep(4)
	while 6>i:
		await ctx.send(f"```------------PROCCESSING STEP {i} of 5---------------```")
		await asyncio.sleep(2)
		i+=1
	randum = random.randint(100000,999999)
	await ctx.send(f"```---------------SECURE ATTACK HOSTED ON PORT {randum}-----------```")
	await asyncio.sleep(5)
	await ctx.send(f"```-------------{member.mention} IS CURRENTLY BEING HACKED ON PORT {randum}-----------```")
	e=0
	while e<6:
		await asyncio.sleep(2)
		await ctx.send(f"```--------------{member}'S INFORMATION IS BEING ACQUIRED STEP {e} OF 5...---------------```")
		e+=1
	await asyncio.sleep(5)
	chars = """abcdefghijklmaopqrstuvwxyz"""
    
	password = f"rs.info.{member}"
	await ctx.send(f"```---------------- INFORMATION LEAKED ON {password}.onion CHECK OUT NOW--------------```")
	await asyncio.sleep(2)
	await ctx.send(f"```-----------------{member}'S PASSWORDS ARE CURRENTLY BEING OBTAINED VIA BRUTEFORCE.ATTACK; .... ------------```")
	await asyncio.sleep(2)
	message = await ctx.send(f'```------------------ BRUTEFORCING PASSWORDS 1%...------------------```')
	j=0
	
	while j<100:
		num = round(random.uniform(0.5,1),3)
		await message.edit(content=(f'```------------------ BRUTEFORCING PASSWORDS {j}%...------------------```'))
		await asyncio.sleep(num)
		j+=4.5
	await message.edit(content=(f'```-------------BRUTFORCING PASSWORDS COMPLETE-----------```'))
	r = round(random.uniform(10,20),3)
	await ctx.send(f'```----------------- PASSWORDS SUCCESSFULLY OBTAINED IN {r}S, CHECK rs.passwords.{member}.onion FOR PASSWORDS-------------```')


##ADMIN COMMANDS
#donate
@client.command()
async def donate(ctx):
	await ctx.send("https://www.paypal.me/r33nter")

#ban
@client.command()
@commands.has_permissions(ban_members=True, kick_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	
	await ctx.send(f'{member.mention} has been banned for {reason}')
	await member.ban(reason=reason)
#unban
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx,*, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user
		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
			return
#clear
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount:int = 100):
	await ctx.channel.purge(limit=amount,check=None, before=None, after=None, around=None, oldest_first=False, bulk=True)
#kick
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
	if not member:
		await ctx.send("Please specify a member")
	await ctx.send(f'{member.mention} has been kicked for {reason}')
	await member.kick(reason=reason)
#mute
@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, t: int):

	
	muted = discord.utils.get(ctx.guild.roles, name="Muted")
	await member.edit()
	await member.add_roles(muted)
	if t == 1:
		await ctx.send(f"{member.mention} has been muted for 1 minute!")
	else:
		await ctx.send(f'{member.mention} has been muted for {t} minutes!')
	await asyncio.sleep(t*60)
	await member.remove_roles(muted)
	await ctx.send(f"{member.mention} was muted for {t} minute(s) and is now unmuted!")
#unmute
@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
	muted = discord.utils.get(ctx.guild.roles, name ="Muted")
	await member.remove_roles(muted)
	await ctx.send(f"Unmuted {member.mention}")

#userinfo
@client.command()
async def userinfo(ctx, member: discord.Member):
	await ctx.send(f'{member.mention} was created at {member.created_at} and joined the server at {member.joined_at}')
#disable command	
@client.command()
async def disable(ctx, command):
	client.get_command(command)
	command=False()
	
#warn
@client.command()
@commands.has_permissions(manage_roles=True)
async def warn(ctx, member: discord.Member, *,reason=None):
	await ctx.send(f"{member.mention} has been warned for {reason} ")

############# HELP
#general
@client.command()
async def help(ctx):
	embed1 = discord.Embed(
	title="Categories",
	description=".helpgames \n.helputilities \n.helpfun  \n.helpadmin \n.helpreactions  ",
	color=discord.Color.blue()
	)
	embed1.set_footer(text="")                         
	await ctx.send(embed=embed1)
#fun
@client.command()
async def helpfun(ctx):
	helpfune = discord.Embed(
	title="Fun",
	description=".pinguser [user] [number of pings] (DO NOT ABUSE SPAM PINGING IS AGAINST THE RULES) \n.dmspam [user] [amount] [message]\n.hackaccount [user] (doesnt actually hack account its just a joke!)",
	color=discord.Color.blue()
	)
	await ctx.send(embed=helpfune)
#games
@client.command()
async def helpgames(ctx):
	helpgamese = discord.Embed(
	title="Games",
	description=".coinflip		flips a coin \n.roll		rolls a dice",
	color=discord.Color.blue()
	)
	await ctx.send(embed=helpgamese)
#utilities
@client.command()
async def helputilities(ctx):
	helputilitiese = discord.Embed(
	title="Utilities",
	description=""".ping check your latency \n.randomnum [num][num]\n.donate	donation link to r33nterbots dev team!\n.dm [user][message]
	.say [message]\n.search [search]\n.define [word]
	""", 
	color = discord.Color.blue()
	)
	await ctx.send(embed=helputilitiese)
#admin
@client.command()
async def helpadmin(ctx):
	helpadmine = discord.Embed(
		title = "Admin Help",
		description =""" .mute [user] [minutes]\n .ban [user] [reason]\n.kick [user] [reason]\n .unban [user(string)] .clear [amount]\n.userinfo [member]
		.unmute [member] .disable\n.warn [member] [reason]""",
		color = discord.Color.blue()
	)
	await ctx.send(embed=helpadmine)
#reactions

@client.command()
async def helpreactions(ctx):
	helpreactione = discord.Embed(
		title = "Reactions Help",
		description=".reactionrolesetup \n.messid [messageid]\n.checkmessid\n.react [emoji] [messageid]\n.unreact [emoji] [messageid]",
		color = discord.Color.blue()
	)
	await ctx.send(embed=helpreactione)

client.run(token)
