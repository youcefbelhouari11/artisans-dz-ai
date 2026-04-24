import re


def detect_language(text: str) -> str:
    if not text:
        return "fr"

    text_lower = text.lower()

    # 🇦🇷 Arabic detection (strong presence)
    arabic_chars = re.findall(r"[\u0600-\u06FF]", text)
    if len(arabic_chars) >= 2:
        return "ar"

    # 🇫🇷 French keywords (extended)
    french_keywords = [
        "plombier", "électricien", "electricien", "menuisier",
        "peintre", "bonjour", "salut", "merci", "comment",
        "ville", "cher", "pas cher", "expérimenté",
        "prix", "temps", "disponible", "service", "travail",
    ]

    if any(word in text_lower for word in french_keywords):
        return "fr"

    # 🇬🇧 fallback
    return "en"