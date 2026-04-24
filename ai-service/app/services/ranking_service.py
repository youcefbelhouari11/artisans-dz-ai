# ================================================================
# ranking_service.py — Artisans DZ / Wilaya de Tiaret
# Score normalisé : rating, expérience, trust, disponibilité, prix
# ================================================================


def _normalize(value: float, min_val: float, max_val: float) -> float:
    """Ramène une valeur entre 0 et 1."""
    if max_val == min_val:
        return 0.0
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))


def compute_provider_score(provider: dict, price_min: float = 500, price_max: float = 50000) -> float:
    """
    Score composite normalisé sur 100.

    Poids :
      45 % → rating        (0–5 → normalisé 0–1)
      20 % → expérience    (0–20 ans → normalisé 0–1)
      20 % → trust_score   (0–100 → normalisé 0–1)
      10 % → disponibilité (0 ou 1)
       5 % → prix compétitif (inversé : moins cher = meilleur)
    """
    rating     = float(provider.get("rating_average", 0) or 0)
    experience = float(provider.get("experience_years", 0) or 0)
    trust      = float(provider.get("trust_score", 0) or 0)
    available  = 1.0 if provider.get("is_available", False) else 0.0
    verified   = 1.0 if provider.get("is_verified", False) else 0.0
    price      = provider.get("price")

    # Normalisation
    r_norm   = _normalize(rating,     0.0, 5.0)
    exp_norm = _normalize(experience, 0.0, 20.0)
    t_norm   = _normalize(trust,      0.0, 100.0)

    # Prix : inversé (prix bas = meilleur score)
    if price and price > 0:
        p_norm = 1.0 - _normalize(float(price), price_min, price_max)
    else:
        p_norm = 0.5  # neutre si prix inconnu

    # Bonus vérifié (léger)
    verified_bonus = verified * 0.05

    score = (
        r_norm   * 0.45 +
        exp_norm * 0.20 +
        t_norm   * 0.20 +
        available * 0.10 +
        p_norm   * 0.05 +
        verified_bonus
    ) * 100  # ramène sur 100

    return round(score, 2)


def attach_scores(providers: list[dict]) -> list[dict]:
    """Calcule et attache le score à chaque prestataire."""
    # Calcule price_min/max sur la liste pour normalisation relative
    prices = [p.get("price") for p in providers if p.get("price") and p["price"] > 0]
    p_min = min(prices) if prices else 500
    p_max = max(prices) if prices else 50000

    for provider in providers:
        provider["score"] = compute_provider_score(provider, p_min, p_max)
    return providers


def sort_providers(providers: list[dict], filters: dict | None = None) -> list[dict]:
    """Tri selon le filtre demandé ou par score composite."""
    filters  = filters or {}
    sort_by  = filters.get("sort_by")

    if sort_by == "experience":
        return sorted(
            providers,
            key=lambda x: (
                x.get("experience_years", 0) or 0,
                x.get("rating_average", 0) or 0,
            ),
            reverse=True,
        )

    if sort_by == "rating":
        return sorted(
            providers,
            key=lambda x: (
                x.get("rating_average", 0) or 0,
                x.get("experience_years", 0) or 0,
            ),
            reverse=True,
        )

    if sort_by == "price":
        return sorted(
            providers,
            key=lambda x: (
                float(x["price"]) if x.get("price") is not None else float("inf"),
                -(x.get("rating_average", 0) or 0),
            ),
        )

    # Tri par défaut : score composite
    return sorted(
        providers,
        key=lambda x: x.get("score", 0) or 0,
        reverse=True,
    )


def rank_providers(providers: list[dict], filters: dict | None = None) -> list[dict]:
    """Point d'entrée principal : score + tri."""
    providers = attach_scores(providers)
    providers = sort_providers(providers, filters)
    return providers


def get_best_provider(providers: list[dict]) -> dict | None:
    """Retourne le meilleur prestataire (premier après ranking)."""
    return providers[0] if providers else None