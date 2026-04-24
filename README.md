# 🔧 Artisans DZ — AI Service

> **Projet de Fin d'Études (PFE) — Licence Informatique**
> Assistant IA pour la mise en relation entre demandeurs et prestataires de services dans la wilaya de Tiaret, Algérie.

---

## 📋 Table des matières

- [Présentation du projet](#présentation-du-projet)
- [Architecture](#architecture)
- [Stack technique](#stack-technique)
- [Installation locale](#installation-locale)
- [Lancement avec Docker](#lancement-avec-docker)
- [Structure du projet](#structure-du-projet)
- [Fonctionnalités AI](#fonctionnalités-ai)
- [API Reference](#api-reference)
- [Base de données](#base-de-données)
- [Tests](#tests)
- [Équipe](#équipe)

---

## 📌 Présentation du projet

**Artisans DZ** est une plateforme de mise en relation entre clients et artisans/prestataires de service dans la wilaya de Tiaret (42 communes).

Ce dépôt contient le **microservice AI** qui expose un assistant conversationnel intelligent capable de :

- 🔍 Comprendre des requêtes en **arabe, français et anglais**
- 📍 Localiser les prestataires par **commune**
- 🏆 **Classer** les résultats selon un score composite (note, expérience, confiance, disponibilité, prix)
- 💬 Répondre à des **questions contextuelles** sur un prestataire (prix, disponibilité, contact…)
- 💡 Proposer des **suggestions dynamiques** adaptées au contexte

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (HTML/JS)                   │
│         interface.html → http://127.0.0.1:8000          │
└────────────────────────┬────────────────────────────────┘
                         │ GET /chat?user_input=...
┌────────────────────────▼────────────────────────────────┐
│               FastAPI — AI Service                      │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │intent_service│  │search_service│  │ranking_service│  │
│  │  (NLP + NLU) │  │  (SQL query) │  │ (score/tri)   │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬───────┘  │
│         │                │                  │           │
│  ┌──────▼──────────────────────────────────▼───────┐   │
│  │           memory_service (session TTL 30 min)    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │     ai_service → Ollama (qwen2.5:3b)             │   │
│  │     réponses générales + suggestions             │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   PostgreSQL — Tiaret   │
              │  provider / service /   │
              │  location / avis / ...  │
              └─────────────────────────┘
```

---

## ⚙️ Stack technique

| Composant | Technologie | Version |
|---|---|---|
| Backend API | FastAPI | 0.115 |
| Serveur ASGI | Uvicorn | 0.32 |
| Base de données | PostgreSQL | 16 |
| ORM | SQLAlchemy | 2.0 |
| Modèle AI | Ollama / qwen2.5:3b | local |
| Frontend | HTML + CSS + JS vanilla | — |
| Containerisation | Docker + Docker Compose | — |
| Migrations DB | Alembic | 1.14 |

---

## 🚀 Installation locale

### Prérequis

- Python 3.11+
- PostgreSQL 16
- [Ollama](https://ollama.com/) installé et lancé

### Étapes

```bash
# 1. Cloner le projet
git clone https://github.com/VOTRE_USERNAME/pfe-ai-service.git
cd pfe-ai-service/ai-service

# 2. Créer l'environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos informations (DATABASE_URL, etc.)

# 5. Créer la base de données
psql -U postgres -c "CREATE DATABASE bdd;"
psql -U postgres -d bdd -f "base de donnees/bdd.sql"
psql -U postgres -d bdd -f "base de donnees/data_tiaret.sql"

# 6. Télécharger le modèle AI
ollama pull qwen2.5:3b

# 7. Lancer le serveur
uvicorn app.main:app --reload --port 8000
```

L'API sera disponible sur : **http://127.0.0.1:8000**
L'interface sur : **http://127.0.0.1:8000/frontend/interface.html**

---

## 🐳 Lancement avec Docker

```bash
# Depuis le dossier ai-service/
docker-compose up --build

# En arrière-plan
docker-compose up -d --build

# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f api
```

> ⚠️ Ollama doit tourner en local sur le host. Le docker-compose utilise `host.docker.internal:11434` pour y accéder.

---

## 📁 Structure du projet

```
ai-service/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── chat.py              # Route principale /chat
│   ├── core/
│   │   ├── config.py                # Variables d'environnement
│   │   └── database.py              # Connexion SQLAlchemy
│   ├── services/
│   │   ├── ai_service.py            # Ollama + suggestions dynamiques
│   │   ├── catalog_service.py       # Communes et services depuis DB
│   │   ├── explanation_service.py   # Explication du choix prestataire
│   │   ├── filter_service.py        # Extraction filtres (prix, note…)
│   │   ├── intent_service.py        # NLU : service + commune + question
│   │   ├── memory_service.py        # Mémoire de session (TTL 30 min)
│   │   ├── moderation_service.py    # Détection langage abusif
│   │   ├── ranking_service.py       # Score composite + tri
│   │   └── search_service.py        # Requêtes SQL PostgreSQL
│   ├── utils/
│   │   ├── formatter.py             # Formatage des réponses
│   │   ├── language.py              # Détection langue (ar/fr/en)
│   │   ├── mapping.py               # Communes + services Tiaret
│   │   └── text.py                  # Normalisation texte arabe
│   └── main.py                      # Application FastAPI
├── frontend/
│   └── interface.html               # Interface chatbot
├── base de donnees/
│   ├── bdd.sql                      # Schéma PostgreSQL
│   └── data_tiaret.sql              # 40 prestataires Tiaret
├── .env.example                     # Template variables d'environnement
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🤖 Fonctionnalités AI

### Détection d'intention (NLU)

Le système comprend les requêtes en **3 langues** avec correction de fautes (fuzzy matching) :

```
"sbaak fi tiaret"    → service: plumber, commune: tiaret
"كهربائي في فرندة"   → service: electrician, commune: frenda
"electricien franda" → service: electrician, commune: frenda (fuzzy)
```

### Score de ranking composite

```
score = rating(45%) + expérience(20%) + trust_score(20%)
      + disponibilité(10%) + prix_compétitif(5%)
```

Tous les critères sont **normalisés entre 0 et 1** avant calcul.

### Questions contextuelles (8 types)

Après avoir trouvé des prestataires, l'utilisateur peut demander :

| Question | Exemple |
|---|---|
| Prix | "كم يكلف؟" / "quel est son tarif ?" |
| Durée | "كم يحتاج من الوقت؟" / "how long does it take?" |
| Qualité | "هل هو مليح؟" / "a-t-il de bonnes notes ?" |
| Contact | "كيف نتواصل؟" / "comment le contacter ?" |
| Disponibilité | "واش متوفر؟" / "is he available?" |
| Proximité | "قريب مني؟" / "près de moi ?" |
| Méthode de travail | "كيف يخدم؟" / "comment il travaille ?" |
| Plaintes | "عنده مشكلة؟" / "any complaints?" |

### Suggestions dynamiques

Les suggestions changent selon le contexte :

- **Résultats trouvés** → filtres alternatifs + question prestataire + autre service
- **Service seul** → communes où il est disponible
- **Commune seule** → services disponibles dans cette commune
- **Pas de résultats** → communes alternatives avec ce service

### Modération

- **Langage abusif** → bloqué avec message poli
- **Feedback négatif** → détecté, propose un meilleur prestataire

---

## 📡 API Reference

### `GET /chat`

Endpoint principal du chatbot.

**Paramètres :**

| Paramètre | Type | Défaut | Description |
|---|---|---|---|
| `user_input` | `string` | requis | Message de l'utilisateur |
| `session_id` | `string` | `"default"` | Identifiant de session |

**Réponse :**

```json
{
  "reply": "Je recommande Hassan Meziani à Frenda — ⭐ 4.9/5, 10 ans — 1800 DZD. ✅ disponible.",
  "providers": [
    {
      "id": 3,
      "first_name": "Hassan",
      "last_name": "Meziani",
      "phone": "0661101003",
      "commune": "frenda",
      "rating_average": 4.9,
      "experience_years": 10,
      "price": 1800,
      "is_available": true,
      "score": 87.4
    }
  ],
  "suggestions": [
    "plombier expérimenté à Frenda",
    "Quel est son tarif ?",
    "électricien à Frenda"
  ],
  "status_hint": "results_ready"
}
```

**Status hints :**

| Valeur | Signification |
|---|---|
| `results_ready` | Prestataires trouvés |
| `needs_commune` | Service détecté, commune manquante |
| `needs_service` | Commune détectée, service manquant |
| `no_results` | Aucun résultat |
| `answering` | Réponse générale |
| `clarifying` | Demande de précision |

### `GET /chat/stream`

Même paramètres que `/chat` — retourne la réponse en **streaming SSE**.

### `GET /health`

```json
{"status": "ok"}
```

---

## 🗄️ Base de données

**Tables principales :**

```
provider          → prestataires (rating, experience, trust_score…)
service           → offres de service (price, category_id, is_active)
service_category  → plomberie, électricité, peinture…
location          → commune + adresse
users             → comptes utilisateurs (role_id: 1=admin, n=prestataire, n=client)
avis              → évaluations clients
trust_scores      → score de confiance agrégé
```

**Données incluses :**
- 42 communes de la wilaya de Tiaret
- n prestataires répartis sur n catégories
- 20 avis clients

---

## 🧪 Tests

```bash
# Test endpoint chat
curl "http://127.0.0.1:8000/chat?user_input=plombier+tiaret"

# Test filtre prix
curl "http://127.0.0.1:8000/chat?user_input=plombier+pas+cher+tiaret"

# Test arabe
curl "http://127.0.0.1:8000/chat?user_input=%D8%B3%D8%A8%D8%A7%D9%83+%D9%81%D9%8A+%D8%AA%D9%8A%D8%A7%D8%B1%D8%AA"

# Test santé
curl "http://127.0.0.1:8000/health"
```

**Cas de test recommandés :**

| Entrée | Résultat attendu |
|---|---|
| `plombier tiaret` | Liste plombiers à Tiaret |
| `best` | Filtre par meilleure note (contexte mémoire) |
| `cheap` | Filtre par prix (contexte mémoire) |
| `سباك في تيارت` | Résultats en arabe |
| `كم يكلف؟` | Réponse prix du meilleur prestataire |
| `هل متوفر؟` | Disponibilité du prestataire |
| `plombr tiaret` | Correction fuzzy → plombier |
| `bonjour` | Salutation sans Ollama |

---

## 👥 Équipe

**Projet PFE — Semestre 6 — Licence Informatique**

Encadrant : Mr.ouguessa Abdelkader

Étudiants :
- Belhouari Youcef
- Belhouari Oussama
- Boutbel Abdelnnour

---

## 📄 Licence

Ce projet est développé dans le cadre académique du PFE
Licence ISIL، Groupe 01
Tiaret 
ibn khaldoun.
Tous droits réservés © 2025-2026.
