from pyrogram import Client, filters
from pymongo import MongoClient
from googlesearch import search
from googletrans import Translator
from config.config import Config
from utils.logger import Logger
import json
import os
import random

# Initialize Pyrogram client
app = Client("quiz_bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

# Initialize MongoDB client
mongo_client = MongoClient(Config.MONGODB_URI)
db = mongo_client["quiz_bot"]

# Define collections
quiz_collection = db["quizzes"]
user_stats_collection = db["user_stats"]


# Dictionary to store active quizzes by user ID
active_quizzes = {}

# Command to start a private quiz
@app.on_message(filters.private & filters.command("startquiz"))
def start_private_quiz(_, message):
    user_id = message.from_user.id

    # Check if the user already has an active quiz
    if user_id in active_quizzes:
        app.send_message(user_id, "You already have an active quiz.")
        return

    # Generate a random quiz (replace this with your actual quiz generation logic)
    quiz_title = f"Quiz_{random.randint(1000, 9999)}"
    quiz_questions = ["Question 1", "Question 2", "Question 3"]  # Replace with your questions

    # Store the quiz information for this user
    active_quizzes[user_id] = {"title": quiz_title, "questions": quiz_questions, "current_question": 0}

    # Send the first question to the user
    send_question(user_id)

# Function to send a quiz question
def send_question(user_id):
    # Get the active quiz for this user
    active_quiz = active_quizzes.get(user_id)

    if active_quiz:
        # Send the current question
        current_question = active_quiz["current_question"]
        question_text = f"Question {current_question + 1}: {active_quiz['questions'][current_question]}"
        app.send_message(user_id, question_text)
    else:
        app.send_message(user_id, "No active quiz.")


# Dictionary to store active quizzes by group ID
active_quizzes = {}

# Command to start a group quiz (admins-only)
@app.on_message(filters.group & filters.command("startquiz") & filters.user("admins"))
def start_group_quiz(_, message):
    group_id = message.chat.id

    # Check if the group already has an active quiz
    if group_id in active_quizzes:
        app.send_message(group_id, "A quiz is already active in this group.")
        return

    # Generate a random quiz (replace this with your actual quiz generation logic)
    quiz_title = f"Quiz_{group_id}"
    quiz_questions = ["Question 1", "Question 2", "Question 3"]  # Replace with your questions

    # Store the quiz information for this group
    active_quizzes[group_id] = {"title": quiz_title, "questions": quiz_questions, "current_question": 0, "started_by": message.from_user.id}

    # Send the first question to the group
    send_question(group_id)

# Command to stop the group quiz (admins or user who started)
@app.on_message(filters.group & filters.command("stopquiz") & (filters.user("admins") | filters.user(lambda _, __, user: user.id == active_quizzes.get(_.chat.id, {}).get("started_by"))))
def stop_group_quiz(_, message):
    group_id = message.chat.id

    # Check if there is an active quiz in the group
    if group_id in active_quizzes:
        app.send_message(group_id, "The quiz has been stopped.")
        # Remove the quiz information for this group
        del active_quizzes[group_id]
    else:
        app.send_message(group_id, "No active quiz in this group.")

# Function to send a quiz question
def send_question(group_id):
    # Get the active quiz for this group
    active_quiz = active_quizzes.get(group_id)

    if active_quiz:
        # Send the current question
        current_question = active_quiz["current_question"]
        question_text = f"Question {current_question + 1}: {active_quiz['questions'][current_question]}"
        app.send_message(group_id, question_text)
    else:
        app.send_message(group_id, "No active quiz in this group.")


# Dictionary to store active quizzes by group ID
active_quizzes = {}

# Dictionary to store quizzes created by each user
user_quizzes = {}

# Command to start a group quiz (admins-only)
@app.on_message(filters.group & filters.command("startquiz") & filters.user("admins"))
def start_group_quiz(_, message):
    group_id = message.chat.id

    # Check if the group already has an active quiz
    if group_id in active_quizzes:
        app.send_message(group_id, "A quiz is already active in this group.")
        return

    # Generate a random quiz (replace this with your actual quiz generation logic)
    quiz_title = f"Quiz_{group_id}"
    quiz_questions = ["Question 1", "Question 2", "Question 3"]  # Replace with your questions

    # Store the quiz information for this group
    active_quizzes[group_id] = {"title": quiz_title, "questions": quiz_questions, "current_question": 0, "started_by": message.from_user.id}

    # Store the quiz created by this user
    user_id = message.from_user.id
    user_quizzes[user_id] = {"title": quiz_title, "questions": quiz_questions}

    # Send the first question to the group
    send_question(group_id)

# Command to view the quiz created by the user
@app.on_message(filters.private & filters.command("viewmyquiz"))
def view_user_quiz(_, message):
    user_id = message.from_user.id

    # Check if the user has created a quiz
    if user_id in user_quizzes:
        quiz_info = f"Your Quiz:\nTitle: {user_quizzes[user_id]['title']}\nQuestions: {len(user_quizzes[user_id]['questions'])}"
        app.send_message(user_id, quiz_info)
    else:
        app.send_message(user_id, "You haven't created a quiz yet.")

# Function to send a quiz question
def send_question(group_id):
    # Get the active quiz for this group
    active_quiz = active_quizzes.get(group_id)

    if active_quiz:
        # Send the current question
        current_question = active_quiz["current_question"]
        question_text = f"Question {current_question + 1}: {active_quiz['questions'][current_question]}"
        app.send_message(group_id, question_text)
    else:
        app.send_message(group_id, "No active quiz in this group.")



# Initialize MongoDB client
mongo_client = MongoClient(Config.MONGODB_URI)
db = mongo_client["quiz_bot"]

# Define collections
quiz_collection = db["quizzes"]
user_stats_collection = db["user_stats"]

# Logger group ID
logger_group_id = -1001971385258  # Replace with your logger group ID

# Dictionary to store active quizzes by group ID
active_quizzes = {}

# Dictionary to store quizzes created by each user
user_quizzes = {}

# Command to start a group quiz (admins-only)
@app.on_message(filters.group & filters.command("startquiz") & filters.user("admins"))
def start_group_quiz(_, message):
    group_id = message.chat.id

    # Check if the group already has an active quiz
    if group_id in active_quizzes:
        app.send_message(group_id, "A quiz is already active in this group.")
        return

    # Generate a random quiz (replace this with your actual quiz generation logic)
    quiz_title = f"Quiz_{group_id}"
    quiz_questions = ["Question 1", "Question 2", "Question 3"]  # Replace with your questions

    # Store the quiz information for this group
    active_quizzes[group_id] = {"title": quiz_title, "questions": quiz_questions, "current_question": 0, "started_by": message.from_user.id}

    # Store the quiz created by this user
    user_id = message.from_user.id
    user_quizzes[user_id] = {"title": quiz_title, "questions": quiz_questions}

    # Send the first question to the group
    send_question(group_id)

# Command to view the quiz created by the user
@app.on_message(filters.private & filters.command("viewmyquiz"))
def view_user_quiz(_, message):
    user_id = message.from_user.id

    # Check if the user has created a quiz
    if user_id in user_quizzes:
        quiz_info = f"Your Quiz:\nTitle: {user_quizzes[user_id]['title']}\nQuestions: {len(user_quizzes[user_id]['questions'])}"
        app.send_message(user_id, quiz_info)
    else:
        app.send_message(user_id, "You haven't created a quiz yet.")

# Command to show bot statistics
@app.on_message(filters.command("stats"))
def show_stats(_, message):
    # Get the number of quizzes and users from the database
    total_quizzes = quiz_collection.count_documents({})
    total_users = user_stats_collection.count_documents({})

    stats_message = f"Bot Statistics:\nTotal Quizzes: {total_quizzes}\nTotal Users: {total_users}"
    app.send_message(message.chat.id, stats_message)

# Command to show the list of chats where the bot is added
@app.on_message(filters.command("chatlist") & filters.user("admins"))
def show_chat_list(_, message):
    chat_list = app.get_dialogs()
    chat_names = [f"{chat.chat.id} - {chat.chat.title}" for chat in chat_list]

    chat_list_message = "Chats where the bot is added:\n" + "\n".join(chat_names)
    app.send_message(message.chat.id, chat_list_message)

# Function to send a quiz question
def send_question(group_id):
    # Get the active quiz for this group
    active_quiz = active_quizzes.get(group_id)

    if active_quiz:
        # Send the current question
        current_question = active_quiz["current_question"]
        question_text = f"Question {current_question + 1}: {active_quiz['questions'][current_question]}"
        app.send_message(group_id, question_text)
    else:
        app.send_message(group_id, "No active quiz in this group.")


# Command for Google search
@app.on_message(filters.command("google"))
def google_search(_, message):
    # Get the search query from the user's message
    search_query = " ".join(message.command[1:])

    # Perform the Google search
    search_results = list(search(search_query, num=5, stop=5, pause=2))

    # Send the search results as text
    if search_results:
        result_message = "\n".join(search_results)
        app.send_message(message.chat.id, f"Google search results for '{search_query}':\n{result_message}")
    else:
        app.send_message(message.chat.id, f"No results found for '{search_query}'.")


# Dictionary to store the current state of Tic Tac Toe games in different chats
tic_tac_toe_games = {}

# Command to start a Tic Tac Toe game
@app.on_message(filters.command("tictactoe"))
def start_tic_tac_toe(_, message):
    chat_id = message.chat.id

    # Check if a Tic Tac Toe game is already in progress
    if chat_id in tic_tac_toe_games:
        app.send_message(chat_id, "A Tic Tac Toe game is already in progress in this chat.")
        return

    # Initialize a new Tic Tac Toe game
    tic_tac_toe_games[chat_id] = {"board": [" "] * 9, "current_player": "X"}

    # Display the initial game board
    display_board(chat_id)

# Command to make a move in the Tic Tac Toe game
@app.on_message(filters.command("move") & filters.regex(r"^[1-9]$"))
def make_move(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    move = int(message.text)

    # Check if a Tic Tac Toe game is in progress in this chat
    if chat_id not in tic_tac_toe_games:
        app.send_message(chat_id, "No Tic Tac Toe game in progress. Use /tictactoe to start a new game.")
        return

    game = tic_tac_toe_games[chat_id]

    # Check if it's the current player's turn
    if user_id != get_current_player_id(game):
        app.send_message(chat_id, "It's not your turn.")
        return

    # Check if the selected move is valid
    if not is_valid_move(game, move):
        app.send_message(chat_id, "Invalid move. Please choose an empty cell (1-9).")
        return

    # Make the move
    game["board"][move - 1] = game["current_player"]

    # Check for a winner or a draw
    winner = check_winner(game)
    if winner:
        app.send_message(chat_id, f"Player {winner} wins!")
        end_game(chat_id)
    elif " " not in game["board"]:
        app.send_message(chat_id, "It's a draw!")
        end_game(chat_id)
    else:
        # Switch to the next player
        game["current_player"] = "O" if game["current_player"] == "X" else "X"
        display_board(chat_id)

# Function to display the current Tic Tac Toe board
def display_board(chat_id):
    game = tic_tac_toe_games[chat_id]
    board = game["board"]
    board_str = f"\n {board[0]} | {board[1]} | {board[2]} \n" \
                f"-----------\n" \
                f" {board[3]} | {board[4]} | {board[5]} \n" \
                f"-----------\n" \
                f" {board[6]} | {board[7]} | {board[8]} \n"

    app.send_message(chat_id, f"Current board:\n{board_str}\nPlayer {game['current_player']}'s turn. Make a move (1-9).")

# Function to check if a move is valid
def is_valid_move(game, move):
    return 1 <= move <= 9 and game["board"][move - 1] == " "

# Function to check if there is a winner
def check_winner(game):
    board = game["board"]
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != " ":
            return board[condition[0]]

    return None

# Function to get the ID of the current player
def get_current_player_id(game):
    current_player = game["current_player"]
    return 1 if current_player == "X" else 2

# Function to end the Tic Tac Toe game
def end_game(chat_id):
    del tic_tac_toe_games[chat_id]
    app.send_message(chat_id, "Game over. Use /tictactoe to start a new game.")


# Initialize the translator
translator = Translator()

# Command to translate text
@app.on_message(filters.command("translate"))
def translate_text(_, message):
    # Get the text to be translated from the user's message
    text_to_translate = " ".join(message.command[1:])

    # Check if the user provided text to translate
    if not text_to_translate:
        app.send_message(message.chat.id, "Please provide text to translate.")
        return

    # Detect the language of the input text
    source_language = translator.detect(text_to_translate).lang

    # Translate the text to the target language (Hindi in this case)
    translated_text = translator.translate(text_to_translate, dest='hi').text

    # Send the translation as a message
    translation_message = f"Original ({source_language}): {text_to_translate}\nTranslated (Hindi): {translated_text}"
    app.send_message(message.chat.id, translation_message)

# Initialize MongoDB client
mongo_client = MongoClient("Config.MONGODB_URI")
db = mongo_client["quiz_bot"]

# Define collections
quizzes_collection = db["quizzes"]

# Dictionary to store active quizzes by user ID
active_quizzes = {}

# Command to start creating a quiz in a private chat
@app.on_message(filters.private & filters.command("createquiz"))
def start_create_quiz(_, message):
    user_id = message.from_user.id

    # Check if the user is already creating a quiz
    if user_id in active_quizzes:
        app.send_message(user_id, "You are already creating a quiz.")
        return

    # Start creating a new quiz
    active_quizzes[user_id] = {"title": "", "questions": []}

    # Ask for the quiz title
    app.send_message(user_id, "Let's start creating a quiz! Enter the title of your quiz:")

# Handler for receiving the quiz title
@app.on_message(filters.private & ~filters.command & ~filters.text & filters.reply & filters.user(list(active_quizzes.keys())))
def receive_quiz_title(_, message):
    user_id = message.from_user.id

    # Check if the user is in the process of creating a quiz
    if user_id not in active_quizzes:
        return

    # Save the quiz title
    active_quizzes[user_id]["title"] = message.text

    # Ask for the first quiz question
    app.send_message(user_id, "Great! Now enter the first question for your quiz:")

# Handler for receiving quiz questions
@app.on_message(filters.private & ~filters.command & ~filters.text & filters.reply & filters.user(list(active_quizzes.keys())))
def receive_quiz_questions(_, message):
    user_id = message.from_user.id

    # Check if the user is in the process of creating a quiz
    if user_id not in active_quizzes:
        return

    # Save the quiz question
    active_quizzes[user_id]["questions"].append(message.text)

    # Ask if the user wants to add another question
    app.send_message(user_id, "Question added! Do you want to add another question? (Type 'yes' or 'no')")

# Handler for receiving the decision to add another question or finish
@app.on_message(filters.private & ~filters.command & filters.text & filters.user(list(active_quizzes.keys())))
def decide_add_question(_, message):
    user_id = message.from_user.id

    # Check if the user is in the process of creating a quiz
    if user_id not in active_quizzes:
        return

    decision = message.text.lower()

    if decision == "yes":
        # Ask for the next quiz question
        app.send_message(user_id, "Enter the next question for your quiz:")
    elif decision == "no":
        # Finish creating the quiz and store it in the database
        quiz_data = active_quizzes.pop(user_id)
        quizzes_collection.insert_one(quiz_data)
        app.send_message(user_id, "Quiz created and stored in the database! You can now start it in groups.")
    else:
        # Ask for a valid decision
        app.send_message(user_id, "Please type 'yes' if you want to add another question, or 'no' to finish.")


# Initialize the translator
translator = Translator()

# Command to display help information
@app.on_message(filters.command("help"))
def help_command(_, message):
    user_id = message.from_user.id

    help_message = (
        "Here are some commands you can use:\n\n"
        "/createquiz - Start creating a quiz in a private chat.\n"
        "/startquiz - Start a quiz in a group (admin-only).\n"
        "/translate - Translate text to Hindi or English.\n\n"
        "To create a quiz:\n"
        "1. Use /createquiz in a private chat.\n"
        "2. Follow the instructions to provide a title and questions.\n"
        "3. Type 'yes' or 'no' to add more questions or finish.\n\n"
        "To start a quiz in a group:\n"
        "1. Use /startquiz in the group (admin-only).\n"
        "2. Follow the instructions to start the quiz.\n\n"
        "To translate text:\n"
        "1. Use /translate <text> to translate to Hindi.\n"
        "2. Use /translate <text> en to translate to English.\n\n"
        "Enjoy using the bot!"
    )

    app.send_message(user_id, help_message)


# Command to start creating a quiz in a private chat
@app.on_message(filters.private & filters.command("createquiz"))
def start_create_quiz(_, message):
    user_id = message.from_user.id

    # Check if the user is already creating a quiz
    if user_id in active_quizzes:
        app.send_message(user_id, "You are already creating a quiz.")
        return

    # Start creating a new quiz
    active_quizzes[user_id] = {"title": "", "questions": []}

    # Ask for the quiz title
    app.send_message(user_id, "Let's start creating a quiz! Enter the title of your quiz:")

# Handler for receiving the quiz title
@app.on_message(filters.private & ~filters.command & ~filters.text & filters.reply & filters.user(list(active_quizzes.keys())))
def receive_quiz_title(_, message):
    user_id = message.from_user.id

    # Check if the user is in the process of creating a quiz
    if user_id not in active_quizzes:
        return

    # Save the quiz title
    active_quizzes[user_id]["title"] = message.text

    # Ask for the first quiz question
    app.send_message(user_id, "Great! Now enter the first question for your quiz:")

# Handler for receiving quiz questions
@app.on_message(filters.private & ~filters.command & ~filters.text & filters.reply & filters.user(list(active_quizzes.keys())))
def receive_quiz_questions(_, message):
    user_id = message.from_user.id

    # Check if the user is in the process of creating a quiz
    if user_id not in active_quizzes:
        return



# Command to start a group quiz (admins-only)
@app.on_message(filters.group & filters.command("startquiz") & filters.user("admins"))
def start_group_quiz(_, message):
    group_id = message.chat.id

    # Check if the group already has an active quiz
    if group_id in active_quizzes:
        app.send_message(group_id, "A quiz is already active in this group.")
        return

    # Generate a random quiz (replace this with your actual quiz generation logic)
    quiz_title = f"Quiz_{group_id}"
    quiz_questions = ["Question 1", "Question 2", "Question 3"]  # Replace with your questions

    # Store the quiz information for this group
    active_quizzes[group_id] = {"title": quiz_title, "questions": quiz_questions, "current_question": 0, "started_by": message.from_user.id}

    # Send the first question to the group
    send_question(group_id)

# Command to stop the group quiz (admins or user who started)
@app.on_message(filters.group & filters.command("stopquiz") & (filters.user("admins") | filters.user(lambda _, __, user: user.id == active_quizzes.get(_.chat.id, {}).get("started_by"))))
def stop_group_quiz(_, message):
    group_id = message.chat.id


    # Check if there is an active quiz in the group
    if group_id in active_quizzes:
        app.send_message(group_id, "The quiz has been stopped.")
        # Remove the quiz information for this group
        del active_quizzes[group_id]
    else:
        app.send_message(group_id, "No active quiz in this group.")


# Command to translate text
@app.on_message(filters.command("translate"))
def translate_text(_, message):
    # Get the text to be translated from the user's message
    text_to_translate = " ".join(message.command[1:])

    # Check if the user provided text to translate
    if not text_to_translate:
        app.send_message(message.chat.id, "Please provide text to translate.")
        return

    # Detect the language of the input text
    source_language = translator.detect(text_to_translate).lang

    # Translate the text to the target language (Hindi in this case)
    translated_text = translator.translate(text_to_translate, dest='hi').text

    # Send the translation as a message
    translation_message = f"Original ({source_language}): {text_to_translate}\nTranslated (Hindi): {translated_text}"
    app.send_message(message.chat.id, translation_message)



# Run the bot
if __name__ == "__main__":
    app.run()
