import httpx
from config.settings import SERPER_API_KEY

class SerperService:
    """Сервис для поиска в интернете через Google Serper API"""

    def __init__(self):
        self.api_key = SERPER_API_KEY
        self.base_url = "https://google.serper.dev"

    async def search(self, query: str, num_results: int = 5) -> dict:
        """
        Выполняет поиск в Google через Serper API

        Args:
            query: Поисковый запрос
            num_results: Количество результатов (по умолчанию 5)

        Returns:
            Словарь с результатами поиска
        """
        payload = {
            "q": query,
            "num": num_results,  # Количество результатов
            "gl": "ru",  # Географическая локация (Россия)
            "hl": "ru"   # Язык интерфейса (русский)
        }

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/search",
                json=payload,
                headers=headers
            )

            response.raise_for_status()
            return response.json()

    async def search_images(self, query: str, num_results: int = 3) -> list:
        """
        Выполняет поиск изображений в Google через Serper API

        Args:
            query: Поисковый запрос
            num_results: Количество результатов (по умолчанию 3)

        Returns:
            Список URL изображений
        """
        payload = {
            "q": query,
            "num": num_results,
            "gl": "ru",
            "hl": "ru"
        }

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/images",  # Используем /images эндпоинт
                json=payload,
                headers=headers
            )

            response.raise_for_status()
            data = response.json()

            # Извлекаем URL изображений
            image_urls = []
            if "images" in data:
                for img in data["images"][:num_results]:
                    image_url = img.get("imageUrl")
                    if image_url:
                        image_urls.append(image_url)

            return image_urls

    def format_results(self, search_data: dict) -> str:
        """
        Форматирует результаты поиска в читаемый текст

        Args:
            search_data: Данные от Serper API

        Returns:
            Отформатированная строка с результатами
        """
        formatted = []

        # Проверяем наличие органических результатов
        if "organic" in search_data and search_data["organic"]:
            formatted.append("🔍 Результаты поиска:\n")

            for i, result in enumerate(search_data["organic"], 1):
                title = result.get("title", "Без названия")
                snippet = result.get("snippet", "")
                link = result.get("link", "")

                formatted.append(f"{i}. {title}")
                if snippet:
                    formatted.append(f"   {snippet}")
                formatted.append(f"   🔗 {link}\n")

        # Если есть блок "People also ask"
        if "peopleAlsoAsk" in search_data:
            formatted.append("\n❓ Похожие вопросы:")
            for item in search_data["peopleAlsoAsk"][:3]:  # Показываем только 3
                question = item.get("question", "")
                answer = item.get("snippet", "")
                formatted.append(f"\nВопрос: {question}")
                if answer:
                    formatted.append(f"Ответ: {answer}")

        if not formatted:
            return "😔 Результаты не найдены"

        return "\n".join(formatted)
