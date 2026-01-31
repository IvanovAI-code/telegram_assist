import httpx
from config.settings import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

class DeepSeekService:
   """Сервис для общения ДикПикАПИ"""

   def __init__(self):
      self.api_key = DEEPSEEK_API_KEY
      self.base_url = DEEPSEEK_BASE_URL
      self.model = DEEPSEEK_MODEL

   async def chat(self, user_message: str, system_prompt: str = None, history: list = None) -> str:
      """
      Отправляет сообщение пользователя в DeepSeek и возращает ответ

      args:
         user_message: сообщение пользователя
         system_prompt: системный промт
         history: история предыдущих сообщений (опционально)

      Returns:
         Ответ от DeepSeek

      """

      #формируем список сообщений
      messages = []

      #Если имеется системный промт - добавляем первым
      if system_prompt:
         messages.append({
            "role": "system",
            "content": system_prompt
         })

      #Добавляем историю если есть
      if history:
         messages.extend(history)

      #Добавляем сообщение пользователя
      messages.append({
         "role": "user",
         "content": user_message
      })

      #Подготваливаем запрос к API
      payload = {
         "model": self.model,
         "messages": messages,
         "temperature": 0.7, #креативность модели. 0.7 - баланс.

         "max_tokens": 600, #ограничиваем длину ответа для краткости

      }

      #отправляем асинхронный HTTP запрос 
      headers = {
         "Authorization": f"Bearer {self.api_key}",
         "Content-Type": "application/json"
         }

      async with httpx.AsyncClient(timeout=60.0) as client: #тут так же играемся с таймаутами.
         responce = await client.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers=headers
         )
         
         #проверяем статус ответа
         responce.raise_for_status()
         

         #парсим JSON ответ
         data = responce.json()

         #Извлекаем текст ответа
         return data["choices"][0]["message"]["content"]


