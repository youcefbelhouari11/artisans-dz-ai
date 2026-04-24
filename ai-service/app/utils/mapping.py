# ================================================================
# mapping.py — Artisans DZ / Wilaya de Tiaret
# Toutes les villes → communes de la wilaya 14
# ================================================================


# ── SERVICES : noms canoniques + variantes ──────────────────────
SERVICE_MAPPING = {
    "plumber": [
        "plumber", "plombier", "plomberie",
        "سباك", "سباكة", "سبّاك",
    ],
    "electrician": [
        "electrician", "electricien", "électricien",
        "electricite", "électricité",
        "كهربائي", "كهرباء", "كهربجي",
    ],
    "carpenter": [
        "carpenter", "menuisier", "menuiserie",
        "نجار", "نجارة",
    ],
    "painter": [
        "painter", "peintre", "peinture",
        "دهان", "صباغ", "صباغة",
    ],
    "climatisation": [
        "climatisation", "climatiseur", "clim",
        "مكيف", "مكيفات", "تكييف",
    ],
    "mason": [
        "mason", "maçon", "maçonnerie",
        "بنّاء", "بناء", "مبني",
    ],
    "cleaner": [
        "cleaner", "nettoyeur", "nettoyage",
        "نظافة", "منظف",
    ],
    "gardener": [
        "gardener", "jardinier", "jardinage",
        "حدّاق", "بستاني",
    ],
}


# ── KEYWORDS : détection par contexte ───────────────────────────
SERVICE_KEYWORDS = {
    "plumber": [
        "fuite", "canalisation", "robinet", "tuyau", "toilette", "wc",
        "leak", "pipe", "water", "sink",
        "تسرب", "ماء", "حنفية", "مواسير", "أنبوب", "مرحاض", "سيفون",
    ],
    "electrician": [
        "prise", "interrupteur", "cable", "fil", "courant", "tension",
        "electricity", "switch", "socket", "lamp", "light", "wire",
        "مصباح", "لمبة", "ضوء", "إنارة", "كهرباء",
        "قابس", "سلك", "شورط", "قاطع",
    ],
    "carpenter": [
        "porte", "fenetre", "bois", "armoire", "table",
        "door", "window", "wood", "furniture",
        "باب", "نافذة", "خشب", "خزانة", "طاولة", "أثاث",
    ],
    "painter": [
        "peinture", "mur", "couleur", "façade", "vernis",
        "paint", "wall", "color",
        "طلاء", "دهان", "جدار", "لون", "واجهة",
    ],
    "climatisation": [
        "climatiseur", "clim", "froid", "chaud", "air",
        "ac", "cooling", "air conditioning",
        "مكيف", "تبريد", "حرارة", "تكييف",
    ],
    "mason": [
        "béton", "ciment", "mur", "dalle", "carrelage",
        "cement", "concrete", "tile", "wall",
        "بيتون", "إسمنت", "بلاط", "طوب",
    ],
    "cleaner": [
        "nettoyage", "ménage", "propreté",
        "cleaning", "sweep",
        "نظافة", "كنس", "غسيل",
    ],
    "gardener": [
        "jardin", "gazon", "plante", "arbre",
        "garden", "grass", "tree",
        "حديقة", "عشب", "شجرة",
    ],
}


# ── COMMUNES DE TIARET (42 communes wilaya 14) ──────────────────
# Chaque commune a : nom canonique → liste de variantes
COMMUNE_MAPPING = {
    "tiaret": [
        "tiaret", "تيارت", "تيارط", "tyaret", "tiaret centre",
    ],
    "sougueur": [
        "sougueur", "سوقر", "سقر", "sogueur", "souger",
    ],
    "frenda": [
        "frenda", "فرندة", "franda",
    ],
    "mahdia": [
    "mahdia", "ماهدية", "مهدية",
    ],
    "rahouia": [
        "rahouia", "رحوية", "راهوية",
    ],
    "ksar chellala": [
        "ksar chellala", "قصر الشلالة", "ksar challala", "qsar chellala",
    ],
    "ain deheb": [
        "ain deheb", "عين الضهب", "عين ضهب", "ain dheb",
    ],
    "medrissa": [
        "medrissa", "مدريسة", "medressa",
    ],
    "zmalet el amir abdelkader": [
        "zmalet el amir abdelkader", "زمالة الأمير عبد القادر", "zmalet",
    ],
    "dahmouni": [
        "dahmouni", "دحموني", "dahmoni",
    ],
    "sidi bakhti": [
        "sidi bakhti", "سيدي بختي", "bakhti",
    ],
    "guertoufa": [
        "guertoufa", "قرطوفة", "guartoufa",
    ],
    "hamadia": [
        "hamadia", "حمادية", "hammadia",
    ],
    "ain kermes": [
        "ain kermes", "عين كرمس", "ain kermesse",
    ],
    "oued lilli": [
        "oued lilli", "وادي ليلي", "oued lili",
    ],
    "madna": [
        "madna", "مدنة",
    ],
    "bougara": [
        "bougara", "بوقرة",
    ],
    "sidi ali mellal": [
        "sidi ali mellal", "سيدي علي ملال",
    ],
    "rechaiga": [
        "rechaiga", "رشايقة", "rachiga",
    ],
    "ain dzarit": [
    "ain dzarit", "عين زراريت", "ain dzarrit",
    ],
    "tagdempt": [
        "tagdempt", "تاقدمت", "tagdamt",
    ],
    "djillali ben amar": [
        "djillali ben amar", "جيلالي بن عمار",
    ],
    "sidi hosni": [
        "sidi hosni", "سيدي حسني",
    ],
    "sebt": [
        "sebt", "السبت",
    ],
    "mellakou": [
        "mellakou", "ملاكو", "mellako",
    ],
    "chehaima": [
        "chehaima", "شحيمة",
    ],
    "takhemaret": [
        "takhemaret", "تاخمارت", "takhmart",
    ],
    "tousnina": [
        "tousnina", "توسنينة",
    ],
    "meghila": [
        "meghila", "مغيلة",
    ],
    "serghine": [
        "serghine", "سرغين",
    ],
    "ain el hadid": [
        "ain el hadid", "عين الحديد",
    ],
    "ouled djilali": [
        "ouled djilali", "أولاد جيلالي",
    ],
    "sidi abderrahmane": [
        "sidi abderrahmane", "سيدي عبد الرحمان",
    ],
    "naima": [
        "naima", "نعيمة",
    ],
    "ain bouchekif": [
        "ain bouchekif", "عين بوشقيف",
    ],
    "faidja": [
        "faidja", "فايجة",
    ],
    "si abdelghani": [
        "si abdelghani", "سي عبد الغاني",
    ],
    "tidda": [
        "tidda", "تيدة",
    ],
    "mechraa safa": [
        "mechraa safa", "مشرع الصفا",
    ],
    "ain el assel": [
        "ain el assel", "عين العسل",
    ],
    "nahr ouassel": [
        "nahr ouassel", "نهر وسل",
    ],
    "bekira": [
        "bekira", "بكيرة",
    ],
}

# Alias court pour compatibilité (anciennement CITY_MAPPING)
CITY_MAPPING = COMMUNE_MAPPING


# ── SERVICE → CATEGORY (pour la recherche SQL) ──────────────────
SERVICE_TO_CATEGORY = {
    "plumber":       "plomberie",
    "electrician":   "electricite",
    "carpenter":     "menuiserie",
    "painter":       "peinture",
    "climatisation": "climatisation",
    "mason":         "maçonnerie",
    "cleaner":       "nettoyage",
    "gardener":      "jardinage",
}