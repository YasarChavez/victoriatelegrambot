from datetime import datetime
import os
from config import ADMIN_ID

class AdminMessageHandlers:
    def __init__(self, bot, config, chat_sessions):
        self.bot = bot
        self.config = config
        self.chat_sessions = chat_sessions

    def list_users(self, message):
        if message.from_user.id == ADMIN_ID:
            folder = "chats"
            users_list = []
            try:
                for filename in os.listdir(folder):
                    if filename.endswith(".json"):
                        chat_id = filename.split("_")[1].split(".")[0]
                        users_list.append(chat_id)
                users_list_str = "\n".join(users_list)
                self.bot.send_message(message.chat.id, f"Usuarios activos:\n{users_list_str}")
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Error listando usuarios: {str(e)}")
        else:
            self.bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")

    def message_all(self, message):
        if message.from_user.id == ADMIN_ID:
            text = message.text.split("/message_all", 1)[1].strip()
            folder = "chats"
            try:
                for filename in os.listdir(folder):
                    if filename.endswith(".json"):
                        chat_id = filename.split("_")[1].split(".")[0]
                        self.bot.send_message(chat_id, text)
                self.bot.send_message(message.chat.id, "Mensaje enviado a todos los usuarios.")
            except Exception as e:
                self.bot.send_message(
                    message.chat.id,
                    f"Error enviando mensaje a todos los usuarios: {str(e)}",
                )
        else:
            self.bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")

    def list_messages(self, message):
        if message.from_user.id == ADMIN_ID:
            folder = "chats"
            messages_list = []
            try:
                for filename in os.listdir(folder):
                    if filename.endswith(".json"):
                        chat_id = filename.split("_")[1].split(".")[0]
                        with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                            data = json.load(file)
                            message_count = data.get("message_count", 0)
                            messages_list.append(f"Usuario {chat_id}: {message_count} mensajes")
                messages_list_str = "\n".join(messages_list)
                self.bot.send_message(
                    message.chat.id,
                    f"Cantidad de mensajes por usuario:\n{messages_list_str}",
                )
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Error listando mensajes: {str(e)}")
        else:
            self.bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")