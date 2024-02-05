from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import requests
import json

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token received from BotFather
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. Send me a message, and I will process it.')

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    # Prepare the data for the POST request
    data = {
        "messages": [
            {"content": "You are a helpful assistant.", "role": "system"},
            {"content": user_message, "role": "user"}
        ],
        "model": "tinyllama-1.1b",
        "stream": True,
        "max_tokens": 2048,
        "stop": ["hello"],
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": 0.7,
        "top_p": 0.95
    }

    # Specify the URL and headers
    url = 'http://localhost:1337/v1/chat/completions'
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response and send a reply back to the user
        reply = response.json()  # Assuming the response JSON contains a field that can be directly sent as a reply
        update.message.reply_text(f'Response: {reply}')
    else:
        update.message.reply_text('There was an error processing your request.')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
