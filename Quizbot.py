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
quizzes_collection = db.quizzes
scores_collection = db.scores

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! This is the Quiz Bot. Type /quiz to start a quiz or /broadcast to send a broadcast message.')

def quiz(update: Update, context: CallbackContext) -> None:
    # Get a random quiz question
    quiz = quizzes_collection.find_one()
    
    if quiz:
        context.user_data['current_quiz'] = quiz
        update.message.reply_text(f"Question: {quiz['question']}\nOptions: {', '.join(quiz['options'])}")
    else:
        update.message.reply_text('No quiz available. Use /create_quiz to create one.')

def answer(update: Update, context: CallbackContext) -> None:
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

def create_quiz(update: Update, context: CallbackContext) -> None:
    # Manually create a quiz (replace with your own logic)
    question = "What is the capital of Germany?"
    options = ["Berlin", "Paris", "Madrid", "Rome"]
    answer = "Berlin"

    quizzes_collection.insert_one({'question': question, 'options': options, 'answer': answer})
    update.message.reply_text('Quiz created successfully!')

def broadcast(update: Update, context: CallbackContext) -> None:
    # Check if the sender is authorized to broadcast
    if update.message.from_user.id == YOUR_ADMIN_USER_ID:
        message_text = update.message.text

        # Broadcast the message to all users
        all_users = scores_collection.find()
        for user in all_users:
            context.bot.send_message(user['user_id'], message_text)

def main() -> None:
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("quiz", quiz))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    dp.add_handler(CommandHandler("create_quiz", create_quiz))
    dp.add_handler(CommandHandler("broadcast", broadcast))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
