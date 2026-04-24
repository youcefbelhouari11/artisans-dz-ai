# ================================================================
# memory_service.py
# Fix: commune/city unified | last_best_provider | general question isolation
# ================================================================

import time
import copy

MEMORY_TTL_SECONDS  = 1800
MAX_HISTORY_MESSAGES = 8

SESSION_MEMORY  = {}
SESSION_HISTORY = {}


def default_memory() -> dict:
    return {
        "service":            None,
        "commune":            None,   # ← champ unifié (plus de city/commune dual)
        "category":           None,
        "language":           None,
        "filters": {
            "rating_min":     None,
            "experience_min": None,
            "sort_by":        None,
            "price_max":      None,
            "available_only": False,
        },
        "last_best_provider": None,   # ← prestataire recommandé → follow-up questions
        "_updated_at":        time.time(),
    }


def cleanup_expired_sessions():
    now  = time.time()
    dead = [
        sid for sid, data in SESSION_MEMORY.items()
        if now - data.get("_updated_at", now) > MEMORY_TTL_SECONDS
    ]
    for sid in dead:
        SESSION_MEMORY.pop(sid, None)
        SESSION_HISTORY.pop(sid, None)


def get_memory(session_id: str) -> dict:
    cleanup_expired_sessions()
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = default_memory()
    if session_id not in SESSION_HISTORY:
        SESSION_HISTORY[session_id] = []
    SESSION_MEMORY[session_id]["_updated_at"] = time.time()
    return SESSION_MEMORY[session_id]


def get_history(session_id: str) -> list[dict]:
    if session_id not in SESSION_HISTORY:
        SESSION_HISTORY[session_id] = []
    return SESSION_HISTORY[session_id]


def append_history(session_id: str, role: str, content: str):
    history = get_history(session_id)
    history.append({"role": role, "content": content, "timestamp": time.time()})
    if len(history) > MAX_HISTORY_MESSAGES:
        SESSION_HISTORY[session_id] = history[-MAX_HISTORY_MESSAGES:]


def merge_with_memory(intent: dict, memory: dict) -> dict:
    """
    Fusionne intent + memory.
    FIX: commune/city unified | n'écrase PAS les questions générales
    """
    merged = intent.copy()

    # FIX: unifie commune et city dans l'intent
    if not merged.get("commune") and merged.get("city"):
        merged["commune"] = merged["city"]
    if not merged.get("city") and merged.get("commune"):
        merged["city"] = merged["commune"]

    # Ne fusionne le contexte mémoire QUE pour search/provider_question
    if merged.get("type") in ("search", "provider_question"):

        if not merged.get("service"):
            merged["service"] = memory.get("service")

        if not merged.get("commune"):
            merged["commune"] = memory.get("commune")
            merged["city"]    = memory.get("commune")

        if not merged.get("category"):
            merged["category"] = memory.get("category")

        if not merged.get("language"):
            merged["language"] = memory.get("language")

        cur_f = merged.get("filters") or {}
        mem_f = memory.get("filters") or {}
        merged["filters"] = {
            "rating_min":     cur_f.get("rating_min")     if cur_f.get("rating_min")     is not None else mem_f.get("rating_min"),
            "experience_min": cur_f.get("experience_min") if cur_f.get("experience_min") is not None else mem_f.get("experience_min"),
            "sort_by":        cur_f.get("sort_by")        or mem_f.get("sort_by"),
            "price_max":      cur_f.get("price_max")      if cur_f.get("price_max")      is not None else mem_f.get("price_max"),
            "available_only": cur_f.get("available_only") if cur_f.get("available_only") is not None else mem_f.get("available_only", False),
        }

    return merged


def save_memory(intent: dict, memory: dict, best_provider: dict | None = None):
    """
    Sauvegarde le contexte de recherche + last_best_provider.
    FIX: commune/city unified
    """
    if intent.get("type") == "search":
        commune = intent.get("commune") or intent.get("city")
        memory["service"]  = intent.get("service")
        memory["commune"]  = commune
        memory["category"] = intent.get("category")
        memory["language"] = intent.get("language")
        memory["filters"]  = intent.get("filters", {})

    if best_provider:
        # FIX: normalise commune dans le provider avant de sauvegarder
        provider_copy = copy.deepcopy(best_provider)
        if not provider_copy.get("commune") and provider_copy.get("city"):
            provider_copy["commune"] = provider_copy["city"]
        elif not provider_copy.get("city") and provider_copy.get("commune"):
            provider_copy["city"] = provider_copy["commune"]
        memory["last_best_provider"] = provider_copy

    memory["_updated_at"] = time.time()