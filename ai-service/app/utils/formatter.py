# ================================================================
# formatter.py — FINAL FIXED
# FIX: keeps emojis, phones, markdown, line breaks — no truncation
# ================================================================

import re


def format_reply(text: str) -> str:
    """
    Formattage SÉCURISÉ — ne supprime rien d'important.
    - garde les emojis
    - garde les numéros de téléphone
    - garde les prix (1800 DZD)
    - garde les sauts de ligne (structure bullet points)
    - garde le markdown léger (** gras)
    - supprime uniquement les espaces multiples et lignes vides excessives
    """
    if not text:
        return ""

    # Normalise les retours à la ligne
    text = str(text).replace("\r\n", "\n").replace("\r", "\n")

    lines = []
    for line in text.split("\n"):
        # Supprime uniquement les espaces en double dans une ligne
        line = re.sub(r"[ \t]+", " ", line).strip()
        lines.append(line)

    # Supprime les lignes vides consécutives (max 1)
    cleaned = []
    prev_empty = False
    for line in lines:
        if line == "":
            if not prev_empty:
                cleaned.append(line)
            prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False

    result = "\n".join(cleaned).strip()
    return result


def build_no_results_message(language: str) -> str:
    if language == "ar":
        return "ما لقيناش نتائج 😔"
    if language == "fr":
        return "Aucun résultat 😔"
    return "No results 😔"