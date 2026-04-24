# ================================================================
# filter_service.py — FINAL FIXED
# ================================================================

import re
from app.utils.text import normalize_text


def extract_filters(text: str) -> dict:
    normalized = normalize_text(text or "")

    filters = {
        "rating_min":     None,
        "experience_min": None,
        "sort_by":        None,
        "price_max":      None,
        "available_only": False,
    }

    # ── BEST / TOP RATED ─────────────────────────────────────────
    if any(w in normalized for w in [
        "best", "top", "top rated", "best rated",
        "meilleur", "mieux note", "mieux note", "top note",
        "الافضل", "افضل", "مليح", "الاحسن", "احسن واحد",
        "كبير", "قيمة مليحة",
    ]):
        filters["sort_by"] = "rating_desc"

    # ── CHEAP / LOW PRICE ────────────────────────────────────────
    if any(w in normalized for w in [
        "cheap", "affordable", "low price", "less expensive",
        "pas cher", "moins cher", "abordable", "economique",
        "رخيص", "الارخص", "اقل سعر", "اقل ثمن", "اقتصادي",
        "بالرخيص", "ارخص واحد", "بسيط", "في الميزانية",
    ]):
        if not filters["sort_by"]:
            filters["sort_by"] = "price_asc"

    # ── EXPERIENCED ──────────────────────────────────────────────
    if any(w in normalized for w in [
        "experienced", "expert", "professional", "senior",
        "experimente", "experimente", "professionnel", "expert",
        "عندو خبرة", "خبرة", "محترف", "متمرس", "قديم",
        "خبير", "عندو باكراوند", "شاطر",
    ]):
        filters["experience_min"] = 5
        if not filters["sort_by"]:
            filters["sort_by"] = "experience_desc"

    # ── AVAILABLE ONLY ───────────────────────────────────────────
    if any(w in normalized for w in [
        "available", "available now", "disponible", "dispo",
        "متوفر", "متوفر الان", "حاضر", "خدام", "ديسبو",
        "يخدم الان", "حاضر الان", "يقدر يجي اليوم",
    ]):
        filters["available_only"] = True

    # ── HIGH RATING MIN ──────────────────────────────────────────
    if any(w in normalized for w in [
        "well rated", "good rating",
        "bien note", "bien note",
        "تقييم مليح", "تقييم جيد", "عندو تقييم",
    ]):
        filters["rating_min"] = 4.0

    # ── PRICE CAPS — détection numérique ─────────────────────────
    # "moins de 3000" / "اقل من 5000" / "under 2000"
    price_match = re.search(
        r"(?:moins de|under|below|اقل من|اقل|تحت)\s+(\d+)",
        normalized
    )
    if price_match:
        filters["price_max"] = int(price_match.group(1))

    # "بحدود 3000 دج" / "environ 2000"
    approx_match = re.search(
        r"(?:بحدود|حوالي|environ|around|about)\s+(\d+)",
        normalized
    )
    if approx_match and not filters["price_max"]:
        filters["price_max"] = int(approx_match.group(1)) + 500

    return filters