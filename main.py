from random import choice
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Member
import Admin_Funcs
import Fun_Funcs
import Utility_Funcs
import os, math
import discord

TOKEN = os.environ['TOKEN']
bot = Bot(command_prefix=["z.", "Z."])
bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you..."))
	print('{0.user}, ready to conquer the world.'.format(bot))

#-----------------------------#  Administrator Commands
@bot.command()
async def echo(ctx, *, message=None):
    """
    Echos a message. If no message, it will alert the user.
    Args:
        ctx: discord context : dictionary
        message: message to display : str
    Returns:
        None
    """
    await ctx.message.delete()
    await ctx.send(Admin_Funcs.send_echo(message))

# @bot.command()
# async def dailychallenge(ctx):
# 	if ctx.message.author.guild_permissions.administrator:
# 		await ctx.send(Admin_Funcs.DailyChallenge())
# 		Admin_Funcs.increaseDay()
# 	else:
# 		await ctx.send(f"Permission denied: with little power comes... no responsibility?", reference=ctx.message)

@bot.command()
async def rules(ctx, *, args):
	if ctx.message.author.guild_permissions.administrator:
		text = args.replace("!rules", "").split("\n")
		
		embed = discord.Embed(title=text[0], description="", timestamp=ctx.message.created_at)
		for index, content in enumerate(text, 1):
			if int(index) >= 2:
				embed.add_field(name='Rule #'+str(index-1) , value=content)
		await ctx.message.delete()
		await ctx.send(embed=embed)
	else:
		await ctx.send(f"Permission denied: with little power comes... no responsibility?", reference=ctx.message)

@bot.command(aliases=["purge", "clr", "clean"])
@commands.has_role("Staff")
@commands.cooldown(1, 500, commands.BucketType.user)
async def clear(ctx, amount: str):
	audit = bot.get_channel(953545221260595280)
	if int(amount) <= 50:
		#set to 50 max to prevent wrongdoings.
		await ctx.channel.purge(limit=int(amount)), await audit.send(f"{ctx.author} deleted {amount} messages in {ctx.channel}")
	else:
		embed = discord.Embed(title="ERROR", description="")
		embed.add_field(name="Reason:", value="Invalid input- please choose a number 1-50")
		await ctx.channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		msg = "**You're still on cooldown!! next avaliable in {:.2f}s".format(error.retry_after)
		alert = bot.get_channel(953545221260595280)
		await alert.send(f"{ctx.author.mention}\n {msg}")


@bot.command()
async def times(ctx):
	embed = discord.Embed(title=f"**TIMES**", description="")
	embed.add_field(name="Staff", value=Utility_Funcs.get_times())
	await ctx.send(embed=embed)

#-----------------------------#  User "Fun" Commands
@bot.command()
async def hello(ctx):
	await ctx.send(Fun_Funcs.hello(), reference=ctx.message)

@bot.command()
async def taunt(ctx):
	await ctx.send(Fun_Funcs.taunt(), reference=ctx.message)
	
@bot.command()
async def catfact(ctx):
	await ctx.send(Fun_Funcs.catfact(), reference=ctx.message)

@bot.command()
async def dogfact(ctx):
	await ctx.send(Fun_Funcs.dogfact(), reference=ctx.message)

@bot.command()
async def pugfact(ctx):
	await ctx.send(Fun_Funcs.pugFact(), reference=ctx.message)

@bot.command()
async def catpic(ctx):
	await ctx.send(file=discord.File(fp=Fun_Funcs.catpic(), filename="cat.png"), reference=ctx.message)

@bot.command()
async def joke(ctx):
	await ctx.send(Fun_Funcs.joke(), reference=ctx.message)
	
@bot.command()
async def quote(ctx):
	await ctx.send(Fun_Funcs.quote(), reference=ctx.message)

@bot.command(aliases=["8ball"])
async def eightball(ctx):
	await ctx.send('???? - ' + Fun_Funcs.eightball(), reference=ctx.message)
	
@bot.command()
async def fakeperson(ctx):
	await ctx.send(Fun_Funcs.fakePerson(), reference=ctx.message)

@bot.command()
async def rolldice(ctx):
	await ctx.send(f"**{ctx.message.author.name}** rolled a **{Fun_Funcs.dice()}**", reference=ctx.message)

@bot.command()
async def google(ctx, *, args):
	await ctx.send(f"Here, allow me to google that one for you:\nhttps://letmegooglethat.com/?q={args.replace(' ', '+')}",reference=ctx.message)

@bot.command()
async def pokedex(ctx, *, pokemon):
    await ctx.send(embed=Fun_Funcs.pokedex(pokemon))
    
@bot.command()
async def dogpic(ctx, *, breed=None):
    await ctx.send(embed=Fun_Funcs.dogpic(breed))

"""   

				Utility Commands

"""
@bot.command()
async def runcode(ctx):
	await ctx.send(Utility_Funcs.runcode(), reference=ctx.message)
	
@bot.command()
async def codeblock(ctx):
	await ctx.send(Utility_Funcs.codeblock(), reference=ctx.message)

@bot.command()
async def embed(ctx, *, args):
    embed = Utility_Funcs.make_embed(ctx.message.content, 
								 ctx.message.author,
                                 ctx.message.created_at,
                                 ctx.message.author.avatar_url)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command()
async def zeus(ctx, *, args):
	res = Utility_Funcs.Run_zeus(url=args)

	if res[1] == "**ONLINE**":
		COLOR = discord.Color.green()
	else:
		COLOR = discord.Color.red()

	embed = discord.Embed(title="ZeusTheInvestigator", description="", timestamp=ctx.message.created_at, color=COLOR)
	embed.add_field(name=f"Checked link: *{res[0]}*", value=f"STATUS: {res[1]}")
	embed.set_footer(text="Credits to: @777advait#6334")

	await ctx.send(embed=embed)

@bot.listen('on_message')
async def preview(message):
	text = message.content
	l = text.replace(", ", " ").split(" ")
	key = "https://discord.com/channels/"
	for item in l:
		if key in item:
			try:
				lilink = l[l.index(item)]
				response = "-**---** **Content** **in** **the** **link** **above** **---**- \n\n"
				link = lilink.replace("https://discord.com/channels/", "").split("/")
				sourceServer = bot.get_guild(int(link[0]))
				sourceChannel = sourceServer.get_channel(int(link[1]))
				sourceMessage = await sourceChannel.fetch_message(int(link[2]))

				if len(sourceMessage.content) <= 1000:
					embed = discord.Embed(title=response, description="", timestamp=sourceMessage.created_at)
					embed.add_field(name=f"Length: {len(sourceMessage.content)}", value=sourceMessage.content)
					embed.set_footer(text=sourceMessage.author, icon_url=sourceMessage.author.avatar_url)
					await message.channel.send(embed=embed)

				if len(sourceMessage.content) > 1000:
					contents = sourceMessage.content
					con2 = []
					splitstr = math.ceil(len(contents)/1000)
					embed1 = discord.Embed(title=response, description="", timestamp=sourceMessage.created_at)
					while contents:
						con2.append(contents[:900])
						contents = contents[900:]
					for feilds in range(0, splitstr):
						embed1.add_field(name="**---CUT---HERE---**", value=f"```py\n{con2[feilds]}\n```", inline=False)
					embed1.set_footer(text=sourceMessage.author, icon_url=sourceMessage.author.avatar_url)
					await message.channel.send(embed=embed1)

			except:

				await message.channel.send(f"         -**Cannot** **preview**-\n-"
										   f"**Make sure message is in this server,"
										   f" and not a text file or image**-")

@bot.command()
async def suggest(ctx, *, args):
	await ctx.message.delete()
	embed = discord.Embed(description=args, timestamp=ctx.message.created_at)
	embed.set_author(name=f"Suggestion by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
	msg = await ctx.send(embed=embed)
	await msg.add_reaction("????")	
	await msg.add_reaction("????")

@bot.command()
async def poll(ctx):
	await ctx.message.delete()
	reactions = {
		'1': '1??????',
		'2': '2??????',
		'3': '3??????',
		'4': '4??????',
		'5': '5??????',
		'6': '6??????',
		'7': '7??????',
		"8": '8??????',
		"9": '9??????',
		"10": '????'
	}
	text = ctx.message.content.replace("!poll", "").split("\n")

	if len(text) < 4:
		await ctx.send("Can't create a poll! Please provide more options.")
	elif len(text) > 12:
		await ctx.send("Can't create a poll! Please provide only 10 options.")
	else:
		embed = discord.Embed(
			description=f"**{text[1]}**\n\n"+"\n\n".join(f"{reactions[str(idx)]}: {opt}" for idx, opt in enumerate(text[2:], 1)),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name=f"Poll by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

		msg = await ctx.send(embed=embed)
		
		for idx in range(1, len(text[2:]) + 1):
			await msg.add_reaction(reactions[str(idx)]), await ctx.message.delete()

@bot.command(aliases=["av"])
async def avatar(
        ctx,
        member: discord.Member = None):
    embed = Utility_Funcs.get_avatar(ctx, member)
    await ctx.send(embed=embed, reference=ctx.message)


@bot.command(aliases=["whois"])
async def userinfo(ctx, member: Member = None):
	if not member:
		member = ctx.message.author

	roles = [role for role in member.roles]

	embed = discord.Embed(
		colour=discord.Colour.orange(),
		timestamp=ctx.message.created_at,
		title=str(member.display_name)
	)
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f"Requested by {ctx.message.author}")

	embed.add_field(name="Username:", value=member.name, inline=False)
	embed.add_field(name="ID:", value=member.id, inline=False)

	embed.add_field(name="Account Created On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
	embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

	try:
		embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
		embed.add_field(name="Highest Role:", value=member.top_role.mention)
		
		await ctx.send(embed=embed)

	except:
		await ctx.send(embed=discord.Embed(title="Traceback (most recent call last): \"~/ur_brain\"", colour=discord.Colour.red(), description="NoRoleError: Please get atleast one role for yourself"))

@bot.command(aliases=["pip", "pypi"])
async def pipsearch(ctx):
	package = ctx.message.content.split(" ")[-1]
	
	if not package:
		await ctx.send(embed=discord.Embed(title="Traceback (most recent call): \"~/ur_brain\"", description="Invalid pacakge name!", colour=discord.Colour.red()))
	else:
		data = Utility_Funcs.getPypiInfo(package)
		
		embed=discord.Embed(
			title=f"Searched {package}",
			description=f"[Project URL]({data['info']['package_url']})",
			colour=discord.Colour.green(),
			timestamp=ctx.message.created_at,
		)

		embed.add_field(name=f"{data['info']['name']}-{data['info']['version']}", value=f"{data['info']['summary']}")
		embed.set_footer(text=f"Requested by {ctx.message.author}")
		await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
	await ctx.send(
		embed=discord.Embed(
			title="Zorathian Army Report",
			description=f"Zorak's current ping is **{round(bot.latency * 1000)}ms**",
			timestamp=ctx.message.created_at
		)
	)

@bot.command(aliases=["git"])
async def github(ctx, *, endpoint):
	info = Utility_Funcs.getgitinfo(endpoint)

	owner = info["owner"]["login"]
	language = info["language"]
	stars = info["stargazers_count"]
	forks = info["forks"]
	issues = info["open_issues"]
	license = info["license"]["name"] if info["license"] is not None else "None"
	thumbnail = info["owner"]["avatar_url"]
	
	contrib_info = Utility_Funcs.getgitinfo(endpoint+"/contributors")
	contributors = [contribs["login"] for contribs in contrib_info]

	embed = discord.Embed(
		title=info["name"],
		description=f"[Repository Link]({info['html_url']})",
		colour=discord.Colour.gold(),
		timestamp=ctx.message.created_at
	)

	embed.add_field(
		name="Owner",
		value=owner
	)
	embed.add_field(
		name="Language",
		value=language
	)
	embed.add_field(
		name="Stars",
		value=stars
	)
	embed.add_field(
		name="Forks",
		value=forks
	)
	embed.add_field(
		name="License",
		value=license
	)
	embed.add_field(
		name="Open Issues",
		value=issues
	)
	embed.add_field(
		name="Contributors",
		value="\n".join(contributors)
	)
	embed.set_thumbnail(url=thumbnail)
	embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)

	await ctx.send(embed=embed, reference=ctx.message)

@github.error
async def no_endpoint(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send(
			embed=discord.Embed(
				title="No endpoint",
				description="Please add an endpoint!\n`Syntax: !github|!git <username/repo_name>`",
				timestamp=ctx.message.created_at,
				colour=discord.Colour.red()
			),
			reference=ctx.message
		)


@bot.command(aliases=["tex"])
async def latex(ctx, *, expr):
	res = Utility_Funcs.render_latex(expr, ctx)

	await ctx.message.delete()
	await ctx.send(embed=res[0], file=res[1])

@bot.command()
async def help(ctx):
	embed = discord.Embed(title="User-Commands", description=Utility_Funcs.help_msg(), timestamp=ctx.message.created_at)
	await ctx.send(embed=embed, reference=ctx.message)


"""   

				Error Handling

"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("User you requested cannot be found.",
                       reference=ctx.message)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Zorak has no such command!", reference=ctx.message)
    await ctx.message.delete()


if __name__ == "__main__":
	bot.run(TOKEN)

