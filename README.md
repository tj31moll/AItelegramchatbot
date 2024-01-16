# AItelegramchatbot

![Screenshot](https://github.com/tj31moll/AItelegramchatbot/assets/91799649/a6a7031e-014e-4a07-96b3-b460b4b1a9f5)

This repository contains a Python script for a Telegram bot that integrates with OpenAI's API or other compatible REST APIs (such as Jan https://jan.ai/). It's designed to provide an interactive AI experience through Telegram, using simple chat functionalities.

## Features

- **Easy Interaction**: Users can interact with the bot using a `/chat` command followed by their message.
- **Flexible API Integration**: Compatible with OpenAI and similar REST APIs.
- **Customizable Responses**: The bot can be configured to modify its behavior, response tone, and other settings.

## Getting Started

### Prerequisites

- Python 3.x
- `python-telegram-bot` library
- OpenAI API or a compatible API

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/tj31moll/AItelegramchatbot]
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key and Telegram Bot Token in the script.

### Usage

Run the script:
```bash
python bot.py
```

## Configuration

- **Bot Token**: Replace `your-bot-token` in the script with your actual Telegram Bot Token.
- **API Key**: Set up your OpenAI API key or the key for an alternative API.
- **Allowed Chat IDs**: Define the chat IDs that are allowed to interact with the bot for security.
- **System Prompt**: Adding a System PromptSystem Prompt Configuration: To customize the behavior of your bot, you can add a system prompt. This prompt acts as an initial input to the AI model, influencing how the bot responds to user messages.To add a system prompt, locate the section in the script where the chat function is defined.Add a variable to hold your prompt, like system_prompt = "Your system prompt here".When creating the completion request to the OpenAI API, include the system_prompt as part of the input. For example:

` completion = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ],
    temperature=0.7,)`

- This system prompt can include instructions or a specific tone/style you want the bot to follow, setting the context for its responses.ExampleHere's an example of setting a system prompt that instructs the bot to be friendly and informative:system_prompt = "Be friendly and informative in your responses."Remember, the system prompt is a powerful tool to guide the interaction flow and style of your bot. Feel free to experiment with different prompts to see how they affect the bot's behavior.

## Contributing

Contributions, issues, and feature requests are welcomed!

## License

Distributed under the MIT License. See `LICENSE` for more information.


## Acknowledgements
Jan builds on top of other open-source projects: License - Jan is free and open source, under the AGPLv3 license.
OpenAI
Python and libraries
