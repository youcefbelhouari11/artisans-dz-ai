# ================================================================
# search_service.py — Artisans DZ / Wilaya de Tiaret
# Compatible avec BDD:
# provider / service / service_category / location
# ================================================================

from sqlalchemy import text
from app.utils.mapping import SERVICE_MAPPING


def build_search_keywords(service: str | None) -> list[str]:
    """Construit la liste de mots-clés à partir du service canonique."""
    if not service:
        return []

    keywords = SERVICE_MAPPING.get(service, [service])
    seen, unique = set(), []

    for kw in keywords:
        kw_norm = str(kw).strip().lower()
        if kw_norm and kw_norm not in seen:
            seen.add(kw_norm)
            unique.append(kw_norm)

    return unique


def build_search_query(
    keywords: list[str],
    commune: str | None,
    filters: dict | None,
):
    filters = filters or {}

    base_query = """
        SELECT
            p.id,
            p.first_name,
            p.last_name,
            p.phone,
            p.bio,
            p.is_available,
            p.is_verified,
            p.rating_average,
            p.experience_years,
            p.trust_score,

            l.city AS city,
            l.city AS commune,
            l.address,

            c.name AS category,

            s.id AS service_id,
            s.title AS service_title,
            s.description AS service_description,
            s.price,
            s.currency
        FROM provider p
        JOIN service s
            ON s.provider_id = p.id
        JOIN service_category c
            ON c.id = s.category_id
        JOIN location l
            ON l.id = p.location_id
        WHERE p.status = 'ACTIVE'
          AND s.is_active = TRUE
          AND s.deleted = FALSE
    """

    params = {}

    # ── Service keywords ─────────────────────────────────────────
    if keywords:
        conditions = []
        for i, kw in enumerate(keywords):
            conditions.append(
                f"""
                (
                    LOWER(c.name) LIKE LOWER(:kw{i})
                    OR LOWER(s.title) LIKE LOWER(:kw{i})
                    OR LOWER(s.description) LIKE LOWER(:kw{i})
                )
                """
            )
            params[f"kw{i}"] = f"%{kw}%"

        base_query += " AND (" + " OR ".join(conditions) + ")"

    # ── Commune / city ───────────────────────────────────────────
    if commune:
        base_query += " AND LOWER(l.city) LIKE LOWER(:commune)"
        params["commune"] = f"%{commune.strip().lower()}%"

    # ── Optional filters ─────────────────────────────────────────
    if filters.get("rating_min") is not None:
        base_query += " AND COALESCE(p.rating_average, 0) >= :rating_min"
        params["rating_min"] = filters["rating_min"]

    if filters.get("experience_min") is not None:
        base_query += " AND COALESCE(p.experience_years, 0) >= :experience_min"
        params["experience_min"] = filters["experience_min"]

    if filters.get("price_max") is not None:
        base_query += " AND COALESCE(s.price, 0) <= :price_max"
        params["price_max"] = filters["price_max"]

    if filters.get("available_only"):
        base_query += " AND p.is_available = TRUE"

    # ── Sorting ──────────────────────────────────────────────────
    sort_by = filters.get("sort_by")

    if sort_by in ("experience", "experience_desc"):
        base_query += """
            ORDER BY
                COALESCE(p.experience_years, 0) DESC,
                COALESCE(p.rating_average, 0) DESC
        """

    elif sort_by in ("rating", "rating_desc"):
        base_query += """
            ORDER BY
                COALESCE(p.rating_average, 0) DESC,
                COALESCE(p.experience_years, 0) DESC
        """

    elif sort_by in ("price", "price_asc"):
        base_query += """
            ORDER BY
                COALESCE(s.price, 999999) ASC,
                COALESCE(p.rating_average, 0) DESC
        """

    else:
        base_query += """
            ORDER BY
                p.is_available DESC,
                p.is_verified DESC,
                COALESCE(p.rating_average, 0) DESC,
                COALESCE(p.trust_score, 0) DESC,
                COALESCE(p.experience_years, 0) DESC,
                COALESCE(s.price, 999999) ASC
        """

    base_query += " LIMIT :limit"
    params["limit"] = int(filters.get("limit", 5) or 5)

    return text(base_query), params


def search_providers(
    db,
    service: str | None,
    city: str | None,
    filters: dict | None = None,
) -> list[dict]:
    keywords = build_search_keywords(service)
    query, params = build_search_query(keywords, city, filters)
    result = db.execute(query, params)
    return [dict(row._mapping) for row in result]


def search_only_by_service(
    db,
    service: str,
    filters: dict | None = None,
) -> list[str]:
    keywords = build_search_keywords(service)
    filters = filters or {}

    if not keywords:
        return []

    conditions = []
    params = {}

    for i, kw in enumerate(keywords):
        conditions.append(
            f"""
            (
                LOWER(c.name) LIKE LOWER(:kw{i})
                OR LOWER(s.title) LIKE LOWER(:kw{i})
                OR LOWER(s.description) LIKE LOWER(:kw{i})
            )
            """
        )
        params[f"kw{i}"] = f"%{kw}%"

    sql = f"""
        SELECT DISTINCT LOWER(l.city) AS commune
        FROM provider p
        JOIN service s
            ON s.provider_id = p.id
        JOIN service_category c
            ON c.id = s.category_id
        JOIN location l
            ON l.id = p.location_id
        WHERE p.status = 'ACTIVE'
          AND s.is_active = TRUE
          AND s.deleted = FALSE
          AND ({' OR '.join(conditions)})
        ORDER BY commune
    """

    result = db.execute(text(sql), params)
    return [row.commune for row in result if row.commune]


def search_only_by_commune(db, commune: str) -> list[str]:
    sql = """
        SELECT DISTINCT LOWER(c.name) AS category
        FROM provider p
        JOIN service s
            ON s.provider_id = p.id
        JOIN service_category c
            ON c.id = s.category_id
        JOIN location l
            ON l.id = p.location_id
        WHERE p.status = 'ACTIVE'
          AND s.is_active = TRUE
          AND s.deleted = FALSE
          AND LOWER(l.city) LIKE LOWER(:commune)
        ORDER BY category
    """

    result = db.execute(
        text(sql),
        {"commune": f"%{commune.strip().lower()}%"},
    )

    return [row.category for row in result if row.category]