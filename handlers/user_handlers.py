from datetime import datetime
from models.chat_session import ChatSession

class UserHandlers:
    def __init__(self, bot, config, chat_sessions):
        self.bot = bot
        self.config = config
        self.chat_sessions = chat_sessions

    def show_help(self, message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        is_premium = str(user_id) in self.config["premium_users"]
        today = datetime.now().date()

        if is_premium:
            premium_until = datetime.strptime(
                self.config["premium_users"][str(user_id)], "%Y-%m-%d"
            ).date()
            time_left = (premium_until - today).days
            status_text = f"Eres usuario VIP ⭐.\n\n"
            if time_left > 0:
                status_text += f"Tiempo restante de VIP:\n{time_left} días."
            else:
                status_text += "Tu membresía VIP ha expirado."
            status_text += "\nTienes mensajes Ilimitados."
        else:
            status_text = f"Eres usuario común 😢.\n\n"
            chat_session = self.chat_sessions.get(chat_id)
            if chat_session:
                messages_sent_today = chat_session.message_count
                messages_left_today = self.config["daily_limit"] - messages_sent_today
                status_text += f"Mensajes enviados hoy: \n{messages_sent_today}.\nMensajes restantes: \n{messages_left_today}."

        self.bot.send_message(chat_id, status_text + "\n\nAdministrador:\n@ChavezYasar\n")
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bot.send_message(message.chat.id, f"Fecha y hora del servidor:\n{today}")
        self.bot.send_message(message.chat.id, f"Tu ID de usuario es: \n{user_id}")

    def handle_message(self, message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        is_premium = str(user_id) in self.config["premium_users"]
        today = datetime.now().date()

        if chat_id not in self.chat_sessions:
            self.chat_sessions[chat_id] = ChatSession(chat_id)

        chat_session = self.chat_sessions[chat_id]

        if chat_session.last_message_date < today:
            chat_session.message_count = 0
            chat_session.last_message_date = today

        if not is_premium and chat_session.message_count >= self.config["daily_limit"]:
            self.bot.send_message(chat_id, "Has alcanzado tu límite diario de chats.")
            return

        chat_session.message_count += 1
        chat_session.history.append({"role": "user", "parts": [message.text]})
        chat_session.save_to_json()

        response = chat_session.model.start_chat(history=chat_session.history).send_message(
            message.text
        )
        chat_session.history.append({"role": "model", "parts": [response.text]})
        chat_session.save_to_json()

        self.bot.reply_to(message, response.text)