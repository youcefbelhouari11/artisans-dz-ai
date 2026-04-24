# ================================================================
# catalog_service.py — Artisans DZ / Wilaya de Tiaret
# Lit les communes et services depuis la DB (fallback static)
# ================================================================

from sqlalchemy import text
from app.utils.mapping import COMMUNE_MAPPING, SERVICE_MAPPING

# ── Fallback static ─────────────────────────────────────────────
STATIC_SERVICES = list(SERVICE_MAPPING.keys())

STATIC_COMMUNES = [
    "tiaret", "sougueur", "frenda", "mahdia", "rahouia",
    "ksar chellala", "ain deheb", "dahmouni", "guertoufa",
    "hamadia", "takhemaret", "ain bouchekif",
]


def get_service_catalog(db=None) -> list[str]:
    """Retourne les catégories de service depuis la DB."""
    if db is None:
        return STATIC_SERVICES
    try:
        result = db.execute(
            text("SELECT LOWER(name) AS name FROM service_category ORDER BY name")
        )
        rows = [row.name for row in result if row.name]
        return rows or STATIC_SERVICES
    except Exception:
        return STATIC_SERVICES


def get_commune_catalog(db=None) -> list[str]:
    """
    Retourne les communes de Tiaret depuis la table `commune`.
    Fallback sur STATIC_COMMUNES si la table est absente.
    """
    if db is None:
        return STATIC_COMMUNES
    try:
        result = db.execute(
            text("SELECT LOWER(name) AS name FROM commune ORDER BY name")
        )
        rows = [row.name for row in result if row.name]
        return rows or STATIC_COMMUNES
    except Exception:
        return STATIC_COMMUNES


def get_city_catalog(db=None) -> list[str]:
    """
    Compatibilité ascendante — renvoie les communes.
    Essaie d'abord la table `commune`, puis `location`.
    """
    communes = get_commune_catalog(db)
    if communes:
        return communes

    if db is None:
        return STATIC_COMMUNES
    try:
        result = db.execute(
            text(
                "SELECT DISTINCT LOWER(city) AS city "
                "FROM location WHERE city IS NOT NULL ORDER BY city"
            )
        )
        rows = [row.city for row in result if row.city]
        return rows or STATIC_COMMUNES
    except Exception:
        return STATIC_COMMUNES


def get_services_in_commune(db, commune: str) -> list[str]:
    """
    Retourne la liste des catégories de services
    disponibles dans une commune donnée.
    """
    try:
        result = db.execute(
            text("""
                SELECT DISTINCT LOWER(sc.name) AS category
                FROM provider p
                JOIN location l  ON l.id  = p.location_id
                JOIN service s   ON s.provider_id = p.id
                JOIN service_category sc ON sc.id = s.category_id
                WHERE LOWER(l.city) LIKE LOWER(:commune)
                  AND p.status = 'ACTIVE'
                  AND s.is_active = TRUE
                ORDER BY category
            """),
            {"commune": f"%{commune.strip().lower()}%"}
        )
        return [row.category for row in result if row.category]
    except Exception:
        return []


def get_communes_for_service(db, service_keyword: str) -> list[str]:
    """
    Retourne les communes qui ont au moins un prestataire
    actif pour un service donné.
    """
    try:
        result = db.execute(
            text("""
                SELECT DISTINCT LOWER(l.city) AS commune
                FROM provider p
                JOIN location l  ON l.id  = p.location_id
                JOIN service s   ON s.provider_id = p.id
                JOIN service_category sc ON sc.id = s.category_id
                WHERE LOWER(sc.name) LIKE LOWER(:kw)
                  AND p.status = 'ACTIVE'
                  AND s.is_active = TRUE
                ORDER BY commune
            """),
            {"kw": f"%{service_keyword.strip().lower()}%"}
        )
        return [row.commune for row in result if row.commune]
    except Exception:
        return []