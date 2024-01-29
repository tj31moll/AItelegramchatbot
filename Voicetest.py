import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from openai import OpenAI
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import requests
from pydub import AudioSegment
import io

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

# Initialize Whisper model
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")

# Initialize OpenAI client for local model
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# Bot token and allowed chat IDs
BOT_TOKEN = 'your-bot-token'
ALLOWED_CHAT_IDS = []  # Replace with the allowed chat IDs

def process_voice_message(voice_message):
    """Process a voice message using Whisper."""
    file = voice_message.get_file()
    file.download('voice.ogg')

    # Convert OGG to WAV
    audio = AudioSegment.from_ogg('voice.ogg')
    audio.export('voice.wav', format='wav')

    # Transcribe using Whisper
    input_audio = AudioSegment.from_wav('voice.wav').get_array_of_samples()
    input_features = processor(input_audio, sampling_rate=16000, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return ' '.join(transcription)

def chat(update, context):
    chat_id = update.message.chat_id

    # Check if the chat ID is allowed
    if chat_id not in ALLOWED_CHAT_IDS:
        logging.info(f"Unauthorized access attempt from chat ID: {chat_id}")
        return

    # Process text or voice message
    if update.message.voice:
        context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        user_message = process_voice_message(update.message.voice)
    else:
        user_message = update.message.text

    # Send processed message to local model
    try:
        logging.info("Sending message to local model: %s", user_message)
        completion = client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": user_message}],
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

    # Handlers for text and voice messages
    dp.add_handler(MessageHandler(Filters.text, chat))
    dp.add_handler(MessageHandler(Filters.voice, chat))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
