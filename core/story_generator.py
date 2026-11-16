"""Story and scene plan generator for Story Studio RU/UA.

Supports:
- Local LLMs (Ollama, LM Studio, vLLM, text-generation-webui via OpenAI-compatible API)
- Cloud LLM endpoints (OpenAI, Groq, Claude proxy, etc.)
- Offline parametric story generator (zero network dependency)
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from .prompt_builder import enhance_prompt

SYSTEM_PROMPT_UK = """Ти — досвідчений сценарист та режисер захоплюючих відеоісторій для Shorts, Reels та YouTube.
Твоя мета: написати сценарій ролика на задану тему за чіткою структурою:
1. Гачок (Hook) — несподіваний факт або інтригуюче запитання, яке захоплює увагу з першої секунди.
2. Розвиток та напруга (Tension/Action) — що насправді сталося, невідомі деталі події.
3. Розв'язка та висновок (Climax/Takeaway) — кульмінація та глибока думка для глядача.

Вимоги:
- Мова дикторського тексту: природна українська мова, без канцеляризмів.
- 3–5 сцен. Текст кожної сцени: 15–35 слів (щоб диктор читав її за 4–7 секунд).
- Для кожної сцени надай короткий опис кадру та англомовний visual prompt для генерації зображення.

Виведи ТІЛЬКИ валідний JSON у наступному форматі без зайвого тексту:
{
  "title": "Назва ролика",
  "locale": "uk",
  "style": "cinematic",
  "scenes": [
    {
      "text": "Текст репліки диктора українською",
      "visual_description": "Короткий опис того, що ми бачимо в кадрі",
      "image_prompt": "Cinematic visual description in English for image generator"
    }
  ]
}
"""

SYSTEM_PROMPT_RU = """Ты — опытный сценарист и режиссёр захватывающих видеоисторий для Shorts, Reels и YouTube.
Твоя цель: написать сценарий ролика на заданную тему по чёткой структуре:
1. Крючок (Hook) — неожиданный факт или интригующий вопрос, цепляющий с первой секунды.
2. Развитие и напряжение (Tension/Action) — что произошло на самом деле, неизвестные детали.
3. Развязка и вывод (Climax/Takeaway) — кульминация и запоминающийся вывод.

Требования:
- Язык дикторского текста: естественный русский язык, живая подача, без канцеляризмов.
- 3–5 сцен. Текст каждой сцены: 15–35 слов (время чтения диктором 4–7 секунд).
- Для каждой сцены укажи короткое описание кадра и англоязычный visual prompt для генерации изображения.

Выведи ТОЛЬКО валидный JSON в следующем формате без лишнего текста:
{
  "title": "Название ролика",
  "locale": "ru",
  "style": "cinematic",
  "scenes": [
    {
      "text": "Текст реплики диктора на русском",
      "visual_description": "Краткое описание происходящего в кадре",
      "image_prompt": "Cinematic visual description in English for image generator"
    }
  ]
}
"""

CYRILLIC_TO_LATIN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye',
    'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l',
    'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'yu',
    'я': 'ya', 'ё': 'yo', 'ы': 'y', 'э': 'e',
}


def to_latin_subject(text: str) -> str:
    """Convert Cyrillic topic to clean Latin descriptor for English visual models."""
    res = []
    for char in text.lower():
        if char in CYRILLIC_TO_LATIN:
            res.append(CYRILLIC_TO_LATIN[char])
        elif char.isalnum() or char in ' -':
            res.append(char)
    clean = ''.join(res).strip()
    return clean if clean else "historic event"


@dataclass
class StoryScene:
    text: str
    visual_description: str
    image_prompt: str
    image: Optional[str] = None


@dataclass
class StoryPlan:
    title: str
    locale: str
    topic: str
    style: str
    scenes: List[StoryScene] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "locale": self.locale,
            "topic": self.topic,
            "style": self.style,
            "scenes": [asdict(s) for s in self.scenes],
        }

    def to_first_video_plan(self) -> Dict[str, Any]:
        """Convert into first_video.py compatible plan schema."""
        return {
            "title": self.title,
            "locale": self.locale,
            "scenes": [
                {
                    "text": s.text,
                    **({"image": s.image} if s.image else {})
                }
                for s in self.scenes
            ],
        }


def _extract_json(raw: str) -> dict:
    """Extract JSON from raw text, removing markdown codeblocks if present."""
    text = raw.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def generate_story_with_llm(
    topic: str,
    locale: str = "uk",
    style: str = "cinematic",
    api_url: str = "http://localhost:11434/v1/chat/completions",
    model: str = "llama3",
    api_key: Optional[str] = None,
    timeout: int = 45,
) -> StoryPlan:
    """Generate a structured story plan using an OpenAI-compatible LLM endpoint."""
    system_prompt = SYSTEM_PROMPT_UK if locale == "uk" else SYSTEM_PROMPT_RU
    user_prompt = f"Тема ролика: {topic}. Стиль візуалу: {style}."

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 1500,
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        result = json.loads(body)
        raw_content = result["choices"][0]["message"]["content"]

    data = _extract_json(raw_content)
    scenes = [
        StoryScene(
            text=s["text"],
            visual_description=s.get("visual_description", ""),
            image_prompt=s.get("image_prompt", enhance_prompt(s.get("visual_description", topic), style)["prompt"]),
        )
        for s in data["scenes"]
    ]

    return StoryPlan(
        title=data.get("title", topic),
        locale=locale,
        topic=topic,
        style=style,
        scenes=scenes,
    )


def generate_offline_story(
    topic: str,
    locale: str = "uk",
    style: str = "cinematic",
) -> StoryPlan:
    """Robust offline parametric story builder (zero network requirements)."""
    clean_topic = topic.strip()
    latin_topic = to_latin_subject(clean_topic)
    if locale == "uk":
        title = f"Таємниця: {clean_topic}"
        scenes = [
            StoryScene(
                text=f"Чи замислювалися ви коли-небудь, що насправді приховує історія про {clean_topic}? Те, що ми вважали простим, виявилося зовсім іншим.",
                visual_description=f"Таємничий вигляд на {clean_topic} у густому тумані на світанку",
                image_prompt=enhance_prompt(f"Mysterious view of {latin_topic} shrouded in morning fog, dramatic wide angle", style)["prompt"],
            ),
            StoryScene(
                text=f"Дослідники довгий час намагалися розгадати цю загадку. Крок за кроком відкривалися деталі, які повністю змінили уявлення вчених.",
                visual_description=f"Вчені та дослідники вивчають старовинні мапи та сліди {clean_topic}",
                image_prompt=enhance_prompt(f"Historians and archaeologists studying ancient manuscripts and relics of {latin_topic}", style)["prompt"],
            ),
            StoryScene(
                text=f"Сьогодні це відкриття доводить: людство лише починає розуміти велич минулого. А як ви гадаєте, яка таємниця ховається далі?",
                visual_description=f"Величний захід сонця над місцем подій {clean_topic}, епічна панорама",
                image_prompt=enhance_prompt(f"Majestic golden hour sunset panorama over {latin_topic}, breathtaking perspective, 8k", style)["prompt"],
            ),
        ]
    else:
        title = f"Тайна: {clean_topic}"
        scenes = [
            StoryScene(
                text=f"Задумывались ли вы, что на самом деле скрывает история про {clean_topic}? То, к чему мы привыкли, оказалось лишь вершиной айсберга.",
                visual_description=f"Загадочный вид на {clean_topic} в предрассветном тумане",
                image_prompt=enhance_prompt(f"Mysterious view of {latin_topic} shrouded in morning fog, dramatic wide angle", style)["prompt"],
            ),
            StoryScene(
                text=f"Исследователи годами пытались разгадать эту загадку. Шаг за шагом находились свидетельства, перевернувшие привычные теории.",
                visual_description=f"Учёные и исследователи изучают древние артефакты и рукописи {clean_topic}",
                image_prompt=enhance_prompt(f"Historians and archaeologists studying ancient manuscripts and relics of {latin_topic}", style)["prompt"],
            ),
            StoryScene(
                text=f"Сегодня эта находка доказывает: мир хранит ещё сотни неразгаданных тайн. А что об этом думаете вы?",
                visual_description=f"Эпический закат над местом событий {clean_topic}, монументальный вид",
                image_prompt=enhance_prompt(f"Majestic golden hour sunset panorama over {latin_topic}, breathtaking perspective, 8k", style)["prompt"],
            ),
        ]

    return StoryPlan(
        title=title,
        locale=locale,
        topic=clean_topic,
        style=style,
        scenes=scenes,
    )


def generate_story(
    topic: str,
    locale: str = "uk",
    style: str = "cinematic",
    api_url: Optional[str] = None,
    model: str = "llama3",
    api_key: Optional[str] = None,
) -> StoryPlan:
    """Primary high-level story generation entrypoint with automatic offline fallback."""
    if api_url:
        try:
            return generate_story_with_llm(
                topic=topic,
                locale=locale,
                style=style,
                api_url=api_url,
                model=model,
                api_key=api_key,
            )
        except Exception:
            # Fallback to deterministic offline generator on network/LLM error
            pass

    return generate_offline_story(topic=topic, locale=locale, style=style)
