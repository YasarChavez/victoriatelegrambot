import os
import json
from datetime import datetime
from config import ADMIN_ID, ADMIN_PASSWORD
from utils.config_manager import save_config

class AdminSystemManagement:
    def __init__(self, bot, config, chat_sessions):
        self.bot = bot
        self.config = config
        self.chat_sessions = chat_sessions

    def delete_all(self, message):
        if message.from_user.id == ADMIN_ID:
            try:
                folder = "chats"
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                self.chat_sessions.clear()
                self.bot.send_message(
                    message.chat.id, "Todos los historiales han sido eliminados."
                )
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Error eliminando historiales: {str(e)}")
        else:
            self.bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")

    def set_daily_limit(self, message):
        if message.from_user.id == ADMIN_ID:
            try:
                limit = int(message.text.split()[1])
                self.config["daily_limit"] = limit
                save_config(self.config)
                self.bot.send_message(
                    message.chat.id, f"Límite diario de chats establecido en {limit}."
                )
            except (IndexError, ValueError):
                self.bot.send_message(message.chat.id, "Uso: /set_daily_limit [limite]")
        else:
            self.bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")

    def reset_all_messages(self, message):
        if message.from_user.id == ADMIN_ID:
            args = message.text.split()
            if len(args) > 1:
                password = args[1]
                if password == ADMIN_PASSWORD:
                    folder = "chats"
                    try:
                        for filename in os.listdir(folder):
                            if filename.endswith(".json"):
                                with open(
                                    os.path.join(folder, filename), "r+", encoding="utf-8"
                                ) as file:
                                    data = json.load(file)
                                    data["message_count"] = 0
                                    file.seek(0)
                                    json.dump(data, file, ensure_ascii=False, indent=4)
                                    file.truncate()
                        
                        for chat_id in self.chat_sessions:
                            self.chat_sessions[chat_id].message_count = 0

                        self.bot.send_message(
                            message.chat.id, "Se han reseteado todos los mensajes de los usuarios."
                        )
                    except Exception as e:
                        self.bot.send_message(
                            message.chat.id, f"Error reseteando mensajes: {str(e)}"
                        )
                else:
                    self.bot.send_message(
                        message.chat.id, "Contraseña incorrecta."
                    )
            else:
                self.bot.send_message(
                    message.chat.id, "Debes proporcionar una contraseña."
                )
        else:
            self.bot.send_message(
                message.chat.id, "No tienes permiso para usar este comando."
            )