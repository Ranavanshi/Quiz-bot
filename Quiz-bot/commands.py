from pyrogram import filters
import json
import os

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

def quiz_command(client, message):
    # Implementation of /quiz command
    pass

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


def broadcast_command(client, message):
    # Implementation of /broadcast command
    pass
