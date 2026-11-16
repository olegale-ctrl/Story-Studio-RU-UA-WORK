"""Visual prompt builder for Story Studio RU/UA.

Enhances scene descriptions with style triggers, lighting, and camera directives
for AI image generators (Flux, SDXL, Midjourney, ComfyUI).
"""
from __future__ import annotations

from typing import Dict

STYLES: Dict[str, Dict[str, str]] = {
    "cinematic": {
        "name": "Кинематографический реализм / Кінематографічний реалізм",
        "prefix": "Cinematic 35mm photograph,",
        "suffix": "dramatic directional lighting, depth of field, photorealistic, 8k resolution, volumetric atmospheric haze, highly detailed texture",
        "negative": "cartoon, illustration, 3d render, deformed, blurry, low quality, oversaturated",
    },
    "historical": {
        "name": "Историческое полотно / Історичне полотно",
        "prefix": "Detailed historical painting in the style of 19th century masters,",
        "suffix": "authentic period garments, atmospheric Rembrandt lighting, rich color palette, oil on canvas texture, museum quality",
        "negative": "modern clothing, futuristic, plastic, anime, text, watermark, signature",
    },
    "dark_mystery": {
        "name": "Тёмный нуар и мистика / Темний нуар і містика",
        "prefix": "Moody dark noir scene,",
        "suffix": "heavy fog, silhouette backlight, low key lighting, high contrast, eerie cinematic tension, cinematic color grading",
        "negative": "bright, sunny, cheerful, cartoon, lowres, flat lighting",
    },
    "anime_epic": {
        "name": "Эпическая анимация / Епічна анімація",
        "prefix": "High quality anime feature film still, Makoto Shinkai aesthetic,",
        "suffix": "breathtaking lighting, glowing particles, detailed background scenery, beautiful sky, cinematic composition",
        "negative": "western comic, 3d render, live action photo, bad anatomy, lowres",
    },
}


def enhance_prompt(
    scene_description: str,
    style: str = "cinematic",
    aspect_ratio: str = "16:9",
    character_anchor: str = "",
) -> Dict[str, str]:
    """Build positive and negative prompts tailored for the chosen style."""
    style_info = STYLES.get(style, STYLES["cinematic"])
    prefix = style_info["prefix"]
    suffix = style_info["suffix"]
    negative = style_info["negative"]

    core_parts = []
    if character_anchor.strip():
        core_parts.append(character_anchor.strip())
    core_parts.append(scene_description.strip())

    ar_tag = f"--ar {aspect_ratio}" if aspect_ratio in ("16:9", "9:16", "1:1") else ""
    full_positive = f"{prefix} {', '.join(core_parts)}, {suffix} {ar_tag}".strip()

    return {
        "prompt": full_positive,
        "negative_prompt": negative,
        "style": style,
        "aspect_ratio": aspect_ratio,
    }
