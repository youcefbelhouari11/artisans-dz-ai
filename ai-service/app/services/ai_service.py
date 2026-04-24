# ================================================================
# ai_service.py — Artisans DZ / Wilaya de Tiaret  
# ================================================================

import json
import random
import time
import requests
from app.core.config import settings

# ✅ FIX CRITICAL: use full Ollama generate endpoint
OLLAMA_URL = f"{settings.ollama_base_url.rstrip('/')}/api/generate"
MODEL = settings.ollama_model


# ════════════════════════════════════════════════════════════════
# LANGUE
# ════════════════════════════════════════════════════════════════

def get_language_instruction(language):
    if language == "ar":
        return "أجب بالعربية الدارجة الجزائرية فقط. لا تستعمل أي لغة أخرى."
    if language == "fr":
        return "Réponds uniquement en français. N'utilise aucune autre langue."
    return "Respond only in English. Do not use any other language."


def get_system_identity(language):
    # ✅ FIX: do not force identity in every answer
    if language == "ar":
        return (
            "أنت مساعد ذكي لمنصة Artisans DZ في ولاية تيارت. "
            "لا تعرّف بنفسك إلا إذا سُئلت مباشرة من أنت."
        )
    if language == "fr":
        return (
            "Tu es l'assistant intelligent de Artisans DZ à Tiaret. "
            "Ne te présentes que si on te demande directement qui tu es."
        )
    return (
        "You are the intelligent assistant of Artisans DZ in Tiaret. "
        "Only introduce yourself if explicitly asked who you are."
    )


def format_history(history, limit=6):
    if not history:
        return ""
    return "\n".join(
        f"{h.get('role', 'user')}: {h.get('content', '')}"
        for h in history[-limit:]
    )


# ════════════════════════════════════════════════════════════════
# RÉPONSE AUX PROBLÈMES CONCRETS (sans Ollama — rapide)
# ════════════════════════════════════════════════════════════════

_PROBLEM_ADVICE = {
    "plumber": {
        "ar": (
            "🔧 يبدو عندك مشكل في السباكة.\n"
            "• أغلق صنبور الماء الرئيسي إذا كاين تسرب\n"
            "• ما تستعملش المياه في الوقت الراهن\n"
            "• نقدر نعاونك تلقى سباك متوفر الآن — حدد البلدية باش نبحث لك"
        ),
        "fr": (
            "🔧 Vous semblez avoir un problème de plomberie. En attendant :\n"
            "• Coupez l'eau au robinet principal s'il y a une fuite\n"
            "• Évitez d'utiliser l'eau pour le moment\n"
            "• Je peux vous trouver un plombier disponible — précisez votre commune"
        ),
        "en": (
            "🔧 Looks like you have a plumbing issue. In the meantime:\n"
            "• Shut off the main water valve if there's a leak\n"
            "• Avoid using water for now\n"
            "• I can find you an available plumber — tell me your commune"
        ),
    },
    "electrician": {
        "ar": (
            "⚡ يبدو عندك مشكل في الكهرباء.\n"
            "• تحقق من القاطع الرئيسي أولاً\n"
            "• لا تلمس الأسلاك العارية أبداً\n"
            "• نقدر نعاونك تلقى كهربائي متوفر — حدد البلدية"
        ),
        "fr": (
            "⚡ Vous semblez avoir un problème électrique. À faire :\n"
            "• Vérifiez d'abord le disjoncteur principal\n"
            "• Ne touchez jamais les fils dénudés\n"
            "• Je peux trouver un électricien disponible — précisez votre commune"
        ),
        "en": (
            "⚡ Looks like an electrical issue. Do this:\n"
            "• Check the main circuit breaker first\n"
            "• Never touch bare wires\n"
            "• I can find an available electrician — tell me your commune"
        ),
    },
    "climatisation": {
        "ar": (
            "❄️ مشكل في المكيف؟ إليك خطوات سريعة:\n"
            "• تحقق إذا الفلتر محتاج تنظيف (كل شهر)\n"
            "• أعد تشغيل المكيف بعد 5 دقائق إيقاف\n"
            "• إذا المشكل مستمر، نبحث لك على تقني متوفر"
        ),
        "fr": (
            "❄️ Problème de climatiseur ? Étapes rapides :\n"
            "• Vérifiez si le filtre a besoin d'être nettoyé (tous les mois)\n"
            "• Redémarrez l'appareil après 5 minutes d'arrêt\n"
            "• Si le problème persiste, je cherche un technicien disponible"
        ),
        "en": (
            "❄️ AC problem? Quick steps:\n"
            "• Check if the filter needs cleaning (monthly)\n"
            "• Restart the unit after 5 minutes off\n"
            "• If the issue persists, I'll find an available technician"
        ),
    },
    "mason": {
        "ar": (
            "🏗️ مشكل في البناء أو الجدران؟ ما تقلقش:\n"
            "• الشقوق الصغيرة عادية، لكن الكبيرة تحتاج فحص\n"
            "• نقدر نبحث لك على بنّاء متخصص في بلديتك"
        ),
        "fr": (
            "🏗️ Problème de maçonnerie ? Pas de panique :\n"
            "• Les petites fissures sont normales, les grandes nécessitent une inspection\n"
            "• Je peux chercher un maçon spécialisé dans votre commune"
        ),
        "en": (
            "🏗️ Masonry issue? Don't worry:\n"
            "• Small cracks are normal, large ones need inspection\n"
            "• I can find a specialized mason in your commune"
        ),
    },
    "painter": {
        "ar": (
            "🎨 مشكل في الطلاء؟ نساعدك:\n"
            "• الطلاء المتقشر يحتاج تنظيف وإعادة طلاء\n"
            "• نقدر نبحث لك على دهان في بلديتك"
        ),
        "fr": (
            "🎨 Problème de peinture ? Je vous aide :\n"
            "• La peinture qui s'écaille nécessite un nettoyage et une repeinture\n"
            "• Je peux trouver un peintre dans votre commune"
        ),
        "en": (
            "🎨 Painting issue? I can help:\n"
            "• Peeling paint needs cleaning and repainting\n"
            "• I can find a painter in your commune"
        ),
    },
}


def reply_problem_description(problem_type: str, language: str) -> str:
    advice = _PROBLEM_ADVICE.get(problem_type, {})
    lang = language if language in ("ar", "fr", "en") else "fr"

    if advice:
        return advice.get(lang, advice.get("fr", ""))

    if language == "ar":
        return "فهمت مشكلتك. نقدر نساعدك تلقى متخصص. حدد البلدية باش نبحث."
    if language == "fr":
        return "Je comprends votre problème. Précisez votre commune pour que je cherche un spécialiste."
    return "I understand your issue. Tell me your commune and I'll find a specialist."


# ════════════════════════════════════════════════════════════════
# RÉPONSES PRESTATAIRE
# ════════════════════════════════════════════════════════════════

def answer_provider_question(provider: dict, question_type: str, language: str) -> str:
    name = f"{provider.get('first_name', '')} {provider.get('last_name', '')}".strip()
    rating = provider.get("rating_average") or 0
    exp = provider.get("experience_years") or 0
    price = provider.get("price")
    phone = provider.get("phone")
    available = provider.get("is_available", True)
    commune = provider.get("commune") or provider.get("city", "")
    trust = provider.get("trust_score") or 0
    verified = provider.get("is_verified", False)

    def r(ar, fr, en):
        return ar if language == "ar" else fr if language == "fr" else en

    if question_type == "price":
        if price:
            price_max = int(price * 1.2)
            return r(
                f"💰 سعر {name} يبدأ من {price} دج ويمكن يوصل تقريبًا إلى {price_max} دج حسب حجم العمل.",
                f"💰 Le tarif de {name} commence à {price} DZD et peut aller jusqu'à environ {price_max} DZD selon le travail.",
                f"💰 {name}'s rate starts at {price} DZD and may go up to around {price_max} DZD depending on the work."
            )
        return r(
            f"💰 السعر غير محدد لـ {name}. تواصل معه مباشرة على {phone or 'المنصة'}.",
            f"💰 Le tarif de {name} n'est pas précisé. Contactez-le directement au {phone or 'via la plateforme'}.",
            f"💰 {name}'s price is not listed. Contact him at {phone or 'via the platform'}."
        )

    if question_type == "duration":
        if exp >= 8:
            est_ar, est_fr, est_en = "30 دقيقة إلى ساعة", "30 min à 1 heure", "30 min to 1 hour"
        elif exp >= 4:
            est_ar, est_fr, est_en = "1 إلى 2 ساعة", "1 à 2 heures", "1 to 2 hours"
        else:
            est_ar, est_fr, est_en = "2 إلى 3 ساعات", "2 à 3 heures", "2 to 3 hours"

        return r(
            f"⏱️ {name} عادةً يحتاج {est_ar} حسب نوع العمل.",
            f"⏱️ {name} prend généralement {est_fr} selon la nature du travail.",
            f"⏱️ {name} usually takes {est_en} depending on the job."
        )

    if question_type == "quality":
        if rating >= 4.7:
            verdict_ar = "ممتاز ويُنصح به بشدة ✅"
            verdict_fr = "Excellent et fortement recommandé ✅"
            verdict_en = "Excellent and highly recommended ✅"
        elif rating >= 4.0:
            verdict_ar = "جيد جدًا وتقييمه مرضي ✅"
            verdict_fr = "Très bon avec une note satisfaisante ✅"
            verdict_en = "Very good with a satisfactory rating ✅"
        elif rating >= 3.5:
            verdict_ar = "مقبول، راجع التعليقات قبل الحجز"
            verdict_fr = "Acceptable, consultez les avis avant de réserver"
            verdict_en = "Acceptable, check reviews before booking"
        else:
            verdict_ar = "تقييم منخفض، كن حذرًا ⚠️"
            verdict_fr = "Note basse, soyez prudent ⚠️"
            verdict_en = "Low rating, be careful ⚠️"

        extras = []
        if trust >= 85:
            extras.append(r("موثوق", "très fiable", "highly trusted"))
        if verified:
            extras.append(r("موثّق", "vérifié", "verified"))

        extras_text = f" ({' - '.join(extras)})" if extras else ""

        return r(
            f"⭐ {name} تقييمه {rating}/5 — {verdict_ar}{extras_text}",
            f"⭐ {name} a {rating}/5 — {verdict_fr}{extras_text}",
            f"⭐ {name} is rated {rating}/5 — {verdict_en}{extras_text}"
        )

    if question_type == "contact":
        if phone:
            return r(
                f"📞 تقدر تتصل بـ {name} مباشرة على: {phone}",
                f"📞 Vous pouvez contacter {name} directement au: {phone}",
                f"📞 You can contact {name} directly at: {phone}"
            )
        return r(
            f"📞 رقم {name} غير متوفر حاليًا. تواصل معه عبر المنصة.",
            f"📞 Le numéro de {name} n'est pas disponible pour le moment. Contactez-le via la plateforme.",
            f"📞 {name}'s number is not available right now. Contact via the platform."
        )

    if question_type == "availability":
        if available:
            return r(
                f"✅ {name} متوفر حاليًا ويقبل طلبات جديدة في {commune}.",
                f"✅ {name} est disponible maintenant et accepte de nouvelles demandes à {commune}.",
                f"✅ {name} is available now and accepts new requests in {commune}."
            )
        return r(
            f"⚠️ {name} غير متوفر حاليًا في {commune}. نقدر نقترح عليك واحد آخر.",
            f"⚠️ {name} n'est pas disponible pour le moment à {commune}. Je peux vous proposer un autre prestataire.",
            f"⚠️ {name} is not available right now in {commune}. I can suggest another provider."
        )

    if question_type == "proximity":
        return r(
            f"📍 {name} يتمركز في {commune} ويخدم البلديات المجاورة في ولاية تيارت.",
            f"📍 {name} est basé à {commune} et intervient dans les communes voisines de la wilaya de Tiaret.",
            f"📍 {name} is based in {commune} and works in nearby communes of Tiaret wilaya."
        )

    if question_type == "work_method":
        if exp >= 7:
            return r(
                f"🛠️ {name} يشتغل باحترافية: يشخص المشكل أولًا، يعطيك تقدير السعر، ثم يبدأ الخدمة.",
                f"🛠️ {name} travaille avec professionnalisme : diagnostic d'abord, devis ensuite, puis intervention.",
                f"🛠️ {name} works professionally: diagnosis first, then quote, then service."
            )
        return r(
            f"🛠️ {name} عادةً يفحص المشكل أولًا ثم يعطيك السعر قبل البداية.",
            f"🛠️ {name} inspecte généralement le problème puis donne un devis avant de commencer.",
            f"🛠️ {name} usually inspects the issue first and gives a quote before starting."
        )

    if question_type == "complaints":
        if rating >= 4.5 and trust >= 80:
            return r(
                f"✅ {name} ما بانوش عليه شكاوى واضحة، والتقييم تاعو مليح.",
                f"✅ {name} ne présente pas de plaintes marquantes et sa note est bonne.",
                f"✅ {name} does not show significant complaints and has a good rating."
            )
        return r(
            f"⚠️ راجع تقييمات {name} قبل القرار النهائي.",
            f"⚠️ Consultez les avis de {name} avant de décider.",
            f"⚠️ Check {name}'s reviews before deciding."
        )

    avail_str = r("✅ متوفر", "✅ disponible", "✅ available") if available else r("⚠️ غير متوفر", "⚠️ non disponible", "⚠️ not available")
    return r(
        f"📋 {name} في {commune}: ⭐ {rating}/5 | {exp} سنوات خبرة | {price or '—'} دج | {avail_str}",
        f"📋 {name} à {commune}: ⭐ {rating}/5 | {exp} ans | {price or '—'} DZD | {avail_str}",
        f"📋 {name} in {commune}: ⭐ {rating}/5 | {exp} yrs | {price or '—'} DZD | {avail_str}"
    )


# ════════════════════════════════════════════════════════════════
# SUGGESTIONS DYNAMIQUES
# ════════════════════════════════════════════════════════════════

_SVC_LABELS = {
    "plumber": ("سباك", "plombier", "plumber"),
    "electrician": ("كهربائي", "électricien", "electrician"),
    "carpenter": ("نجار", "menuisier", "carpenter"),
    "painter": ("دهان", "peintre", "painter"),
    "climatisation": ("تكييف", "climatisation", "ac repair"),
    "mason": ("بنّاء", "maçon", "mason"),
    "cleaner": ("نظافة", "nettoyage", "cleaning"),
    "gardener": ("بستاني", "jardinier", "gardener"),
}

_TOP_COMMUNES = ["tiaret", "sougueur", "frenda", "mahdia", "rahouia", "ksar chellala", "ain deheb", "dahmouni"]
_TOP_SERVICES = ["plumber", "electrician", "painter", "carpenter", "mason", "climatisation", "cleaner", "gardener"]

_FILTER_VARIANTS = {
    "ar": [
        ("{svc} رخيص في {cm}", "price"),
        ("{svc} عندو خبرة في {cm}", "experience"),
        ("{svc} الأفضل في {cm}", "rating"),
        ("{svc} متوفر في {cm}", "available"),
    ],
    "fr": [
        ("{svc} pas cher à {cm}", "price"),
        ("{svc} expérimenté à {cm}", "experience"),
        ("{svc} mieux noté à {cm}", "rating"),
        ("{svc} disponible à {cm}", "available"),
    ],
    "en": [
        ("cheap {svc} in {cm}", "price"),
        ("experienced {svc} in {cm}", "experience"),
        ("best {svc} in {cm}", "rating"),
        ("available {svc} in {cm}", "available"),
    ],
}

_PROVIDER_QUESTIONS = {
    "ar": [
        "كم يكلف التدخل؟",
        "هل هو متوفر الآن؟",
        "كيف نتواصل معه؟",
        "هل تقييمه مليح؟",
        "كم يحتاج من الوقت؟",
    ],
    "fr": [
        "Quel est son tarif ?",
        "Est-il disponible maintenant ?",
        "Comment le contacter ?",
        "A-t-il de bonnes notes ?",
        "Combien de temps prend l'intervention ?",
    ],
    "en": [
        "What is his rate?",
        "Is he available now?",
        "How to contact him?",
        "Does he have good reviews?",
        "How long does it take?",
    ],
}

_NO_RESULT_SUGGS = {
    "ar": ["جرب بلدية أخرى", "جرب خدمة أخرى", "شوف كل الخدمات المتوفرة"],
    "fr": ["Essayer une autre commune", "Essayer un autre service", "Voir tous les services"],
    "en": ["Try another commune", "Try another service", "See all available services"],
}


def _svc(service, language):
    labels = _SVC_LABELS.get(service, (service, service, service))
    return labels[0] if language == "ar" else labels[1] if language == "fr" else labels[2]


def _cm(commune, language):
    if not commune:
        return ""
    return commune if language == "ar" else commune.capitalize()


def generate_suggestions(intent: dict, status_hint: str = "") -> list[str]:
    service = intent.get("service")
    commune = intent.get("commune") or intent.get("city")
    language = intent.get("language", "fr")
    filters = intent.get("filters") or {}
    sort_by = filters.get("sort_by")
    has_results = intent.get("has_results", True)
    lang = language if language in ("ar", "fr", "en") else "fr"
    suggs = []

    if service and commune and (status_hint == "results_ready" or has_results):
        sl = _svc(service, language)
        cm = _cm(commune, language)
        all_f = [(t, k) for t, k in _FILTER_VARIANTS[lang] if k != sort_by]
        selected = random.sample(all_f, min(2, len(all_f)))
        for tmpl, _ in selected:
            suggs.append(tmpl.format(svc=sl, cm=cm))
        suggs.append(random.choice(_PROVIDER_QUESTIONS[lang]))
        others = [s for s in _TOP_SERVICES if s != service]
        if others:
            alt = random.choice(others[:4])
            alt_sl = _svc(alt, language)
            if language == "ar":
                suggs.append(f"{alt_sl} في {cm}")
            elif language == "fr":
                suggs.append(f"{alt_sl} à {cm}")
            else:
                suggs.append(f"{alt_sl} in {cm}")
        return suggs[:4]

    if service and not commune:
        sl = _svc(service, language)
        communes = random.sample(_TOP_COMMUNES, min(3, len(_TOP_COMMUNES)))
        for c in communes:
            cm = _cm(c, language)
            if language == "ar":
                suggs.append(f"{sl} في {cm}")
            elif language == "fr":
                suggs.append(f"{sl} à {cm}")
            else:
                suggs.append(f"{sl} in {cm}")
        if language == "ar":
            suggs.append(f"أفضل {sl} في تيارت")
        elif language == "fr":
            suggs.append(f"meilleur {sl} à Tiaret")
        else:
            suggs.append(f"best {sl} in Tiaret")
        return suggs[:4]

    if commune and not service:
        cm = _cm(commune, language)
        services = random.sample(_TOP_SERVICES, min(3, len(_TOP_SERVICES)))
        for s in services:
            sl = _svc(s, language)
            if language == "ar":
                suggs.append(f"{sl} في {cm}")
            elif language == "fr":
                suggs.append(f"{sl} à {cm}")
            else:
                suggs.append(f"{sl} in {cm}")
        if language == "ar":
            suggs.append(f"أفضل خدمة في {cm}")
        elif language == "fr":
            suggs.append(f"meilleur service à {cm}")
        else:
            suggs.append(f"best service in {cm}")
        return suggs[:4]

    if status_hint == "no_results":
        base = _NO_RESULT_SUGGS[lang].copy()
        if service:
            sl = _svc(service, language)
            for c in [c for c in _TOP_COMMUNES if c != commune][:2]:
                cm = _cm(c, language)
                if language == "ar":
                    base.insert(0, f"{sl} في {cm}")
                elif language == "fr":
                    base.insert(0, f"{sl} à {cm}")
                else:
                    base.insert(0, f"{sl} in {cm}")
        return base[:4]

    defaults = {
        "ar": ["سباك في تيارت", "كهربائي في فرندة", "نجار في سوقر", "دهان في ماهدية"],
        "fr": ["plombier à Tiaret", "électricien à Frenda", "menuisier à Sougueur", "peintre à Mahdia"],
        "en": ["plumber in Tiaret", "electrician in Frenda", "carpenter in Sougueur", "painter in Mahdia"],
    }
    pool = defaults[lang].copy()
    random.shuffle(pool)
    return pool[:4]


# ════════════════════════════════════════════════════════════════
# RECOMMANDATION PRINCIPALE
# ════════════════════════════════════════════════════════════════

def generate_recommendation(provider: dict, language: str) -> str:
    if not provider:
        return fallback_no_results(language)

    name = f"{provider.get('first_name', '')} {provider.get('last_name', '')}".strip()
    commune = provider.get("commune") or provider.get("city", "")
    rating = provider.get("rating_average", 0)
    exp = provider.get("experience_years", 0)
    price = provider.get("price")
    avail = provider.get("is_available", True)
    verified = provider.get("is_verified", False)

    avail_s = ("✅ متوفر" if language == "ar" else "✅ disponible" if language == "fr" else "✅ available") if avail \
        else ("⚠️ غير متوفر" if language == "ar" else "⚠️ non disponible" if language == "fr" else "⚠️ not available")
    price_s = (f" | 💰 {price} دج" if language == "ar" else f" | 💰 {price} DZD") if price else ""
    verif_s = (" | ✔️ موثّق" if language == "ar" else " | ✔️ Vérifié" if language == "fr" else " | ✔️ Verified") if verified else ""

    if language == "ar":
        return f"أنصح بـ {name} في {commune} — ⭐ {rating}/5 | {exp} سنوات خبرة{price_s}{verif_s}. {avail_s}."
    if language == "fr":
        return f"Je recommande {name} à {commune} — ⭐ {rating}/5 | {exp} ans{price_s}{verif_s}. {avail_s}."
    return f"I recommend {name} in {commune} — ⭐ {rating}/5 | {exp} yrs{price_s}{verif_s}. {avail_s}."


# ════════════════════════════════════════════════════════════════
# SERVICE SEUL / COMMUNE SEULE
# ════════════════════════════════════════════════════════════════

def reply_service_only(service: str, communes: list, language: str) -> str:
    if not communes:
        if language == "ar":
            return f"ما لقيناش {service} في قاعدة البيانات حالياً."
        if language == "fr":
            return f"Aucun {service} trouvé actuellement."
        return f"No {service} found currently."

    commune_list = ", ".join(c.capitalize() for c in communes[:5])

    if language == "ar":
        return f"🔍 وجدنا {service} في هذه البلديات: {commune_list}. حدد البلدية التي تريدها."
    if language == "fr":
        return f"🔍 Des prestataires en {service} sont disponibles à : {commune_list}. Précisez la commune souhaitée."
    return f"🔍 Providers for {service} are available in: {commune_list}. Specify the commune."


def reply_commune_only(commune: str, categories: list, language: str) -> str:
    if not categories:
        if language == "ar":
            return f"ما لقيناش خدمات في {commune} حالياً."
        if language == "fr":
            return f"Aucun service disponible à {commune}."
        return f"No services in {commune} currently."

    cat_list = ", ".join(c.capitalize() for c in categories)

    if language == "ar":
        return f"📍 في {commune} عندنا هذه الخدمات المتوفرة: {cat_list}. قولي وش تحتاج بالضبط."
    if language == "fr":
        return f"📍 À {commune.capitalize()}, les services disponibles sont : {cat_list}. Précisez le service souhaité."
    return f"📍 In {commune.capitalize()}, available services: {cat_list}. Tell me which service you need."


# ════════════════════════════════════════════════════════════════
# RÉPONSE GÉNÉRALE OLLAMA
# ════════════════════════════════════════════════════════════════

def build_general_prompt(user_input, language, history=None):
    if language == "ar":
        rules = (
            "قواعد:\n"
            "- أجب بشكل طبيعي ومختصر\n"
            "- لا تعرّف بنفسك إلا إذا سُئلت مباشرة\n"
            "- إذا لا تعرف الجواب، قل ذلك بوضوح\n"
            "- لا تكرر نفس العبارة في كل مرة"
        )
    elif language == "fr":
        rules = (
            "Règles:\n"
            "- Réponds naturellement et brièvement\n"
            "- Ne te présente que si on te demande qui tu es\n"
            "- Si tu ne sais pas, dis-le clairement\n"
            "- Ne répète pas la même phrase à chaque fois"
        )
    else:
        rules = (
            "Rules:\n"
            "- Reply naturally and briefly\n"
            "- Only introduce yourself if asked who you are\n"
            "- If you do not know, say it clearly\n"
            "- Do not repeat the same sentence every time"
        )

    return f"""{get_language_instruction(language)}
{get_system_identity(language)}
{rules}

Historique:
{format_history(history)}

Message: {user_input}
Réponse:""".strip()


def sanitize_answer(answer, language):
    if not answer:
        return fallback_message(language)

    cleaned = answer.strip()
    banned = [
        "qwen",
        "alibaba cloud",
        "i am qwen",
        "je suis qwen",
        "أنا qwen",
        "created by alibaba",
        "créé par alibaba",
        "i'm qwen",
        "je suis un assistant ia d'alibaba",
    ]

    if any(b in cleaned.lower() for b in banned):
        return fallback_message(language)

    return cleaned


def generate_general_answer(user_input, language, history=None):
    prompt = build_general_prompt(user_input, language, history)
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.25,
                    "top_p": 0.9,
                    "num_predict": 150,
                },
            },
            timeout=20,
        )
        resp.raise_for_status()
        return sanitize_answer(resp.json().get("response", ""), language)
    except Exception as e:
        print("AI ERROR:", e)
        return fallback_message(language)


def stream_general_answer(user_input, language, history=None):
    prompt = build_general_prompt(user_input, language, history)
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.25,
                    "top_p": 0.9,
                    "num_predict": 150,
                },
            },
            stream=True,
            timeout=60,
        )
        resp.raise_for_status()
        full = ""

        for line in resp.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                chunk = data.get("response", "")
                if chunk:
                    full += chunk
                    yield chunk
                if data.get("done"):
                    break
            except Exception:
                continue

        if full and sanitize_answer(full, language) != full:
            yield ""
    except Exception as e:
        print("STREAM ERROR:", e)
        for c in fallback_message(language):
            yield c
            time.sleep(0.01)


# ════════════════════════════════════════════════════════════════
# FALLBACKS
# ════════════════════════════════════════════════════════════════

def fallback_message(language):
    if language == "ar":
        return "ما فهمتش سؤالك مليح، جرب تسقسي على خدمة أو حرفي في تيارت 😊"
    if language == "fr":
        return "Je ne peux pas répondre à cette question pour le moment 😊. Reformulez-la autrement."
    return "I can't answer that question right now 😊. Please rephrase it."


def fallback_no_results(language):
    if language == "ar":
        return "ما لقيناش نتائج😊. جرب بلدية أو خدمة أخرى."
    if language == "fr":
        return "Aucun résultat. 😊 Essayez une autre commune ou service."
    return "No results. 😊 Try a different commune or service."