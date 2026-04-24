# ================================================================
# chat.py — FINAL FIXED
# ================================================================

import random
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ai_service import (
    generate_general_answer,
    generate_recommendation,
    generate_suggestions,
    stream_general_answer,
    reply_service_only,
    reply_commune_only,
    answer_provider_question,
    reply_problem_description,
)
from app.services.explanation_service import build_provider_explanation
from app.services.moderation_service  import moderate_user_input
from app.services.intent_service      import extract_intent
from app.services.memory_service      import (
    append_history, get_history,
    get_memory, merge_with_memory, save_memory,
)
from app.services.ranking_service import get_best_provider, rank_providers
from app.services.search_service  import (
    search_providers,
    search_only_by_service,
    search_only_by_commune,
)
from app.utils.formatter import format_reply, build_no_results_message

router = APIRouter()


# ════════════════════════════════════════════════════════════════
# QUICK RULE-BASED (sans Ollama)
# ════════════════════════════════════════════════════════════════

def detect_quick_general_case(user_input: str, language: str) -> str | None:
    text = (user_input or "").strip().lower()

    def pick(ar, fr, en):
        lst = ar if language == "ar" else fr if language == "fr" else en
        return random.choice(lst)

    state = {
        "واش راك","وش راك","واشراك","وشراك","لاباس","لباس","كيفك","كيف حالك",
        "كيف راه الحال","كيف الحال","شلونك","شخبارك","راك مليح","راك بخير",
        "كيراك","كي راك","واش حوالك","وش حوالك","راك داير","واش داير","وش داير",
        "how are you","how are u","how r u","are you ok","are you fine",
        "you good","you ok","cv","ça va","ca va","comment ça va","tu vas bien",
    }
    greetings = {
        "السلام عليكم","سلام","مرحبا","اهلا","أهلا","هلا",
        "hello","hi","hey","hola","salut","bonjour","bonsoir",
    }
    identity = {
        "من انت","من أنت","شكون انت","عرف روحك","من تكون",
        "who are you","qui es tu","qui es-tu","tu es qui",
    }
    help_requests = {
        "كيفاش تخدم","كيف تعمل","اش تدير","واش تدير","ساعدني","عاوني",
        "how do you work","what do you do","help","help me",
        "comment tu fonctionnes","comment ça marche","aide moi","aide-moi",
    }
    thanks = {
        "شكرا","شكراً","مرسي","يعطيك الصحة","صحا","بارك الله فيك",
        "thanks","thank you","thx","merci","merci beaucoup",
    }
    goodbye = {
        "باي","نشوفك","الى اللقاء","إلى اللقاء","تصبح على خير",
        "bye","goodbye","see you","au revoir","à bientôt",
    }
    capabilities = {
        "وش تقدر تدير","ماذا تستطيع","شنو تقدر تعاون",
        "what can you do","que peux tu faire","que peux-tu faire",
    }
    communes_q = {
        "ما هي البلديات","وش هي البلديات","البلديات المتوفرة",
        "what communes","quelles communes","communes disponibles",
    }
    services_q = {
        "ما هي الخدمات","وش هي الخدمات","الخدمات المتوفرة",
        "what services","quels services","services disponibles",
    }

    if text in state:
        return pick(
            ["الحمد لله بخير، كيفاش نقدر نساعدك؟","بخير! وش تحتاج اليوم؟","لاباس، قلّي الخدمة والبلدية ونعاونك."],
            ["Ça va bien ! Comment puis-je vous aider ?","Je vais bien, quel service cherchez-vous ?","Tout va bien, dites-moi ce dont vous avez besoin."],
            ["I'm good! How can I help you?","Doing well. What service do you need?","All good! Tell me the service and commune."],
        )
    if text in greetings:
        return pick(
            ["مرحبا 👋 أنا مساعد Artisans DZ لولاية تيارت. قلّي وش تحتاج!","أهلاً! ذكر الخدمة والبلدية ونبحثلك مباشرة."],
            ["Bonjour 👋 Je suis l'assistant Artisans DZ pour Tiaret. Que cherchez-vous ?","Salut ! Donnez-moi le service et la commune."],
            ["Hello 👋 I'm the Artisans DZ assistant for Tiaret. What do you need?","Hi! Tell me the service and commune."],
        )
    if text in identity:
        return pick(
            ["أنا مساعد ذكي لمنصة Artisans DZ — أساعدك تلقى الحرفيين في 42 بلدية من ولاية تيارت."],
            ["Je suis l'assistant intelligent de la plateforme Artisans DZ — je vous aide à trouver des artisans dans 42 communes de la wilaya de Tiaret."],
            ["I'm the smart assistant of Artisans DZ — I help you find artisans across 42 communes in Tiaret wilaya."],
        )
    if text in help_requests:
        return pick(
            ["اكتب نوع الخدمة + البلدية. مثال: سباك في تيارت أو كهربائي في فرندة. تقدر كذلك تفلتر: رخيص، الأفضل، عندو خبرة."],
            ["Écrivez le service + la commune. Exemple : plombier à Tiaret ou électricien à Frenda. Filtres disponibles : pas cher, mieux noté, expérimenté."],
            ["Type the service + commune. Example: plumber in Tiaret or electrician in Frenda. Filters: cheap, best rated, experienced."],
        )
    if text in thanks:
        return pick(
            ["على الرحب والسعة 😊","بكل سرور!","العفو، أي وقت!"],
            ["Avec plaisir 😊","Je vous en prie !","De rien, à votre service !"],
            ["You're welcome 😊","Glad to help!","Anytime!"],
        )
    if text in goodbye:
        return pick(
            ["إلى اللقاء 👋 يسعد وقتك!","في أمان الله.","مع السلامة 😊"],
            ["Au revoir 👋 Bonne journée !","À bientôt !","Bonne continuation !"],
            ["Goodbye 👋 Have a great day!","See you!","Take care!"],
        )
    if text in capabilities:
        return pick(
            ["نقدر: نبحث عن سباك، كهربائي، نجار، دهان، تكييف، بنّاء، نظافة، بستنة. في 42 بلدية من ولاية تيارت. مع فلاتر: رخيص، الأفضل، عندو خبرة. ونجاوب على أسئلة عن العامل: السعر، التوفر، التواصل..."],
            ["Je peux : chercher plombier, électricien, menuisier, peintre, clim, maçon, nettoyage, jardinage. Dans 42 communes de Tiaret. Avec filtres : moins cher, mieux noté, expérimenté. Et répondre aux questions sur le prestataire : tarif, disponibilité, contact..."],
            ["I can: find plumber, electrician, carpenter, painter, AC, mason, cleaning, gardening. In 42 communes of Tiaret. With filters: cheap, best rated, experienced. And answer questions about the provider: price, availability, contact..."],
        )
    if text in communes_q:
        return pick(
            ["نغطي 42 بلدية منها: تيارت، سوقر، فرندة، ماهدية، راهوية، قصر الشلالة، عين الضهب، دحموني وأكثر."],
            ["Nous couvrons 42 communes dont : Tiaret, Sougueur, Frenda, Mahdia, Rahouia, Ksar Chellala, Ain Deheb, Dahmouni et plus."],
            ["We cover 42 communes including: Tiaret, Sougueur, Frenda, Mahdia, Rahouia, Ksar Chellala, Ain Deheb, Dahmouni and more."],
        )
    if text in services_q:
        return pick(
            ["الخدمات المتوفرة: 🔧 سباكة | ⚡ كهرباء | 🪵 نجارة | 🎨 دهان | ❄️ تكييف | 🏗️ بناء | 🧹 نظافة | 🌿 بستنة"],
            ["Services disponibles : 🔧 Plomberie | ⚡ Électricité | 🪵 Menuiserie | 🎨 Peinture | ❄️ Climatisation | 🏗️ Maçonnerie | 🧹 Nettoyage | 🌿 Jardinage"],
            ["Available services: 🔧 Plumbing | ⚡ Electricity | 🪵 Carpentry | 🎨 Painting | ❄️ AC | 🏗️ Masonry | 🧹 Cleaning | 🌿 Gardening"],
        )

    return None


def detect_general_limited_case(user_input: str, language: str) -> str | None:
    text = (user_input or "").strip().lower()
    realtime = {"الطقس","weather","météo","الاورو","euro","dollar","دولار","أخبار","news","actualités","match","ماتش","score"}
    coding   = {"python","java","javascript","code","programming","برمجة","كود","algorithm","algorithme"}
    if any(w in text for w in realtime):
        return {
            "ar": "ما عنديش معلومات لحظية. نقدر نعاونك في البحث عن حرفيين في تيارت.",
            "fr": "Je n'ai pas d'informations en temps réel. Je peux vous aider à trouver des artisans à Tiaret.",
            "en": "I don't have real-time information. I can help you find artisans in Tiaret.",
        }.get(language, "")
    if any(w in text for w in coding):
        return {
            "ar": "اختصاصي هو مساعدتك في خدمات محلية بتيارت. اكتبلي الخدمة والبلدية.",
            "fr": "Ma spécialité est de vous aider à trouver des artisans locaux à Tiaret.",
            "en": "My specialty is helping you find local artisans in Tiaret.",
        }.get(language, "")
    return None


def build_followup_suggestions(language: str, provider: dict | None = None) -> list[str]:
    """Suggestions contextuelles après affichage d'un prestataire."""
    if language == "ar":
        base = ["كم يكلف التدخل؟","هل هو متوفر الآن؟","كيف نتواصل معه؟","كم يحتاج من وقت؟"]
        if provider and not provider.get("is_available", True):
            base[1] = "حدد لي عامل آخر متوفر"
    elif language == "fr":
        base = ["Quel est le tarif ?","Est-il disponible ?","Comment le contacter ?","Combien de temps ?"]
        if provider and not provider.get("is_available", True):
            base[1] = "Trouvez-moi un autre disponible"
    else:
        base = ["What is the price?","Is he available?","How to contact him?","How long does it take?"]
        if provider and not provider.get("is_available", True):
            base[1] = "Find me another available one"
    return base


# ════════════════════════════════════════════════════════════════
# ROUTE PRINCIPALE /chat
# ════════════════════════════════════════════════════════════════

@router.get("/chat")
def chat(
    user_input: str,
    session_id: str = Query(default="default"),
    db: Session = Depends(get_db),
):
    memory  = get_memory(session_id)
    history = get_history(session_id)
    append_history(session_id, "user", user_input)

    intent  = extract_intent(user_input, history) or {}
    intent  = merge_with_memory(intent, memory)

    language         = intent.get("language", "fr")
    service          = intent.get("service")
    commune          = intent.get("commune") or intent.get("city")   # FIX: unifié
    filters          = intent.get("filters", {}) or {}
    provider_question = intent.get("provider_question")

    moderation = moderate_user_input(user_input, language)

    def suggs(hint, has_res=True):
        intent["has_results"] = has_res
        return generate_suggestions(intent, status_hint=hint)

    # ── 0. ABUS → blocage ───────────────────────────────────────
    if moderation["blocked"]:
        reply = moderation["message"]
        append_history(session_id, "assistant", reply)
        return {"reply": reply, "providers": [], "suggestions": [], "status_hint": "blocked"}

    # ── 1. QUICK RULE-BASED ──────────────────────────────────────
    quick = detect_quick_general_case(user_input, language)
    if quick:
        append_history(session_id, "assistant", quick)
        return {"reply": quick, "providers": [], "suggestions": suggs("answering"), "status_hint": "answering"}

    # ── 2. LIMITED GENERAL ───────────────────────────────────────
    limited = detect_general_limited_case(user_input, language)
    if limited:
        append_history(session_id, "assistant", limited)
        return {"reply": limited, "providers": [], "suggestions": suggs("answering"), "status_hint": "answering"}

    # ── 3. ✅ FIX: PROVIDER FOLLOW-UP — traité AVANT general question ──
    if provider_question:
        last_provider = memory.get("last_best_provider")
        if last_provider:
            reply = format_reply(answer_provider_question(last_provider, provider_question, language))
            append_history(session_id, "assistant", reply)
            return {
                "reply":       reply,
                "providers":   [],
                "suggestions": build_followup_suggestions(language, last_provider),
                "status_hint": "answering",
            }
        else:
            # Pas de prestataire en mémoire → guide l'user
            msg = {
                "ar": "حددلي الخدمة والبلدية أولاً باش نجاوبك على هذا السؤال.",
                "fr": "Précisez d'abord le service et la commune pour que je puisse répondre.",
                "en": "Please specify the service and commune first so I can answer.",
            }.get(language, "")
            append_history(session_id, "assistant", msg)
            return {"reply": msg, "providers": [], "suggestions": suggs("clarifying"), "status_hint": "clarifying"}

    # ── 4. PROBLÈME CONCRET → aide immédiate ────────────────────
    if moderation["reason"] == "problem_description":
        pt = moderation["problem_type"]
        if pt and not service:
            intent["service"] = pt
            service = pt

        problem_reply = reply_problem_description(pt, language)

        if service and commune:
            providers = search_providers(db, service, commune, {})
            if providers:
                providers = rank_providers(providers, {})
                best      = get_best_provider(providers)
                save_memory(intent, memory, best_provider=best)
                rec        = generate_recommendation(best, language)
                full_reply = format_reply(f"{problem_reply}\n\n{rec}")
                append_history(session_id, "assistant", full_reply)
                return {
                    "reply":       full_reply,
                    "providers":   providers,
                    "suggestions": suggs("results_ready"),
                    "status_hint": "results_ready",
                }

        problem_reply = format_reply(problem_reply)
        append_history(session_id, "assistant", problem_reply)
        return {
            "reply":       problem_reply,
            "providers":   [],
            "suggestions": suggs("needs_commune" if service else "clarifying"),
            "status_hint": "needs_commune" if service else "clarifying",
        }

    # ── 5. QUESTION GÉNÉRALE → Ollama ────────────────────────────
    # FIX: seulement si PAS de service/commune détectés
    if intent.get("type") == "question" and not service and not commune:
        reply = format_reply(generate_general_answer(user_input, language, history))
        if moderation["reason"] == "negative" and moderation.get("message"):
            reply += "\n\n" + moderation["message"]
        append_history(session_id, "assistant", reply)
        return {"reply": reply, "providers": [], "suggestions": suggs("answering"), "status_hint": "answering"}

    # ── 6. SERVICE SEUL → communes disponibles ───────────────────
    if service and not commune:
        communes_av = search_only_by_service(db, service, filters)
        reply = format_reply(reply_service_only(service, communes_av, language))
        append_history(session_id, "assistant", reply)
        return {"reply": reply, "providers": [], "suggestions": suggs("needs_commune"), "status_hint": "needs_commune"}

    # ── 7. COMMUNE SEULE → services disponibles ──────────────────
    if commune and not service:
        cats  = search_only_by_commune(db, commune)
        reply = format_reply(reply_commune_only(commune, cats, language))
        append_history(session_id, "assistant", reply)
        return {"reply": reply, "providers": [], "suggestions": suggs("needs_service"), "status_hint": "needs_service"}

    # ── 8. CONTEXTE FLOU ────────────────────────────────────────
    if not service and not commune:
        if moderation["reason"] == "negative":
            # FIX: utilise le contexte mémoire pour relancer la recherche
            last_service = memory.get("service")
            last_commune = memory.get("commune")
            if last_service and last_commune:
                service, commune = last_service, last_commune
                # continue vers la recherche normale (step 9)
            else:
                msg = {
                    "ar": "وش ما عجبكش بالضبط؟ حددلي الخدمة والبلدية ونعاونك تلقى عامل أحسن.",
                    "fr": "Qu'est-ce qui ne vous a pas plu ? Précisez le service et la commune.",
                    "en": "What didn't you like? Specify the service and commune.",
                }.get(language, "")
                append_history(session_id, "assistant", msg)
                return {"reply": msg, "providers": [], "suggestions": suggs("clarifying"), "status_hint": "clarifying"}
        else:
            msg = {
                "ar": "💡 حددلي الخدمة والبلدية. مثال: سباك في تيارت أو كهربائي في فرندة",
                "fr": "💡 Précisez le service et la commune. Exemple : plombier à Tiaret ou électricien à Frenda",
                "en": "💡 Please specify the service and the commune. Example: plumber in Tiaret or electrician in Frenda",
            }.get(language, "")
            append_history(session_id, "assistant", msg)
            return {"reply": msg, "providers": [], "suggestions": suggs("clarifying"), "status_hint": "clarifying"}

    # ── 9. RECHERCHE NORMALE (service + commune) ─────────────────
    providers = search_providers(db, service, commune, filters) or []

    if not providers:
        communes_alt = search_only_by_service(db, service, {})
        alt_msg = ""
        if communes_alt:
            alt_list = ", ".join(c.capitalize() for c in communes_alt[:3])
            alt_msg = {
                "ar": f"\nلكن هذه الخدمة متوفرة في: {alt_list}.",
                "fr": f"\nMais ce service est disponible à : {alt_list}.",
                "en": f"\nBut this service is available in: {alt_list}.",
            }.get(language, "")
        reply = format_reply(build_no_results_message(language) + alt_msg)
        append_history(session_id, "assistant", reply)
        return {"reply": reply, "providers": [], "suggestions": suggs("no_results", has_res=False), "status_hint": "no_results"}

    providers = rank_providers(providers, filters)
    best      = get_best_provider(providers)

    # ✅ FIX: save_memory avec best_provider → follow-up questions marchent
    save_memory(intent, memory, best_provider=best)

    if moderation["reason"] == "negative":
        intro = {
            "ar": "فهمت. إليك عامل أحسن مقترح لك:",
            "fr": "Je comprends. Voici un meilleur prestataire pour vous :",
            "en": "I understand. Here's a better provider for you:",
        }.get(language, "")
        explanation = build_provider_explanation(best, language)
        reply = f"{intro}\n{explanation}"
    else:
        recommendation = generate_recommendation(best, language)
        explanation    = build_provider_explanation(best, language)
        reply = f"{recommendation}\n{explanation}"

    reply = format_reply(reply)
    append_history(session_id, "assistant", reply)

    return {
        "reply":       reply,
        "providers":   providers,
        "suggestions": suggs("results_ready"),
        "status_hint": "results_ready",
    }


# ════════════════════════════════════════════════════════════════
# ROUTE /chat/stream — FIX: supporte provider follow-up
# ════════════════════════════════════════════════════════════════

@router.get("/chat/stream")
def chat_stream(
    user_input: str,
    session_id: str = Query(default="default"),
    db: Session = Depends(get_db),
):
    memory   = get_memory(session_id)
    history  = get_history(session_id)
    intent   = extract_intent(user_input, history) or {}
    intent   = merge_with_memory(intent, memory)

    language          = intent.get("language", "fr")
    service           = intent.get("service")
    commune           = intent.get("commune") or intent.get("city")
    provider_question = intent.get("provider_question")

    def event_stream():
        moderation = moderate_user_input(user_input, language)

        if moderation["blocked"]:
            for c in moderation["message"]: yield c
            return

        quick = detect_quick_general_case(user_input, language)
        if quick:
            for c in quick: yield c
            return

        limited = detect_general_limited_case(user_input, language)
        if limited:
            for c in limited: yield c
            return

        # ✅ FIX: provider follow-up dans stream aussi
        if provider_question:
            last_provider = memory.get("last_best_provider")
            if last_provider:
                msg = format_reply(answer_provider_question(last_provider, provider_question, language))
            else:
                msg = {
                    "ar": "حددلي الخدمة والبلدية أولاً.",
                    "fr": "Précisez d'abord le service et la commune.",
                    "en": "Please specify the service and commune first.",
                }.get(language, "")
            for c in msg: yield c
            return

        if moderation["reason"] == "problem_description":
            msg = reply_problem_description(moderation["problem_type"], language)
            for c in format_reply(msg): yield c
            return

        if intent.get("type") == "question" and not service and not commune:
            yield from stream_general_answer(user_input, language, history)
            return

        if not service and not commune:
            if moderation["reason"] == "negative":
                last_s = memory.get("service")
                last_c = memory.get("commune")
                msg = (
                    {"ar":"فهمت. جاري البحث عن عامل أحسن...","fr":"Compris. Je cherche un meilleur prestataire...","en":"Understood. Looking for a better provider..."}.get(language, "")
                    if last_s and last_c else
                    {"ar":"وش ما عجبكش؟ حددلي الخدمة والبلدية.","fr":"Qu'est-ce qui ne vous a pas plu ? Précisez service et commune.","en":"What didn't you like? Specify service and commune."}.get(language, "")
                )
            else:
                msg = {
                    "ar":"💡 حدد الخدمة والبلدية. مثال: سباك في تيارت",
                    "fr":"💡 Précisez le service et la commune. Ex: plombier à Tiaret",
                    "en":"💡 Specify service and commune. Ex: plumber in Tiaret",
                }.get(language, "")
            for c in msg: yield c
            return

        save_memory(intent, memory)

        msg = {
            "ar":"🔍 جاري البحث في بلديات تيارت...",
            "fr":"🔍 Recherche dans les communes de Tiaret...",
            "en":"🔍 Searching Tiaret communes...",
        }.get(language, "")
        for c in msg: yield c

    return StreamingResponse(event_stream(), media_type="text/plain; charset=utf-8")