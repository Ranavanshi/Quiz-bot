from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient
import os
import random

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
MONGODB_URI = 'YOUR_MONGODB_URI'

client = MongoClient(MONGODB_URI)
db = client.get_default_database()
questions_collection = db.questions
scores_collection = db.scores

# Example quiz questions (replace with your questions)
questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Which planet is known as the Red Planet?", "answer": "Mars"},
    {"question": "What is the largest mammal?", "answer": "Blue Whale"}
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Quiz Bot! Type /quiz to start the quiz.')

def quiz(update: Update, context: CallbackContext) -> None:
    # Get a random question
    question = random.choice(questions)
    context.user_data['current_question'] = question

    update.message.reply_text(question['question'])

def answer(update: Update, context: CallbackContext) -> None:
    user_answer = update.message.text.lower()
    question = context.user_data.get('current_question')

    if question:
        correct_answer = question['answer'].lower()

        if user_answer == correct_answer:
            update.message.reply_text('Correct! Well done.')
            # Increment user score
            user_id = update.message.from_user.id
            scores_collection.update_one({'user_id': user_id}, {'$inc': {'score': 1}}, upsert=True)
        else:
            update.message.reply_text(f'Incorrect. The correct answer is {correct_answer}.')

        # Remove the current question from user_data
        del context.user_data['current_question']
    else:
        update.message.reply_text('Please start the quiz with /quiz.')

def main() -> None:
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("quiz", quiz))
    
    # Register message handler for answers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
