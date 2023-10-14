from pyrogram import Client, filters
from pymongo import MongoClient
import json
import logging
from filters import is_owner
from commands import start_command, quiz_command, create_question_command, results_command, broadcast_command
from quiz_google_search import google_search

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load questions from the JSON file
with open('quiz_data.json', 'r') as file:
    quiz_data = json.load(file)

questions = quiz_data.get('questions', [])

# Set up MongoDB connection
MONGODB_URI = 'YOUR_MONGODB_URI'
client = MongoClient(MONGODB_URI)
db = client.get_default_database()
scores_collection = db.scores

# Set up Pyrogram
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'

app = Client("quiz_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Register filters
app.add_filter(is_owner)


# Register commands
app.on_message(filters.command("start"))(start_command)
app.on_message(filters.command("quiz"))(quiz_command)
app.on_message(filters.command("create_question") & filters.create(is_owner))(create_question_command)
app.on_message(filters.command("results") & filters.create(is_owner))(results_command)
app.on_message(filters.command("broadcast") & filters.create(is_owner))(broadcast_command)

# Register Google search handler
app.on_message(filters.text & filters.regex(r'^/google'))(google_search)


# Run the bot
if __name__ == "__main__":
    app.run()
