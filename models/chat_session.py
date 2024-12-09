import json
import os
from datetime import datetime
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from config import GENERATION_CONFIG

class ChatSession:
    def __init__(self, chat_id):
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=GENERATION_CONFIG,
            system_instruction="Responder en español, tu nombre es Victoria. Nunca digas que eres una inteligencia artificial.",
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
        )
        self.history = []
        self.chat_id = chat_id
        self.message_count = 0
        self.last_message_date = datetime.now().date()
        self.load_from_json()

    def load_from_json(self):
        filename = f"chats/chat_{self.chat_id}.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.history = data.get("history", [])
                self.message_count = data.get("message_count", 0)
                self.last_message_date = datetime.strptime(
                    data.get("last_message_date", str(datetime.now().date())),
                    "%Y-%m-%d",
                ).date()

    def save_to_json(self):
        filename = f"chats/chat_{self.chat_id}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            data = {
                "history": self.history,
                "message_count": self.message_count,
                "last_message_date": str(self.last_message_date),
            }
            json.dump(data, file, ensure_ascii=False, indent=4)