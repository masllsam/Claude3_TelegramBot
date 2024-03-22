import anthropic
import argparse
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, filters

def generate_env_file():
    if not os.path.exists('.env'):
        anthropic_api_key = input("Enter your Anthropic API key: ")
        telegram_bot_token = input("Enter your Telegram Bot API token: ")
        with open('.env', 'w') as file:
            file.write(f"ANTHROPIC_API_KEY={anthropic_api_key}\n")
            file.write(f"TELEGRAM_BOT_TOKEN={telegram_bot_token}\n")
        print("Generated .env file with API keys.")
    else:
        load_dotenv()

def save_conversation(user_id, username, prompt, response, timestamp):
    with open(f'conversation_{user_id}.txt', 'a') as file:
        file.write(f"[{timestamp}] {username}: {prompt}\n")
        file.write(f"[{timestamp}] Claude: {response}\n\n")

    conversation_file = f'conversation_{user_id}.json'
    conversation = load_conversation(user_id)
    conversation.extend([
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ])
    with open(conversation_file, 'w') as file:
        json.dump(conversation, file)

def load_conversation(user_id):
    conversation_file = f'conversation_{user_id}.json'
    if os.path.exists(conversation_file):
        with open(conversation_file, 'r') as file:
            return json.load(file)
    return []

def generate_response(conversation, model):
    client = anthropic.Anthropic(api_key=anthropic_api_key)
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=0.0,
        system="You are a helpful assistant.",
        messages=conversation
    )
    
    # Concatenate the text content of all ContentBlock objects
    response_text = ""
    for content_block in response.content:
        response_text += content_block.text
    return response_text

async def start_command(update, context):
    user_id = update.effective_user.id
    context.user_data['conversation'] = load_conversation(user_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Claude Conversation Bot! Send me a message to start chatting with Claude.")

async def new_conversation_command(update, context):
    user_id = update.effective_user.id
    conversation_file = f'conversation_{user_id}.json'
    if os.path.exists(conversation_file):
        os.remove(conversation_file)
    context.user_data['conversation'] = []
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Starting a new conversation.")

async def opus_command(update, context):
    context.user_data['model'] = 'claude-3-opus-20240229'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to Claude 3 Opus model.")

async def sonnet_command(update, context):
    context.user_data['model'] = 'claude-3-sonnet-20240229'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to Claude 3 Sonnet model.")

async def haiku_command(update, context):
    context.user_data['model'] = 'claude-3-haiku-20240307'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to Claude 3 Haiku model.")

async def help_command(update, context):
    help_text = "Available commands:\n" \
                "/start - Start a new conversation\n" \
                "/new - Start a new conversation\n" \
                "/opus - Switch to Claude 3 Opus model\n" \
                "/sonnet - Switch to Claude 3 Sonnet model\n" \
                "/haiku - Switch to Claude 3 Haiku model\n" \
                "/help - List all available commands"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

async def message_handler(update, context):
    if update.message:
        user_id = update.effective_user.id
        username = update.effective_user.username
        prompt = update.message.text
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        model = context.user_data.get('model', 'claude-3-opus-20240229')
        
        try:
            conversation = context.user_data.setdefault('conversation', [])
            response = generate_response(conversation + [{"role": "user", "content": prompt}], model)
            conversation.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response}
            ])
            await send_response(update, context, response)
            save_conversation(user_id, username, prompt, response, timestamp)
        except anthropic.AuthenticationError:
            await send_error_message(update, context, "Sorry, there was an issue with the API key. Please check your Anthropic API key and try again.")
        except anthropic.BadRequestError as e:
            await send_error_message(update, context, f"Oops, something went wrong: {str(e)}")
            print(f"Error: {e}")
        except Exception as e:
            await send_error_message(update, context, f"Oops, something went wrong: {str(e)}")
            print(f"Error: {e}")
    else:
        print("No message received.")

async def send_response(update, context, response):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def send_error_message(update, context, error_message):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interact with Claude using an API key.')
    args = parser.parse_args()
    generate_env_file()
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(telegram_bot_token).build()
    start_handler = CommandHandler('start', start_command)
    application.add_handler(start_handler)
    new_conversation_handler = CommandHandler('new', new_conversation_command)
    application.add_handler(new_conversation_handler)
    opus_handler = CommandHandler('opus', opus_command)
    application.add_handler(opus_handler)
    sonnet_handler = CommandHandler('sonnet', sonnet_command)
    application.add_handler(sonnet_handler)
    haiku_handler = CommandHandler('haiku', haiku_command)
    application.add_handler(haiku_handler)
    help_handler = CommandHandler('help', help_command)
    application.add_handler(help_handler)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    application.add_handler(message_handler)
    application.run_polling()
    print("Claude Conversation Bot started. Press Ctrl+C to stop.")