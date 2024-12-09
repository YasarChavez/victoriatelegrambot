# Victoria Telegram Bot

Un bot de Telegram basado en Gemini AI que proporciona respuestas inteligentes en español.          
[Victoria Asistente IA](https://t.me/Victoria_IA_Asistente_bot) ← (Bot en Telegram)         
![ImagenVictoria](/logo/Victoria%20Asistente%20IA.jpg)

## Requisitos

- Python 3.8+
- Token de Bot de Telegram
- API Key de Google Gemini
- Docker (opcional)

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
TOKEN=tu_token_de_telegram
ADMIN_ID=tu_id_de_admin
ADMIN_PASSWORD=tu_contraseña_de_admin
GEMINI_API_KEY=tu_api_key_de_gemini
```

## Instalación Local

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd victoria-telegram-bot
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar el bot:
```bash
python main.py
```

## Despliegue con Docker

1. Construir la imagen:
```bash
docker build -t victoria-bot .
```

2. Ejecutar el contenedor:
```bash
docker run -d --env-file .env victoria-bot
```

## Estructura del Proyecto

```
├── config.py               # Configuración global
├── main.py                # Punto de entrada
├── requirements.txt       # Dependencias
├── Dockerfile            # Configuración de Docker
├── README.md             # Documentación
├── handlers/
│   ├── admin_handlers.py # Manejadores de comandos admin
│   └── user_handlers.py  # Manejadores de comandos usuario
├── models/
│   └── chat_session.py   # Modelo de sesión de chat
└── utils/
    └── config_manager.py # Utilidades de configuración
```

## Comandos Disponibles

### Comandos de Usuario
- `/ayuda` - Muestra información de ayuda y estado
- `/mi_id` - Muestra tu ID de usuario

### Comandos de Administrador
- `/admin` - Muestra comandos de administrador
- `/delete_all` - Elimina todos los historiales
- `/list_users` - Lista usuarios activos
- `/message_all [mensaje]` - Envía mensaje a todos
- `/set_daily_limit [limite]` - Establece límite diario
- `/premium [idUsuario] [diasPremium]` - Agrega usuario premium
- `/clear_premium [contraseña]` - Elimina usuarios premium
- `/list_messages` - Lista mensajes por usuario
- `/reset_messages [idUsuario]` - Resetea mensajes
- `/reset_all_messages [contraseña]` - Resetea todos los contadores
- `/remove_premium [idUsuario]` - Elimina estado premium

## Mantenimiento

### Logs
Los logs se almacenan en la carpeta `chats/` con el formato `chat_[ID].json`

### Respaldo
Se recomienda hacer respaldo periódico de:
- Carpeta `chats/`
- Archivo `config.json`

## Seguridad

- Las credenciales se manejan via variables de entorno
- Los historiales de chat se almacenan localmente
- El acceso admin está protegido por ID y contraseña