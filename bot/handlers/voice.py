import os
from aiogram import Router, F
from aiogram.types import Message
from services.deepseek import DeepSeekService
from services.whisper import WhisperService

# Router для голосовых сообщений
router = Router()

# Создаём сервисы
deepseek = DeepSeekService()
whisper = WhisperService(model_size="small")  # small модель - отличное качество распознавания

# Папка для временных файлов
TEMP_DIR = "/tmp/telegram_voice"
os.makedirs(TEMP_DIR, exist_ok=True)

# Системный промпт
SYSTEM_PROMPT = """Ты личный AI-ассистент в Telegram.
Помогаешь с задачами, привычками, питанием и отвечаешь на вопросы.
Общайся дружелюбно и по-русски."""


@router.message(F.voice)
async def handle_voice(message: Message):
    """
    Обработчик голосовых сообщений

    F.voice = фильтр (только голосовые сообщения)
    """

    # Показываем что бот "слушает"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    try:
        # Формируем путь для временного файла
        file_path = os.path.join(TEMP_DIR, f"{message.voice.file_id}.ogg")

        # Скачиваем голосовое сообщение
        await message.bot.download(
            message.voice,
            destination=file_path
        )

        # Сообщаем что распознаём
        status_msg = await message.answer("🎤 Слушаю...")

        # Распознаём голос
        recognized_text = await whisper.transcribe(file_path)

        # Обновляем статус
        await status_msg.edit_text(f"📝 Распознал: {recognized_text}\n\n💭 Думаю...")

        # Получаем ответ от AI
        ai_response = await deepseek.chat(
            user_message=recognized_text,
            system_prompt=SYSTEM_PROMPT
        )

        # Удаляем статусное сообщение и отправляем ответ
        await status_msg.delete()
        await message.answer(f"🎤 Вы сказали: {recognized_text}\n\n🤖 Ответ:\n{ai_response}")

    except Exception as e:
        await message.answer(
            f"😔 Произошла ошибка при обработке голоса: {str(e)}\n\n"
            "Попробуй ещё раз."
        )
