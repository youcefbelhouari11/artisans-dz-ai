def build_provider_explanation(provider: dict, language: str = "fr") -> str:
    name = f"{provider.get('first_name', '')} {provider.get('last_name', '')}".strip()
    commune = provider.get("commune") or provider.get("city") or "—"
    rating = provider.get("rating_average") or 0
    exp = provider.get("experience_years") or 0
    price = provider.get("price")
    available = provider.get("is_available", False)

    parts = []

    # rating
    if rating >= 4.5:
        parts.append({
            "ar": "⭐ تقييم ممتاز",
            "fr": "⭐ excellente note",
            "en": "⭐ excellent rating",
        }[language])
    elif rating >= 4.0:
        parts.append({
            "ar": "⭐ تقييم جيد",
            "fr": "⭐ bonne note",
            "en": "⭐ good rating",
        }[language])

    # experience
    if exp >= 5:
        parts.append({
            "ar": f"{exp} سنوات خبرة",
            "fr": f"{exp} ans d'expérience",
            "en": f"{exp} years experience",
        }[language])

    # availability
    if available:
        parts.append({
            "ar": "✅ متوفر",
            "fr": "✅ disponible",
            "en": "✅ available",
        }[language])

    # price
    if price:
        parts.append({
            "ar": f"💰 {price} دج",
            "fr": f"💰 {price} DZD",
            "en": f"💰 {price} DZD",
        }[language])

    summary = " | ".join(parts)

    if language == "ar":
        return f"{name} في {commune} — {summary}"
    if language == "fr":
        return f"{name} à {commune} — {summary}"
    return f"{name} in {commune} — {summary}"