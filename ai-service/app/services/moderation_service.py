# ================================================================
# moderation_service.py — Artisans DZ / Wilaya de Tiaret
# Modération : abuse → block | négatif → guide | problème → aide
# ================================================================

import re

# ── MOTS D'ABUS (block immédiat) ────────────────────────────────
BAD_WORDS_AR = {
    "غبي", "حمار", "كلب",   "متخلف",  "سافل",
      "خنزير", "حيوان",
     
}
BAD_WORDS_FR = {
    "idiot", "stupide", "imbecile", "con", "connard", 
   "abruti", "salaud", "batard", "fils de pute",
    "va te faire", "enculé", "crétin", "naze",
}
BAD_WORDS_EN = {
    "idiot", "stupid", "dumb", "asshole",
    "moron", "crap", "loser",
}

# ── MOTS NÉGATIFS (warning + aide à reformuler) ─────────────────
NEGATIVE_WORDS_AR = {
    "سيء", "رديء", "احتيال", "محتال", "نصاب", "سرق", "خدع",
    "ماعجبنيش", "ما عجبنيش", "ما عجبنيش", "غلط", "مشكلة",
    "ضاع فلوسي", "ما خدم", "ما كمل", "خيّب",
}
NEGATIVE_WORDS_FR = {
    "mauvais", "arnaque", "escroc", "voleur", "fake", "nul",
    "pas serieux", "pas sérieux", "déçu", "problème",
    "n'a pas fini", "incompétent", "nul",
}
NEGATIVE_WORDS_EN = {
    "bad", "fake", "scam", "fraud", "thief", "poor",
    "not serious", "disappointed", "issue", "problem",
    "didn't finish", "incompetent",
}

NEGATIVE_PATTERNS = [
    r"هذا\s+عامل\s+سيء", r"عامل\s+سيء", r"خدمة\s+سيئة",
    r"هذا\s+نصاب", r"هذا\s+محتال", r"ما\s+خدم\s+مليح",
    r"pas\s+s[eé]rieux", r"tr[eè]s\s+mauvais", r"pas\s+bien\s+fait",
    r"not\s+serious", r"very\s+bad", r"didn'?t\s+do\s+the\s+job",
]

# ── PATTERNS PROBLÈMES TECHNIQUES (aide directe) ────────────────
# Si l'user décrit un problème concret → intent "problem_description"
PROBLEM_PATTERNS = {
    "plumber": [
        r"تسرب", r"فيضان", r"مياه", r"حنفية.*تقطر", r"أنبوب.*مكسور",
        r"wc.*مسدود", r"بالوعة.*مسدودة", r"ماء.*يقطر",
        r"fuite", r"tuyau.*cassé", r"wc.*bouché", r"lavabo.*bouché",
        r"robinet.*coule", r"inondation",
        r"leak", r"pipe.*broken", r"toilet.*clogged", r"water.*dripping",
    ],
    "electrician": [
        r"كهرباء.*مقطوعة", r"تيار.*منقطع", r"شورط", r"مصباح.*ما.*يضيء",
        r"قاطع.*يقطع", r"حريق.*كهربائي",
        r"panne.*électrique", r"court.circuit", r"lampe.*ne.*marche",
        r"disjoncteur.*saute", r"pas.*courant",
        r"power.*out", r"short.*circuit", r"bulb.*not.*working",
    ],
    "mason": [
        r"شقوق.*جدار", r"جدار.*متشقق", r"سقف.*يتسرب",
        r"fissure.*mur", r"mur.*lézardé", r"plafond.*fuit",
        r"wall.*crack", r"ceiling.*leak",
    ],
    "painter": [
        r"طلاء.*يتقشر", r"جدار.*ملوث",
        r"peinture.*s.écaille", r"mur.*taché",
        r"paint.*peeling", r"wall.*stained",
    ],
    "climatisation": [
        r"مكيف.*ما.*يبرد", r"مكيف.*يشتغل.*بلا.*هواء",
        r"clim.*ne.*refroidit", r"climatiseur.*panne",
        r"ac.*not.*cooling", r"air.*conditioner.*broken",
    ],
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _words(text: str) -> set:
    return set(re.findall(r"\w+", text, flags=re.UNICODE))


def contains_abuse(text: str) -> bool:
    t, w = _normalize(text), _words(_normalize(text))
    return bool(w & BAD_WORDS_AR or w & BAD_WORDS_FR or w & BAD_WORDS_EN)


def contains_negative(text: str) -> bool:
    t, w = _normalize(text), _words(_normalize(text))
    if w & NEGATIVE_WORDS_AR or w & NEGATIVE_WORDS_FR or w & NEGATIVE_WORDS_EN:
        return True
    return any(re.search(p, t, re.IGNORECASE) for p in NEGATIVE_PATTERNS)


def detect_problem_type(text: str) -> str | None:
    """
    Détecte si l'utilisateur décrit un problème concret
    et retourne le type de service adapté.
    """
    t = _normalize(text)
    for service, patterns in PROBLEM_PATTERNS.items():
        if any(re.search(p, t, re.IGNORECASE) for p in patterns):
            return service
    return None


def moderate_user_input(text: str, language: str = "fr") -> dict:
    lang = language if language in ("ar", "fr", "en") else "fr"

    # ── 1. Abus → blocage ───────────────────────────────────────
    if contains_abuse(text):
        return {
            "blocked": True,
            "reason":  "abuse",
            "message": {
                "ar": "⚠️ الرجاء استعمال لغة محترمة حتى نقدر نساعدك.",
                "fr": "⚠️ Merci d'utiliser un langage respectueux pour que je puisse vous aider.",
                "en": "⚠️ Please use respectful language so I can help you.",
            }[lang],
            "problem_type": None,
        }

    # ── 2. Problème concret → aide directe ──────────────────────
    problem_type = detect_problem_type(text)
    if problem_type:
        return {
            "blocked":      False,
            "reason":       "problem_description",
            "problem_type": problem_type,
            "message":      None,
        }

    # ── 3. Feedback négatif → guide ─────────────────────────────
    if contains_negative(text):
        return {
            "blocked": False,
            "reason":  "negative",
            "message": {
                "ar": "💬 فهمت أن عندك تجربة سلبية. نقدر نساعدك تلقى عامل أحسن أو تقدم شكوى رسمية.",
                "fr": "💬 Je comprends que vous avez eu une mauvaise expérience. Je peux vous aider à trouver un meilleur prestataire ou à déposer une réclamation.",
                "en": "💬 I understand you had a bad experience. I can help you find a better provider or submit a complaint.",
            }[lang],
            "problem_type": None,
        }

    return {"blocked": False, "reason": None, "message": None, "problem_type": None}