from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TELEGRAM_TOKEN = 'your_telegram_bot_token_here'

# Phixtral Model and Tokenizer
model_name = "mlabonne/phixtral-4x2_8"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", load_in_4bit=True, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Set default device to CUDA (GPU)
torch.set_default_device("cuda")

# Command Handlers
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I am your Phixtral-powered chatbot. How can I assist you today?')

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send me a message and I will respond with AI-generated content.')

def chat(update, context):
    """Generate response from Phixtral model."""
    user_input = update.message.text

    prompt = f'''
    system
    You are Phixtral, a helpful AI assistant.
    user
    {user_input}
    assistant
    '''

    inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False)
    outputs = model.generate(**inputs, max_length=200)
    response = tokenizer.batch_decode(outputs)[0]
    response = response.split('assistant')[1].strip()  # Extract only the assistant's response

    update.message.reply_text(response)

def main():
    """Start the bot."""
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    
    # Register a message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
