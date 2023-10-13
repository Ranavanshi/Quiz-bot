from pyrogram import filters
from pyrogram.types import Message
import json
import os 
import random

# Define command functions
# quiz_commands.py

def start_command(client, message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Customize the welcome message
    welcome_message = f"Welcome, {username}! 🎉\n\n"
    welcome_message += "This is the Quiz Bot. Use /quiz to start a quiz.\n"
    welcome_message += "For more information, use /help."

    # Send the welcome message
    message.reply_text(welcome_message)

# quiz_commands.py

def quiz_command(client, message):
    user_id = message.from_user.id

    # Check if the user has already created a quiz
    if has_created_quiz(user_id):
        # User has created a quiz, show the available quizzes
        show_available_quizzes(client, user_id)
    else:
        # User has not created a quiz, guide them to the create command
        message.reply_text("You haven't created a quiz yet. Use /create to create a new quiz.")

def has_created_quiz(user_id):
    # Check if the user has already created a quiz
    # Replace this logic with your own implementation (e.g., database check)
    return user_id in get_created_quizzes()

def get_created_quizzes():
    # Dummy function to simulate fetching created quizzes from a database
    # Replace this with your own logic to retrieve created quizzes
    return ["Quiz1", "Quiz2", "Quiz3"]

def show_available_quizzes(client, user_id):
    # Fetch the list of quizzes created by the user
    created_quizzes = get_created_quizzes()

    # Show the available quizzes to the user
    quiz_message = "Available Quizzes:\n\n"
    for index, quiz in enumerate(created_quizzes, start=1):
        quiz_message += f"{index}. {quiz}\n"

    quiz_message += "\nTo start a quiz, use /start_quiz <quiz_number>."

    # Send the message to the user
    client.send_message(user_id, quiz_message)

@Client.on_message(filters.command("start_quiz"))
def start_quiz_command(

# quiz_commands.py

def create_question_command(client, message):
    # Extract the question, options, and correct answer from the message
    try:
        _, *question_parts = message.text.split(" ", 3)
        question, option1, option2, correct_answer = map(str.strip, question_parts)
    except ValueError:
        message.reply_text("Invalid format. Please provide the question, two options, and the correct answer.")
        return

    # Create a dictionary for the new question
    new_question = {
        "question": question,
        "options": [option1, option2],
        "correct_answer": correct_answer,
    }

    # Load existing questions or create an empty list
    questions = load_existing_questions()

    # Add the new question to the list
    questions.append(new_question)

    # Save the updated questions to the JSON file
    save_questions(questions)

    message.reply_text("New question added successfully.")

def load_existing_questions():
    # Load existing questions from the JSON file
    file_path = 'quiz_data.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            quiz_data = json.load(file)
        return quiz_data.get('questions', [])
    else:
        return []

def save_questions(questions):
    # Save the updated questions to the JSON file
    file_path = 'quiz_data.json'

    with open(file_path, 'w') as file:
        json.dump({"questions": questions}, file,



def results_command(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if the user is the owner of the bot or a group admin
    if not is_allowed_user(client, user_id, chat_id):
        message.reply_text("You are not authorized to use this command.")
        return

    # Load scores from the database
    scores = load_scores(chat_id)

    # Check if there are scores available
    if not scores:
        message.reply_text("No quiz scores available yet.")
        return

    # Format and send the results
    results_message = "Quiz Results:\n\n"
    for user, score in scores.items():
        results_message += f"{user}: {score} points\n"

    message.reply_text(results_message)

def is_allowed_user(client, user_id, chat_id):
    # Check if the user is the owner of the bot or a group admin
    return is_owner(client, user_id) or is_group_admin(client, user_id, chat_id)

def is_owner(client, user_id):
    # Replace with your logic to check if the user is the bot owner
    return user_id == OWNER_ID

def is_group_admin(client, user_id, chat_id):
    # Check if the user is an admin in the group
    chat_member = client.get_chat_member(chat_id, user_id)
    return chat_member and chat_member.status == "administrator"

def load_scores(chat_id):
    # Load scores from the database or create an empty dictionary
    # In a real-world scenario, you would fetch this information from your database
    # For simplicity, we use a dictionary as an example
    scores = {
        "User1": 3,
        "User2": 2,
        "User3": 1,
    }

    return scores


# quiz_commands.py

# Replace OWNER_ID with the actual owner's user ID
OWNER_ID = 1995154708

# A list to store chat IDs of groups where the bot is present
registered_groups = []

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
def broadcast_command(client, message):
    # Check if the owner is replying to a message
    if message.reply_to_message:
        reply_to_message(client, message.reply_to_message)
    else:
        message.reply_text("Reply to a message to broadcast it.")

def reply_to_message(client, replied_message: Message):
    # Forward the replied message to all registered groups
    for group_id in registered_groups:
        client.forward_messages(chat_id=group_id, from_chat_id=replied_message.chat.id, message_ids=replied_message.message_id)

    # Inform the owner about the successful broadcast
    replied_message.reply_text("Message forwarded to all groups.")

@Client.on_message(filters.command("register") & filters.user(OWNER_ID))
def register_group(client, message):
    # Register a group for broadcasting
    if message.chat.id not in registered_groups:
        registered_groups.append(message.chat.id)
        message.reply_text("Group registered for broadcasting.")
    else:
        message.reply_text("Group is already registered for broadcasting.")

