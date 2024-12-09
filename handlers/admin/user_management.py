from datetime import datetime, timedelta
from config import ADMIN_ID, ADMIN_PASSWORD

class AdminUserManagement:
    def __init__(self, bot, config, chat_sessions):
        self.bot = bot
        self.config = config
        self.chat_sessions = chat_sessions

    def add_premium_user(self, message):
        if message.from_user.id == ADMIN_ID:
            try:
                _, user_id, days = message.text.split()
                user_id = int(user_id)
                days = int(days)
                premium_until = datetime.now() + timedelta(days=days)
                self.config["premium_users"][str(user_id)] = premium_until.strftime("%Y-%m-%d")
                save_config(self.config)
                self.bot.send_message(
                    message.chat.id,
                    f"Usuario {user_id} agregado como premium por {days} días.",
                )
            except (IndexError, ValueError):
                self.bot.send_message(message.chat.id, "Uso: /premium [idUsuario] [diasPremium]")
        else:
            self.bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")

    def remove_premium_user(self, message):
        if message.from_user.id == ADMIN_ID:
            try:
                user_id = int(message.text.split()[1])
                if str(user_id) in self.config["premium_users"]:
                    del self.config["premium_users"][str(user_id)]
                    save_config(self.config)
                    self.bot.send_message(
                        message.chat.id, f"Estado premium del usuario {user_id} eliminado."
                    )
                else:
                    self.bot.send_message(
                        message.chat.id, f"El usuario {user_id} no es premium."
                    )
            except (IndexError, ValueError):
                self.bot.send_message(message.chat.id, "Uso: /remove_premium [idUsuario]")
        else:
            self.bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")

    def clear_premium_users(self, message):
        args = message.text.split()
        if len(args) > 1:
            password = args[1]
            if message.from_user.id == ADMIN_ID and password == ADMIN_PASSWORD:
                self.config["premium_users"] = {}
                save_config(self.config)
                self.bot.send_message(
                    message.chat.id, "Todos los usuarios premium han sido eliminados."
                )
            else:
                self.bot.send_message(
                    message.chat.id, "No tienes permiso o la contraseña es incorrecta."
                )
        else:
            self.bot.send_message(message.chat.id, "Debes proporcionar una contraseña.")