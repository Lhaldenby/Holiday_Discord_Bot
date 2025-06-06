Holiday Discord Bot
Overview
The Holiday Discord Bot is designed to assist users with travel-related queries and information through Discord. It provides exchange rates, user location tracking on specific days, and travel plans for individual users.

Commands
Get the Current Exchange Rate for GBP to JPY
Command:
!yen

Description:
Retrieves the latest exchange rate for GBP (British Pound) to JPY (Japanese Yen).

Get the Location of Users for a Particular Day on Holiday
Command:
!day <num>

Description:
Returns the date and a list of cities with each person next to it.

Example:
!day 15

Response: "June 15, 2024: Tokyo - JohnDoe, Osaka - JaneDoe"

Get the Plan and Details of Travel for a Particular User
Command:
!plan <name>

Description:
Displays the complete travel itinerary for a specified user, including flight details, hotel reservations, and activities.

Example:
!plan JaneDoe

Response: "JaneDoe's itinerary: Flight from London to Tokyo on 10th June, staying at Tokyo Grand Hotel, city tour on 11th June."

Installation & Setup
Clone the repository:
git clone https://github.com/your-repo/holiday-discord-bot.git
cd holiday-discord-bot

Install dependencies:
pip install -r requirements.txt

Set up the bot token in the .env file:
DISCORD_BOT_TOKEN=your-bot-token

Run the bot:
python bot.py

Contributing
Feel free to fork this repository and submit pull requests with improvements and bug fixes.

License
This project is licensed under the MIT License.