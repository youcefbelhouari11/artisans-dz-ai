from sqlalchemy import text


def search_provider_cards(db, category_keywords, city, filters=None, limit=5):
    filters = filters or {}

    sql = """
        SELECT
            p.id,
            p.first_name,
            p.last_name,
            p.rating_average,
            p.experience_years,
            p.is_available,
            p.is_verified,
            p.trust_score,
            l.city,
            c.name AS category,
            s.price
        FROM provider p
        JOIN service s ON s.provider_id = p.id
        JOIN service_category c ON c.id = s.category_id
        JOIN location l ON l.id = p.location_id
        WHERE (
    """

    sql += " OR ".join(
        [f"LOWER(c.name) LIKE LOWER(:kw{i})" for i in range(len(category_keywords))]
    )

    sql += ") AND LOWER(l.city) LIKE LOWER(:city)"

    # ── FILTERS ─────────────────────────────────────────

    if filters.get("rating_min") is not None:
        sql += " AND p.rating_average >= :rating_min"

    if filters.get("experience_min") is not None:
        sql += " AND p.experience_years >= :experience_min"

    if filters.get("price_max") is not None:
        sql += " AND s.price <= :price_max"

    if filters.get("available_only"):
        sql += " AND p.is_available = TRUE"

    # ── SORTING (FIXED) ────────────────────────────────

    sort_by = filters.get("sort_by")

    if sort_by in ("experience", "experience_desc"):
        sql += " ORDER BY p.experience_years DESC, p.rating_average DESC"

    elif sort_by in ("rating", "rating_desc"):
        sql += " ORDER BY p.rating_average DESC, p.experience_years DESC"

    elif sort_by in ("price", "price_asc"):
        sql += " ORDER BY s.price ASC, p.rating_average DESC"

    else:
        sql += " ORDER BY p.rating_average DESC, p.experience_years DESC"

    # ── LIMIT ──────────────────────────────────────────
    sql += " LIMIT :limit"

    params = {f"kw{i}": f"%{kw}%" for i, kw in enumerate(category_keywords)}
    params["city"] = f"%{city}%"
    params["limit"] = limit

    if filters.get("rating_min") is not None:
        params["rating_min"] = filters["rating_min"]

    if filters.get("experience_min") is not None:
        params["experience_min"] = filters["experience_min"]

    if filters.get("price_max") is not None:
        params["price_max"] = filters["price_max"]

    result = db.execute(text(sql), params)
    return [dict(row._mapping) for row in result]