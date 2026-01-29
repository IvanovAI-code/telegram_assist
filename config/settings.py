import os
from dotenv import load_dotenv

#грузим переменные из env файла
load_dotenv()

#Телеграм
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

#ДикПик:
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat" #выбираем быструю модель, нам ее хватит 

#serper.dev
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
