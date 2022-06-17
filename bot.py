from http import client
import os, discord, datetime, asyncio, string

from dotenv import load_dotenv
from discord.ext import tasks, commands
from dataclasses import dataclass
from translate import Translator
from time import sleep

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
bot = commands.Bot(command_prefix='!')

@dataclass
class Person:
	name: string
	going: bool
	timeoff: bool
	flight: bool
	lodging: bool

Group = [
	Person("Lewis Haldenby",True,False,False,False),
	Person("Michael Bew",True,False,False,False),
	Person("Adrian Larsson",False,False,False,False),
	Person("Nebula Thibaut",True,True,False,False),
	Person("Ryan Johnson",True,False,False,False),
	Person("Jack Sweasey",True,False,False,False),
	Person("Thomas Haldenby",True,False,False,False),
	Person("Brie Mathieson",True,False,False,False),
	Person("Ethan Hart-Coombes",True,False,False,False),
	Person("Beth Middleton",True,False,False,False),
	Person("Oli Ali",False,False,False,False)
]

#DONE
@bot.command(name='days', help='Responds with the days remaining until our trip')
@commands.cooldown(1,15,commands.BucketType.channel)
async def days_command(ctx):
	today = datetime.date.today()
	future = datetime.date(2023,10,14)
	diff = future - today
	if diff.days == 0:
		await ctx.send("Today is the day!!")
	elif diff.days < 0 and diff.days >= -14:
		await ctx.send("We are in Japan, get off discord!")
	elif diff.days < -14:
		await ctx.send("We miss Japan :(")
	else:
		await ctx.send(f'{diff.days} days until our UWU Japan Trip')	

#DONE
@bot.command(name='time', help='Responds with the local Japan time')
@commands.cooldown(1,15,commands.BucketType.channel)
async def time_command(ctx):
	today = datetime.datetime.today() + datetime.timedelta(hours=9)
	formatToday = today.strftime("%d/%m/%Y %H:%M:%S")
	await ctx.send(f'Japan datetime: {formatToday}')

#DONE
@bot.command(name='going_list', help='Whos going on the trip and booked what')
@commands.cooldown(1,30,commands.BucketType.channel)
async def going_command(ctx):
	for person in Group:
		going = "isn't going"
		timeoff = "don't have time off"
		flight = "don't have their flights booked"
		lodging = "don't have a place to stay"
		if person.timeoff:
			timeoff = "have time off"
		if person.flight:
			flight = "have their flights booked"
		if person.lodging:
			lodging = "have a place to stay"
		if person.going:
			going = "is going"
		await ctx.send(f'{person.name} {going}. They {timeoff}, {flight} and {lodging}.')

#DONE
@bot.command(name='going', help='Specific person details needs <name> as parameter')
@commands.cooldown(2,30,commands.BucketType.user)
async def going_command(ctx, name:str):
	for person in Group:
		if name.lower() in person.name.lower():
			going = "isn't going"
			timeoff = "don't have time off"
			flight = "don't have their flights booked"
			lodging = "don't have a place to stay"
			if person.timeoff:
				timeoff = "have time off"
			if person.flight:
				flight = "have their flights booked"
			if person.lodging:
				lodging = "have a place to stay"
			if person.going:
				going = "is going"
			await ctx.send(f'{person.name} {going}. They {timeoff}, {flight} and {lodging}.')

#@bot.command(name='translate', help='Translate your text to japanese')
#@commands.cooldown(3,30,commands.BucketType.user)
#async def trans_command(ctx, words:str):
#	translator = Translator(to_lang="ja")
#	print(f'{words}')
#	response = translator.translate(words) #words, src='en', dest='ja'
#	print(response)
#	await ctx.send(response.text)

#DONE
@bot.command(name='map', help='Get a map of our japan trip')
@commands.cooldown(1,30,commands.BucketType.channel)
async def map_command(ctx):
	embed=discord.Embed(title="Our Japan Map",colour = discord.Colour.orange(), timestamp=ctx.message.created_at, url="https://www.google.com/maps/d/edit?mid=1o_mgr_3GXP_xbLO9mb4QeON7vLoxOSU&ll=35.13006297296019%2C138.11491213319218&z=8")
	embed.set_image(url=(f"https://image.thum.io/get/width/1920/crop/1200/viewportWidth/2400/maxAge/1/noanimate/https://www.google.com/maps/d/edit?mid=1o_mgr_3GXP_xbLO9mb4QeON7vLoxOSU&ll=34.545604858227236%2C136.10263576493375&z=8"))
	await ctx.send(embed=embed)

#DONE
@tasks.loop(hours=1.0)
async def send_daily_message():
	now = datetime.datetime.today()
	mystart = now.replace(hour=8, minute=40, second=0)
	if now.hour == mystart.hour:
		channelToSend = await bot.fetch_channel(CHANNEL)
		today = datetime.date.today()
		future = datetime.date(2023,10,14)
		diff = future - today
		await channelToSend.send(f'Japan Countdown {diff.days} days remaining')

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CheckFailure):
		await ctx.send('You do not have the correct role for this command.')
	if isinstance(error, commands.CommandOnCooldown):
		msg = '**Still on cooldown**, please try again in {:.2f}s'.format(error.retry_after)
		await ctx.send(msg)

@bot.event
async def on_ready():
	print(f"Bot Started")
	send_daily_message.start()
	print(f"loop Started")

bot.run(TOKEN)