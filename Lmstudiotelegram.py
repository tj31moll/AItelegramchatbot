import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from openai import OpenAI

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

# Initialize OpenAI client for local model
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# Bot token and allowed chat IDs
BOT_TOKEN = 'your-bot-token'
ALLOWED_CHAT_IDS = []  # Replace with the allowed chat IDs

def chat(update, context):
    chat_id = update.message.chat_id

    # Check if the chat ID is allowed
    if chat_id not in ALLOWED_CHAT_IDS:
        logging.info(f"Unauthorized access attempt from chat ID: {chat_id}")
        return

    user_message = update.message.text

    # Process and respond to the message
    try:
        logging.info("Sending message to local model: %s", user_message)
        completion = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
        )

        reply = completion.choices[0].message.content
        update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        update.message.reply_text("An error occurred while processing your request.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Message handler for text messages
    dp.add_handler(MessageHandler(Filters.text, chat))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
