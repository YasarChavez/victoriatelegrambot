from datetime import datetime
from config import ADMIN_ID
from .admin.message_handlers import AdminMessageHandlers
from .admin.user_management import AdminUserManagement
from .admin.system_management import AdminSystemManagement

class AdminHandlers:
    def __init__(self, bot, config, chat_sessions):
        self.bot = bot
        self.config = config
        self.chat_sessions = chat_sessions
        self.message_handlers = AdminMessageHandlers(bot, config, chat_sessions)
        self.user_management = AdminUserManagement(bot, config, chat_sessions)
        self.system_management = AdminSystemManagement(bot, config, chat_sessions)

    def admin_help(self, message):
        if message.from_user.id == ADMIN_ID:
            help_text = (
                "/delete_all - Eliminar todos los historiales de chat\n"
                "/list_users - Listar todos los usuarios activos\n"
                "/message_all [mensaje] - Enviar un mensaje a todos los usuarios\n"
                "/set_daily_limit [limite] - Establecer el límite de chats diarios\n"
                "/premium [idUsuario] [diasPremium] - Agregar usuario premium\n"
                "/clear_premium [contraseña] - Eliminar todos los usuarios premium\n"
                "/list_messages - Listar la cantidad de mensajes por usuario\n"
                "/reset_messages [idUsuario] - Resetear mensajes de un usuario\n"
                "/reset_all_messages [contraseña] - Reiniciar todos los contadores\n"
                "/remove_premium [idUsuario] - Eliminar estado premium\n"
                "/mi_id - Mostrar la ID del usuario\n"
            )
            self.bot.send_message(message.chat.id, help_text)
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.bot.send_message(message.chat.id, f"Fecha y hora del servidor:\n{today}")
        else:
            self.bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")