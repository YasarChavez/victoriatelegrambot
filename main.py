import os
import telebot
import google.generativeai as genai
from config import BOT_TOKEN, GEMINI_API_KEY, ADMIN_ID
from models.chat_session import ChatSession
from utils.config_manager import load_config, save_config
from handlers.admin_handlers import AdminHandlers
from handlers.user_handlers import UserHandlers

# Configure Google Generative AI
genai.configure(api_key=GEMINI_API_KEY)

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Create chats directory
os.makedirs("chats", exist_ok=True)

# Initialize configurations and sessions
config = load_config()
chat_sessions = {}

# Initialize handlers
admin_handlers = AdminHandlers(bot, config, chat_sessions)
user_handlers = UserHandlers(bot, config, chat_sessions)

# Register command handlers
@bot.message_handler(commands=["admin"])
def admin_help(message):
    admin_handlers.admin_help(message)

@bot.message_handler(commands=["delete_all"])
def delete_all(message):
    admin_handlers.system_management.delete_all(message)

@bot.message_handler(commands=["list_users"])
def list_users(message):
    admin_handlers.message_handlers.list_users(message)

@bot.message_handler(commands=["message_all"])
def message_all(message):
    admin_handlers.message_handlers.message_all(message)

@bot.message_handler(commands=["set_daily_limit"])
def set_daily_limit(message):
    admin_handlers.system_management.set_daily_limit(message)

@bot.message_handler(commands=["premium"])
def add_premium_user(message):
    admin_handlers.user_management.add_premium_user(message)

@bot.message_handler(commands=["clear_premium"])
def clear_premium_users(message):
    admin_handlers.user_management.clear_premium_users(message)

@bot.message_handler(commands=["list_messages"])
def list_messages(message):
    admin_handlers.message_handlers.list_messages(message)

@bot.message_handler(commands=["reset_all_messages"])
def reset_all_messages(message):
    admin_handlers.system_management.reset_all_messages(message)

@bot.message_handler(commands=["remove_premium"])
def remove_premium_user(message):
    admin_handlers.user_management.remove_premium_user(message)

@bot.message_handler(commands=["ayuda"])
def show_help(message):
    user_handlers.show_help(message)

@bot.message_handler(commands=["mi_id"])
def show_user_id(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, f"Tu ID de usuario es: {user_id}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_handlers.handle_message(message)

if __name__ == "__main__":
    bot.infinity_polling()