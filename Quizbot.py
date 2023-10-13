# your_bot_script.py

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient
from config import Config

# Use Config class variables
TELEGRAM_BOT_TOKEN = Config.TELEGRAM_BOT_TOKEN
API_ID = Config.API_ID
API_HASH = Config.API_HASH
MONGODB_URI = Config.MONGODB_URI
LOGGING_GROUP_ID = Config.LOGGING_GROUP_ID

# ... rest of your code ...

# Load questions from the JSON file
with open('quiz_data.json', 'r') as file:
    quiz_data = json.load(file)

questions = quiz_data.get('questions', [])

client = MongoClient(MONGODB_URI)
db = client.get_default_database()
scores_collection = db.scores

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! This is the Quiz Bot. Type /quiz to start a quiz or /broadcast to send a broadcast message.')

def quiz(update: Update, context: CallbackContext) -> None:
    try:
        # Get a random quiz question
        quiz = random.choice(questions)
        
        if quiz:
            context.user_data['current_quiz'] = quiz
            update.message.reply_text(f"Question: {quiz['question']}\nOptions: {', '.join(quiz['options'])}")
        else:
            update.message.reply_text('No quiz available.')

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def answer(update: Update, context: CallbackContext) -> None:
    try:
        user_answer = update.message.text.lower()
        quiz = context.user_data.get('current_quiz')

        if quiz:
            correct_answer = quiz['answer'].lower()

            if user_answer == correct_answer:
                update.message.reply_text('Correct! Well done.')
                # Increment user score
                user_id = update.message.from_user.id
                scores_collection.update_one({'user_id': user_id}, {'$inc': {'score': 1}}, upsert=True)
            else:
                update.message.reply_text(f'Incorrect. The correct answer is {correct_answer}.')

            # Remove the current quiz from user_data
            del context.user_data['current_quiz']
        else:
            update.message.reply_text('Please start a quiz with /quiz.')

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def create_quiz(update: Update, context: CallbackContext) -> None:
    try:
        # Manually create a quiz (replace with your own logic)
        question = "What is the capital of Germany?"
        options = ["Berlin", "Paris", "Madrid", "Rome"]
        answer = "Berlin"

        quizzes_collection.insert_one({'question': question, 'options': options, 'answer': answer})
        update.message.reply_text('Quiz created successfully!')

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def broadcast(update: Update, context: CallbackContext) -> None:
    try:
        # Check if the sender is authorized to broadcast
        if update.message.from_user.id == YOUR_ADMIN_USER_ID:
            message_text = update.message.text

            # Broadcast the message to all users
            all_users = scores_collection.find()
            for user in all_users:
                context.bot.send_message(user['user_id'], message_text)

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def results(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        user_score = scores_collection.find_one({'user_id': user_id})
        score = user_score.get('score') if user_score else 0

        update.message.reply_text(f"Your current score: {score}")

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def description(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('This is a Telegram quiz bot. You can start a quiz with /quiz, create a quiz with /create_quiz, check your score with /results, and send a broadcast with /broadcast.')

def main() -> None:
    try:
        updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
        dp = updater.dispatcher

        # Register command handlers
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("quiz", quiz))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
        dp.add_handler(CommandHandler("create_quiz", create_quiz))
        dp.add_handler(CommandHandler("broadcast", broadcast))
        dp.add_handler(CommandHandler("results", results))
        dp.add_handler(CommandHandler("description", description))

        updater.start_polling()
        updater.idle()

    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")

if __name__ == '__main__':
    main()
