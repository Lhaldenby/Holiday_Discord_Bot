import discord
import asyncio
import datetime
import requests
import gspread
import json
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from oauth2client.service_account import ServiceAccountCredentials
from wcwidth import wcswidth

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

TOKEN = config["DISCORD_BOT_TOKEN"]
EXCHANGE_API_URL = config["EXCHANGE_API_URL"]
CHANNEL_ID = config["CHANNEL_ID"]
HEADERS = {
    "X-RapidAPI-Key": config["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": config["RAPIDAPI_HOST"]
}

# Google Sheets authentication
SCOPE = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
CREDS_FILE = config["GOOGLE_CREDS_FILE"]
SPREADSHEET_NAME = config["SPREADSHEET_NAME"]

def get_google_sheet_data():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open(SPREADSHEET_NAME).get_worksheet(3)  # Select the fourth sheet
        return sheet
    except Exception as e:
        print("Error fetching Google Sheet data:", e)
        return None

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def get_yen():
    try:
        querystring = {"to": "JPY", "from": "GBP", "q": "1.0"}
        response = requests.get(EXCHANGE_API_URL, headers=HEADERS, params=querystring)
        yen_rate = float(response.json())
        if yen_rate:
            return (f"Current exchange rate: 1 GBP = {yen_rate:.2f} JPY")
        else:
            return ("Could not fetch exchange rate.")
    except Exception as e:
        return ("Error fetching exchange rate {e}.")

last_sent_date = None
async def send_countdown():
    global last_sent_date
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found!")
        return

    while not bot.is_closed():
        now = datetime.datetime.now()
        target_time = now.replace(hour=7, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += datetime.timedelta(days=1)
        wait_time = (target_time - now).total_seconds()

        await asyncio.sleep(wait_time)
        today = datetime.date.today()
        if last_sent_date != today:
            last_sent_date = today
            target_date = datetime.date(2026, 4, 3)
            countdown_days = (target_date - today).days
            await channel.send(f"<@&979099587560218644> Countdown to Japan 2026: {countdown_days} days remaining!\n{get_yen()}")
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(send_countdown())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.command(name="yen", help="Get the current exchange rate for Japanese Yen against GBP.")
@cooldown(1, 60, BucketType.guild)
async def yen(ctx):
    await ctx.send(get_yen())

def pad_display(text, width):
    display_width = wcswidth(text)
    return text + ' ' * (width - display_width)

@bot.command(name="plan", help="Retrieve and display a table from a Google Sheet.")
@cooldown(1, 60, BucketType.user)
async def plan(ctx, name: str = None):
    sheet = get_google_sheet_data()
    people_data = {
        "lewis" : sheet.get('C:D'),
        "bew"   : sheet.get('E:F'),
        "michael"   : sheet.get('E:F'),
        "ruan"  : sheet.get('G:H'),
        "ryan"  : sheet.get('G:H'),
        "jack"  : sheet.get('I:J'),
        "sweasey"  : sheet.get('I:J'),
        "tom"   : sheet.get('K:L'),
        "thomas"   : sheet.get('K:L'),
        "ethan" : sheet.get('M:N'),
        "beth"  : sheet.get('O:P'),
        "adrian": sheet.get('Q:R'),
        "neb"   : sheet.get('S:T'),
        "nebula"   : sheet.get('S:T'),
    }
    if name:
        name_key = name.lower()
        if name_key in people_data:
            data = people_data[name_key]
            start_index = next(i for i, row in enumerate(data) if row == ['Location', 'Plan']) + 1
            end_index = next(i for i, row in enumerate(data[start_index:], start=start_index) if row == [])
            trip_data = data[start_index:end_index]

            normalised = [(row + [row[0]])[:2] for row in trip_data]
            col1_width = max(wcswidth(row[0]) for row in normalised)
            col2_width = max(wcswidth(row[1]) for row in normalised)

            lines = []
            border = '-' * (col1_width + col2_width + 5)
            lines.append(border)
            for col1, col2 in normalised:
                padded_col1 = pad_display(col1, col1_width)
                padded_col2 = pad_display(col2, col2_width)
                lines.append(f"| {padded_col1} | {padded_col2} |")
            lines.append(border)

            table = '\n'.join(lines)
            await ctx.send(f"```\n{table}\n```")
        else :
            name_options = ", ".join(people_data.keys())
            await ctx.send(f"Unknown name {name}, try: {name_options}")


@bot.command(name="day", help="See what everyone is doing on a certain day of the holiday")
@cooldown(1, 1, BucketType.user)
async def day(ctx, *, message: str):
    sheet = get_google_sheet_data()
    people_data = {
        "Lewis" : sheet.col_values(3),
        "Bew"   : sheet.col_values(5),
        "Ruan"  : sheet.col_values(7),
        "Jack"  : sheet.col_values(9),
        "Tom"   : sheet.col_values(11),
        "Ethan" : sheet.col_values(13),
        "Beth"  : sheet.col_values(15),
        "Adrian": sheet.col_values(17),
        "Neb"   : sheet.col_values(19)
    }
    try:
        location_map = {}
        day_int = int(message)
        dayRow = sheet.row_values(day_int+2)
        tableString = ""
        for person, locations in people_data.items():
            if (day_int +2)  < len(locations):
                location = locations[(day_int +2)]
                if location not in location_map:
                    location_map[location] = []
                location_map[location].append(person)
        if "" in location_map:
            location_map["Undecided"] = location_map.pop("")
        tableString += f"{dayRow[1]}\n"+"\n".join([f"{location}: {', '.join(people)}" for location, people in location_map.items()])
        await ctx.send(tableString)

    except ValueError as ex:
         await ctx.send(f"Can't understand that! Please give me an integer of the day you want to see.")

print('i am starting!')
bot.run(TOKEN)
