# ================================================================
# intent_service.py 
# ================================================================

from difflib import get_close_matches

from app.utils.text import normalize_text
from app.utils.language import detect_language
from app.utils.mapping import (
    SERVICE_MAPPING,
    SERVICE_KEYWORDS,
    COMMUNE_MAPPING,
    SERVICE_TO_CATEGORY,
)
from app.services.filter_service import extract_filters


# ── helpers ─────────────────────────────────────────────────────

def _find_exact(text: str, mapping: dict) -> str | None:
    text = normalize_text(text)

    for canonical, variants in mapping.items():
        for variant in variants:
            variant_norm = normalize_text(variant)
            if variant_norm and variant_norm in text:
                return canonical

    return None


def _find_fuzzy(text: str, mapping: dict, cutoff: float = 0.75) -> str | None:
    text = normalize_text(text)
    words = text.split()

    flat = []
    reverse = {}

    for canonical, variants in mapping.items():
        for v in variants:
            v_norm = normalize_text(v)
            if v_norm:
                flat.append(v_norm)
                reverse[v_norm] = canonical

    for word in words:
        matches = get_close_matches(word, flat, n=1, cutoff=cutoff)
        if matches:
            return reverse[matches[0]]

    return None


def _find_by_keywords(text: str, keyword_mapping: dict) -> str | None:
    text = normalize_text(text)

    scores = {}

    for service, keywords in keyword_mapping.items():
        score = 0

        for kw in keywords:
            kw_norm = normalize_text(kw)
            if kw_norm and kw_norm in text:
                # نعطي وزن أكبر للكلمات الطويلة باش نقللو false positives
                score += len(kw_norm)

        if score > 0:
            scores[service] = score

    return max(scores, key=scores.get) if scores else None


def find_service(text: str) -> str | None:
    text = normalize_text(text)

    return (
        _find_exact(text, SERVICE_MAPPING)
        or _find_by_keywords(text, SERVICE_KEYWORDS)
        or _find_fuzzy(text, SERVICE_MAPPING, cutoff=0.72)
    )


def find_commune(text: str) -> str | None:
    text = normalize_text(text)

    return (
        _find_exact(text, COMMUNE_MAPPING)
        or _find_fuzzy(text, COMMUNE_MAPPING, cutoff=0.70)
    )


# ── PROVIDER QUESTIONS ──────────────────────────────────────────

PROVIDER_QUESTION_PATTERNS = {
    "duration": [
        "كم يحتاج", "كم من الوقت", "كم يستغرق", "مدة", "شحال من وقت",
        "باش يخلص", "في قداش يكمل", "وقت العمل", "قداه وقت",
        "combien de temps", "durée", "temps de travail",
        "how long", "time needed", "duration", "how much time"
    ],

    "price": [
        "كم يكلف", "قداش يكلف", "كم السعر", "السعر", "الثمن",
        "قداش", "شحال", "بقداه", "السومة", "كم يدير",
        "combien ça coûte", "combien ca coute", "prix", "tarif", "coût", "cout",
        "how much", "price", "cost", "how much does it cost"
    ],

    "quality": [
        "هل هو مليح", "واش مليح", "هل جيد", "التقييم",
        "واش رايك فيه", "هل يستاهل", "خدمتو مليحة", "موثوق",
        "avis", "rating", "qualité", "qualite", "est-il bon", "est il bon",
        "is he good", "review", "is he reliable", "reliable"
    ],

    "contact": [
        "كيف نتواصل", "كيف اتواصل", "كيف نكلمه", "كيف نتصل",
        "رقمه", "رقم", "هاتف", "تيليفون", "تليفون", "عطيني رقم",
        "كيف نعيطلو", "نحب نتصل بيه", "كيف نلقاه", "تواصل",
        "comment le contacter", "contacter", "contact",
        "numéro", "numero", "telephone", "téléphone", "joindre",
        "how to contact", "contact him", "contact her",
        "phone", "phone number", "number", "call him", "call her"
    ],

    "availability": [
        "هل متوفر", "واش متوفر", "متوفر", "متاح", "خدام", "ديسبو",
        "يخدم اليوم", "يقدر يجي", "راه يخدم", "يجي اليوم",
        "disponible", "available", "est-il disponible", "est il disponible",
        "is he available", "available now", "can he come"
    ],

    "proximity": [
        "قريب مني", "قريب", "في الحومة", "في بلاصتي",
        "près de moi", "pres de moi", "proche", "à proximité", "a proximite",
        "near me", "close to me", "nearby"
    ],

    "work_method": [
        "كيف يخدم", "طريقة عمله", "كيفاش يخدم",
        "واش يدير بالضبط", "كيف يشتغل", "طريقة الخدمة",
        "comment il travaille", "méthode de travail", "methode de travail",
        "how does he work", "work process", "how he works"
    ],

    "complaints": [
        "عنده مشكلة", "شكاوي", "كاين شكاوي",
        "ناس تشكي عليه", "مشاكل مع الزبائن",
        "complaints", "problems", "issues",
        "bad reviews", "any complaints"
    ],

    "experience": [
        "كم عنده خبرة", "سنوات خبرة", "شحال خدم", "عندو خبرة",
        "expérience", "experience", "années d'expérience", "annees experience",
        "how many years", "years of experience"
    ],

    "comparison": [
        "وش الأفضل", "من خير", "قارنلي", "الأفضل", "احسن واحد",
        "le meilleur", "compare", "comparaison",
        "which is better", "best one", "who is better"
    ],
}


def detect_provider_question(text: str) -> str | None:
    normalized = normalize_text(text)

    for q_type, patterns in PROVIDER_QUESTION_PATTERNS.items():
        for pattern in patterns:
            pattern_norm = normalize_text(pattern)
            if pattern_norm and pattern_norm in normalized:
                return q_type

    return None


# ── BUILD INTENT ────────────────────────────────────────────────

def build_intent(
    user_input: str,
    service: str | None,
    commune: str | None,
    language: str,
    filters: dict,
    provider_question: str | None = None,
) -> dict:
    category = SERVICE_TO_CATEGORY.get(service) if service else None

    has_search = bool(
        service
        or commune
        or filters.get("sort_by")
        or filters.get("rating_min") is not None
        or filters.get("experience_min") is not None
        or filters.get("price_max") is not None
        or filters.get("available_only")
    )

    # إذا فيها service/commune/filter نخليها search
    # إذا سؤال فقط على provider نخليها provider_question
    if provider_question and not has_search:
        intent_type = "provider_question"
    elif has_search:
        intent_type = "search"
    else:
        intent_type = "question"

    return {
        "type": intent_type,
        "service": service,
        "city": commune,
        "commune": commune,
        "category": category,
        "language": language,
        "filters": filters,
        "price_max": filters.get("price_max"),
        "provider_question": provider_question,
        "has_service_only": bool(service and not commune),
        "has_commune_only": bool(commune and not service),
    }


def extract_intent(user_input: str, history: list[dict] | None = None) -> dict:
    language = detect_language(user_input)
    normalized = normalize_text(user_input)

    service = find_service(normalized)
    commune = find_commune(normalized)
    filters = extract_filters(user_input)

    provider_question = detect_provider_question(normalized)

    return build_intent(
        user_input=user_input,
        service=service,
        commune=commune,
        language=language,
        filters=filters,
        provider_question=provider_question,
    )