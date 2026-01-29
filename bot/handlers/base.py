from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from services.deepseek import DeepSeekService

# Router = группировка обработчиков
router = Router()

# Создаём экземпляр сервиса DeepSeek
deepseek = DeepSeekService()

# Системный промпт - описывает роль AI
SYSTEM_PROMPT = """Ты личный AI-ассистент в Telegram. 
Помогаешь с задачами, привычками, питанием и отвечаешь на вопросы.
Общайся дружелюбно и по-русски."""


@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обработчик команды /start
    
    @ = декоратор (вешает функцию на событие)
    router.message = слушаем сообщения
    Command("start") = фильтр для команды /start
    """
    await message.answer(
        "👋 Привет! Я твой AI-ассистент.\n\n"
        "Просто напиши мне что угодно, и я помогу!\n\n"
        "Доступные команды:\n"
        "/start - Начать\n"
        "/help - Помощь"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "🤖 Я умею:\n\n"
        "✅ Отвечать на вопросы\n"
        "✅ Давать советы\n"
        "✅ Помогать с планированием\n\n"
        "Скоро научусь:\n"
        "🔜 Голосовые сообщения\n"
        "🔜 Поиск в интернете\n"
        "🔜 Управление задачами"
    )


@router.message(F.text)
async def handle_text(message: Message):
    """
    Обработчик всех текстовых сообщений
    
    F.text = фильтр (только текст, не фото/видео)
    """
    
    # Показываем что бот "печатает"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )
    
    try:
        # Получаем ответ от DeepSeek
        ai_response = await deepseek.chat(
            user_message=message.text,
            system_prompt=SYSTEM_PROMPT
        )
        
        # Отправляем ответ пользователю
        await message.answer(ai_response)
        
    except Exception as e:
        # Если ошибка - сообщаем пользователю
        await message.answer(
            f"😔 Произошла ошибка: {str(e)}\n\n"
            "Попробуй ещё раз чуть позже."
        )
