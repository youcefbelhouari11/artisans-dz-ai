import re
import unicodedata


def strip_accents(text: str) -> str:
    if not text:
        return ""

    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def normalize_arabic(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ة": "ه",
        "ى": "ي",
        "ؤ": "و",
        "ئ": "ي",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def reduce_repeated_letters(text: str) -> str:
    if not text:
        return ""

    return re.sub(r"(.)\1{2,}", r"\1\1", text)


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()

    # accents
    text = strip_accents(text)

    # arabic normalization
    text = normalize_arabic(text)

    # ⚠️ FIX: ما نحذفوش "في" ولا "à"
    # نخليهم باش detection يخدم صح

    # reduce repeated letters
    text = reduce_repeated_letters(text)

    # clean special chars
    text = re.sub(r"[^\w\s\u0600-\u06FF-]", " ", text)

    # normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()