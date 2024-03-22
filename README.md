# Claude Conversation Bot

The Claude Conversation Bot is a Telegram bot that allows users to chat with the Anthropic AI assistant, Claude. Users can start new conversations, switch between different language models, and the bot will remember and respond to previous messages. The conversation history is saved to both text and JSON files for each user, ensuring privacy and legal compliance.

## Features

- Start a new conversation with the `/start` or `/new` commands
- Switch between different language models using the `/opus`, `/sonnet`, and `/haiku` commands
- View available commands using the `/help` command
- Conversation history is saved to text and JSON files for each user
- Ensures privacy and legal compliance by storing conversation data separately for each user

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/claude-conversation-bot.git
   ```
2. Navigate to the project directory:
   ```
   cd claude-conversation-bot
   ```
3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project directory and add your Anthropic API key and Telegram bot API token:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```
6. Run the bot:
   ```
   python claude_t_convo.py
   ```

## Usage

Once the bot is running, you can interact with it using the following commands:

- `/start` or `/new`: Start a new conversation
- `/opus`: Switch to the Claude 3 Opus model
- `/sonnet`: Switch to the Claude 3 Sonnet model
- `/haiku`: Switch to the Claude 3 Haiku model
- `/help`: List all available commands

The bot will remember your previous messages and respond accordingly. Your conversation history will be saved to text and JSON files in the project directory.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```

**LICENSE**

```
MIT License

Copyright (c) 2023 Marcell Bandi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
