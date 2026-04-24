-- ================================================================
-- SCRIPT GLOBAL — BASE DE DONNÉES COMPLÈTE
-- Modules : Authentication · Provider · Avis · Messages · Demandeur
-- Compatible PostgreSQL
-- ================================================================


-- ================================================================
-- DROP TYPES & TABLES (nettoyage complet avant recréation)
-- ================================================================

DROP VIEW  IF EXISTS vue_demandes_details      CASCADE;
DROP VIEW  IF EXISTS view_top_prestataires     CASCADE;
DROP VIEW  IF EXISTS view_stats_prestataire    CASCADE;
DROP VIEW  IF EXISTS view_avis_complet         CASCADE;

DROP TABLE IF EXISTS negotiation               CASCADE;
DROP TABLE IF EXISTS demande_task              CASCADE;
DROP TABLE IF EXISTS demande                   CASCADE;
DROP TABLE IF EXISTS demandeur                 CASCADE;
DROP TABLE IF EXISTS commune                   CASCADE;

-- Ancien module demandeur (remplacé)
DROP TABLE IF EXISTS demandes_historique       CASCADE;
DROP TABLE IF EXISTS demande_lignes            CASCADE;
DROP TABLE IF EXISTS notifications             CASCADE;
DROP TABLE IF EXISTS parametres               CASCADE;
DROP TABLE IF EXISTS demandes                  CASCADE;
DROP TABLE IF EXISTS demandeurs                CASCADE;
DROP TABLE IF EXISTS communes                  CASCADE;

-- Autres modules
DROP TABLE IF EXISTS avis_ai_analysis          CASCADE;
DROP TABLE IF EXISTS moderation_queue          CASCADE;
DROP TABLE IF EXISTS avis_reports              CASCADE;
DROP TABLE IF EXISTS avis_helpful              CASCADE;
DROP TABLE IF EXISTS avis_reponses             CASCADE;
DROP TABLE IF EXISTS avis_medias               CASCADE;
DROP TABLE IF EXISTS avis                      CASCADE;
DROP TABLE IF EXISTS trust_scores              CASCADE;
DROP TABLE IF EXISTS messages                  CASCADE;
DROP TABLE IF EXISTS portfolio_image           CASCADE;
DROP TABLE IF EXISTS availability              CASCADE;
DROP TABLE IF EXISTS task                      CASCADE;
DROP TABLE IF EXISTS service                   CASCADE;
DROP TABLE IF EXISTS service_category          CASCADE;
DROP TABLE IF EXISTS provider                  CASCADE;
DROP TABLE IF EXISTS location                  CASCADE;
DROP TABLE IF EXISTS audit_log                 CASCADE;
DROP TABLE IF EXISTS login_attempt             CASCADE;
DROP TABLE IF EXISTS user_mfa                  CASCADE;
DROP TABLE IF EXISTS email_verification        CASCADE;
DROP TABLE IF EXISTS password_reset            CASCADE;
DROP TABLE IF EXISTS session                   CASCADE;
DROP TABLE IF EXISTS refresh_token             CASCADE;
DROP TABLE IF EXISTS role_permission           CASCADE;
DROP TABLE IF EXISTS permission                CASCADE;
DROP TABLE IF EXISTS users                     CASCADE;
DROP TABLE IF EXISTS role                      CASCADE;

DROP TYPE  IF EXISTS negotiation_status        CASCADE;
DROP TYPE  IF EXISTS demande_status            CASCADE;
DROP TYPE  IF EXISTS statut_demande            CASCADE;
DROP TYPE  IF EXISTS account_status            CASCADE;
DROP TYPE  IF EXISTS service_status            CASCADE;
DROP TYPE  IF EXISTS trust_level               CASCADE;
DROP TYPE  IF EXISTS media_type                CASCADE;
DROP TYPE  IF EXISTS report_reason             CASCADE;


-- ================================================================
-- ENUM TYPES
-- ================================================================

CREATE TYPE account_status AS ENUM (
    'PENDING',
    'ACTIVE',
    'SUSPENDED',
    'BANNED'
);

CREATE TYPE service_status AS ENUM (
    'DRAFT',
    'PUBLISHED',
    'ARCHIVED'
);

CREATE TYPE trust_level AS ENUM (
    'EXCELLENT',
    'TRES_FIABLE',
    'FIABLE',
    'A_SURVEILLER',
    'RISQUE',
    'NOUVEAU'
);

CREATE TYPE media_type AS ENUM (
    'image',
    'video'
);

CREATE TYPE report_reason AS ENUM (
    'spam',
    'fake',
    'offensive',
    'inappropriate',
    'other'
);

-- Enum module demandeur
CREATE TYPE demande_status AS ENUM (
    'PENDING',
    'NEGOTIATING',
    'ACCEPTED',
    'REJECTED',
    'CANCELLED',
    'IN_PROGRESS',
    'COMPLETED'
);

CREATE TYPE negotiation_status AS ENUM (
    'PENDING',
    'ACCEPTED',
    'REJECTED',
    'COUNTER'
);


-- ================================================================
-- MODULE AUTHENTIFICATION
-- ================================================================

CREATE TABLE role (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE permission (
    id          BIGSERIAL PRIMARY KEY,
    code_name   VARCHAR(100) NOT NULL,
    description TEXT,
    module      VARCHAR(100)
);

CREATE TABLE users (
    id              BIGSERIAL PRIMARY KEY,
    username        VARCHAR(100) UNIQUE NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    phone_number    VARCHAR(20),
    role_id         BIGINT,
    is_active       BOOLEAN   DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP,

    CONSTRAINT fk_role
        FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE role_permission (
    role_id       BIGINT,
    permission_id BIGINT,

    PRIMARY KEY (role_id, permission_id),

    CONSTRAINT fk_role_permission_role
        FOREIGN KEY (role_id)       REFERENCES role(id)       ON DELETE CASCADE,

    CONSTRAINT fk_role_permission_permission
        FOREIGN KEY (permission_id) REFERENCES permission(id) ON DELETE CASCADE
);

CREATE TABLE refresh_token (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT,
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked    BOOLEAN   DEFAULT FALSE,

    CONSTRAINT fk_refresh_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE session (
    id                 BIGSERIAL PRIMARY KEY,
    user_id            BIGINT,
    session_token_hash TEXT,
    ip_address         VARCHAR(50),
    user_agent         TEXT,
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at         TIMESTAMP,

    CONSTRAINT fk_session_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE password_reset (
    id               BIGSERIAL PRIMARY KEY,
    user_id          BIGINT,
    reset_token_hash TEXT,
    expires_at       TIMESTAMP,
    used             BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_reset_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE email_verification (
    id                      BIGSERIAL PRIMARY KEY,
    user_id                 BIGINT UNIQUE,
    verification_token_hash TEXT,
    verified                BOOLEAN   DEFAULT FALSE,
    expires_at              TIMESTAMP,

    CONSTRAINT fk_email_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE login_attempt (
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT,
    ip_address   VARCHAR(50),
    success      BOOLEAN,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_attempt_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE user_mfa (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT UNIQUE,
    secret_key TEXT,
    enabled    BOOLEAN   DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_mfa_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE audit_log (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT,
    action     VARCHAR(200),
    entity     VARCHAR(200),
    entity_id  BIGINT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);


-- ================================================================
-- MODULE PROVIDER
-- ================================================================

-- =========================
-- LOCATION
-- =========================

CREATE TABLE location (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(255),
    address VARCHAR(255),
    region VARCHAR(255)
);

-- =========================
-- SERVICE CATEGORY
-- =========================

CREATE TABLE service_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- =========================
-- PROVIDER
-- =========================

CREATE TABLE provider (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(50),
    bio TEXT,
    profile_image_url TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    experience_years INTEGER,
    rating_average DOUBLE PRECISION DEFAULT 0,
    trust_score DOUBLE PRECISION DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    status account_status DEFAULT 'PENDING',

    is_available BOOLEAN DEFAULT TRUE,

    location_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_provider_location
        FOREIGN KEY (location_id)
        REFERENCES location(id)
        ON DELETE SET NULL
);

-- =========================
-- SERVICE
-- =========================

CREATE TABLE service (
    id BIGSERIAL PRIMARY KEY,
    provider_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status service_status DEFAULT 'DRAFT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    price DOUBLE PRECISION,
    rating_average DOUBLE PRECISION DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    currency VARCHAR(10),
    category_id BIGINT NOT NULL,
    publication_date TIMESTAMP,
    image_url TEXT,

    CONSTRAINT fk_service_provider
        FOREIGN KEY (provider_id)
        REFERENCES provider(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_service_category
        FOREIGN KEY (category_id)
        REFERENCES service_category(id)
);

-- =========================
-- TASK
-- =========================

CREATE TABLE task (
    id BIGSERIAL PRIMARY KEY,
    service_id BIGINT NOT NULL,
    name VARCHAR(255),
    description TEXT,
    duration INTEGER,
    price DOUBLE PRECISION,
    mandatory BOOLEAN DEFAULT TRUE,
    image_url TEXT,

    CONSTRAINT fk_task_service
        FOREIGN KEY (service_id)
        REFERENCES service(id)
        ON DELETE CASCADE
);

-- =========================
-- PORTFOLIO IMAGES
-- =========================

CREATE TABLE portfolio_image (
    id BIGSERIAL PRIMARY KEY,
    provider_id BIGINT NOT NULL,
    image_url TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_portfolio_provider
        FOREIGN KEY (provider_id)
        REFERENCES provider(id)
        ON DELETE CASCADE
);

-- ✅ الجدول الوسيط (The Pivot Table)
--fix problem ( sign up : category)
CREATE TABLE provider_category (
    provider_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    PRIMARY KEY (provider_id, category_id),
    
    CONSTRAINT fk_pc_provider 
        FOREIGN KEY (provider_id) 
        REFERENCES provider(id) 
        ON DELETE CASCADE,
        
    CONSTRAINT fk_pc_category 
        FOREIGN KEY (category_id) 
        REFERENCES service_category(id) 
        ON DELETE CASCADE
);


-- ================================================================
-- MODULE AVIS
-- ================================================================

CREATE TABLE avis (
    id                   BIGSERIAL PRIMARY KEY,
    client_id            BIGINT NOT NULL
                             REFERENCES users(id)    ON DELETE CASCADE,
    prestataire_id       BIGINT NOT NULL
                             REFERENCES provider(id) ON DELETE CASCADE,
    service_id           BIGINT
                             REFERENCES service(id)  ON DELETE SET NULL,
    commentaire          TEXT    NOT NULL,
    note_globale         INTEGER NOT NULL CHECK (note_globale      BETWEEN 1 AND 5),
    note_prix            INTEGER          CHECK (note_prix         BETWEEN 1 AND 5),
    note_qualite         INTEGER          CHECK (note_qualite      BETWEEN 1 AND 5),
    note_rapidite        INTEGER          CHECK (note_rapidite     BETWEEN 1 AND 5),
    note_communication   INTEGER          CHECK (note_communication BETWEEN 1 AND 5),
    is_verified_purchase BOOLEAN   DEFAULT FALSE,
    is_anonymous         BOOLEAN   DEFAULT FALSE,
    is_edited            BOOLEAN   DEFAULT FALSE,
    is_deleted           BOOLEAN   DEFAULT FALSE,
    helpful_count        INTEGER   DEFAULT 0,
    report_count         INTEGER   DEFAULT 0,
    reply_count          INTEGER   DEFAULT 0,
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE avis_reponses (
    id             BIGSERIAL PRIMARY KEY,
    avis_id        BIGINT NOT NULL REFERENCES avis(id)  ON DELETE CASCADE,
    user_id        BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    contenu        TEXT NOT NULL,
    is_prestataire BOOLEAN   DEFAULT FALSE,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE avis_helpful (
    id         BIGSERIAL PRIMARY KEY,
    avis_id    BIGINT NOT NULL REFERENCES avis(id)  ON DELETE CASCADE,
    user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (avis_id, user_id)
);

CREATE TABLE avis_reports (
    avis_id     BIGINT NOT NULL REFERENCES avis(id)  ON DELETE CASCADE,
    id          BIGSERIAL PRIMARY KEY,
    reporter_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reason      report_reason NOT NULL,
    description TEXT,
    status      VARCHAR(20)   DEFAULT 'pending',
    created_at  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE moderation_queue (
    id           BIGSERIAL PRIMARY KEY,
    avis_id      BIGINT    REFERENCES avis(id)  ON DELETE CASCADE,
    reason       VARCHAR(50),
    status       VARCHAR(20) DEFAULT 'pending',
    moderated_by BIGINT      REFERENCES users(id),
    moderated_at TIMESTAMP,
    created_at   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE avis_ai_analysis (
    id              BIGSERIAL PRIMARY KEY,
    avis_id         BIGINT UNIQUE NOT NULL REFERENCES avis(id) ON DELETE CASCADE,
    sentiment       VARCHAR(20) CHECK (sentiment IN ('positif', 'neutre', 'negatif')),
    sentiment_score NUMERIC(4,3),
    keywords        TEXT[],
    toxicity_score  NUMERIC(4,3),
    analyzed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE avis_medias (
    id            BIGSERIAL PRIMARY KEY,
    avis_id       BIGINT NOT NULL REFERENCES avis(id) ON DELETE CASCADE,
    media_type    media_type NOT NULL,
    file_url      TEXT NOT NULL,
    thumbnail_url TEXT,
    upload_order  INTEGER   DEFAULT 0,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trust_scores (
    id               BIGSERIAL PRIMARY KEY,
    prestataire_id   BIGINT UNIQUE NOT NULL
                         REFERENCES provider(id) ON DELETE CASCADE,
    trust_score      NUMERIC(5,2) DEFAULT 0
                         CHECK (trust_score BETWEEN 0 AND 100),
    total_reviews    INTEGER      DEFAULT 0,
    positive_reviews INTEGER      DEFAULT 0,
    neutral_reviews  INTEGER      DEFAULT 0,
    negative_reviews INTEGER      DEFAULT 0,
    avg_rating       NUMERIC(3,2) DEFAULT 0,
    verified_reviews INTEGER      DEFAULT 0,
    response_rate    NUMERIC(5,2) DEFAULT 0,
    report_count     INTEGER      DEFAULT 0,
    trust_level      trust_level  GENERATED ALWAYS AS (
        CASE
            WHEN trust_score >= 90 THEN 'EXCELLENT'   ::trust_level
            WHEN trust_score >= 75 THEN 'TRES_FIABLE' ::trust_level
            WHEN trust_score >= 60 THEN 'FIABLE'      ::trust_level
            WHEN trust_score >= 40 THEN 'A_SURVEILLER'::trust_level
            WHEN trust_score >= 20 THEN 'RISQUE'      ::trust_level
            ELSE                        'NOUVEAU'     ::trust_level
        END
    ) STORED,
    last_calculated  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ================================================================
-- MODULE MESSAGES
-- ================================================================

CREATE TABLE messages (
    id_msg              BIGSERIAL PRIMARY KEY,
    receiver_id         BIGINT NOT NULL,
    sender_id           BIGINT NOT NULL,
    content             TEXT NOT NULL,
    sent_time           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at             TIMESTAMP,
    deleted_by_receiver BOOLEAN   DEFAULT FALSE,
    deleted_by_sender   BOOLEAN   DEFAULT FALSE,
    delete_time         TIMESTAMP,

    CONSTRAINT fk_msg_receiver
        FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT fk_msg_sender
        FOREIGN KEY (sender_id)   REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT chk_no_self_message
        CHECK (sender_id <> receiver_id)
);


-- ================================================================
-- MODULE DEMANDEUR  (nouvelle version)
-- ================================================================

-- 1. Commune (42 communes de la wilaya de Tiaret)
CREATE TABLE commune (
    id     BIGSERIAL PRIMARY KEY,
    name   VARCHAR(100) NOT NULL,
    code   VARCHAR(10),
    wilaya VARCHAR(50)  DEFAULT 'Tiaret'
);

INSERT INTO commune (name, code) VALUES
    ('Tiaret',                          '14001'),
    ('Sougueur',                        '14002'),
    ('Frenda',                          '14003'),
    ('Mahdia',                          '14004'),
    ('Rahouia',                         '14005'),
    ('Ksar Chellala',                   '14006'),
    ('Ain Deheb',                       '14007'),
    ('Medrissa',                        '14008'),
    ('Zmalet El Amir Abdelkader',       '14009'),
    ('Dahmouni',                        '14010'),
    ('Sidi Bakhti',                     '14011'),
    ('Guertoufa',                       '14012'),
    ('Hamadia',                         '14013'),
    ('Ain Kermes',                      '14014'),
    ('Oued Lilli',                      '14015'),
    ('Madna',                           '14016'),
    ('Bougara',                         '14017'),
    ('Sidi Ali Mellal',                 '14018'),
    ('Rechaiga',                        '14019'),
    ('Ain Dzarit',                      '14020'),
    ('Tagdempt',                        '14021'),
    ('Djillali Ben Amar',               '14022'),
    ('Sidi Hosni',                      '14023'),
    ('Sebt',                            '14024'),
    ('Mellakou',                        '14025'),
    ('Chehaima',                        '14026'),
    ('Takhemaret',                      '14027'),
    ('Tousnina',                        '14028'),
    ('Meghila',                         '14029'),
    ('Serghine',                        '14030'),
    ('Ain El Hadid',                    '14031'),
    ('Ouled Djilali',                   '14032'),
    ('Sidi Abderrahmane',               '14033'),
    ('Naima',                           '14034'),
    ('Ain Bouchekif',                   '14035'),
    ('Faidja',                          '14036'),
    ('Si Abdelghani',                   '14037'),
    ('Tidda',                           '14038'),
    ('Mechraa Safa',                    '14039'),
    ('Ain El Assel',                    '14040'),
    ('Nahr Ouassel',                    '14041'),
    ('Bekira',                          '14042');


-- 2. Demandeur
CREATE TABLE demandeur (
    id                BIGSERIAL PRIMARY KEY,
    user_id           BIGINT NOT NULL UNIQUE,
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    phone             VARCHAR(50),
    profile_image_url TEXT,
    status            account_status DEFAULT 'ACTIVE',
    location_id       BIGINT,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_demandeur_user
        FOREIGN KEY (user_id)     REFERENCES users(id)    ON DELETE CASCADE,

    CONSTRAINT fk_demandeur_location
        FOREIGN KEY (location_id) REFERENCES location(id)
);


-- 3. Demande
CREATE TABLE demande (
    id           BIGSERIAL PRIMARY KEY,
    reference    VARCHAR(50) UNIQUE NOT NULL,

    demandeur_id BIGINT NOT NULL,
    provider_id  BIGINT NOT NULL,
    service_id   BIGINT NOT NULL,

    address      TEXT,
    commune_id   BIGINT,
    desired_date DATE,
    description  TEXT,

    total_amount DOUBLE PRECISION DEFAULT 0,
    status       demande_status   DEFAULT 'PENDING',

    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_demande_demandeur
        FOREIGN KEY (demandeur_id) REFERENCES demandeur(id),

    CONSTRAINT fk_demande_provider
        FOREIGN KEY (provider_id)  REFERENCES provider(id),

    CONSTRAINT fk_demande_service
        FOREIGN KEY (service_id)   REFERENCES service(id),

    CONSTRAINT fk_demande_commune
        FOREIGN KEY (commune_id)   REFERENCES commune(id)
);


-- 4. Demande_task
CREATE TABLE demande_task (
    id         BIGSERIAL PRIMARY KEY,
    demande_id BIGINT  NOT NULL,
    task_id    BIGINT  NOT NULL,
    quantity   INTEGER NOT NULL DEFAULT 1,
    unit_price DOUBLE PRECISION NOT NULL,
    subtotal   DOUBLE PRECISION GENERATED ALWAYS AS (quantity * unit_price) STORED,

    CONSTRAINT fk_dt_demande
        FOREIGN KEY (demande_id) REFERENCES demande(id) ON DELETE CASCADE,

    CONSTRAINT fk_dt_task
        FOREIGN KEY (task_id)    REFERENCES task(id),

    CONSTRAINT uq_demande_task UNIQUE (demande_id, task_id)
);


-- 5. Negotiation
CREATE TABLE negotiation (
    id              BIGSERIAL PRIMARY KEY,
    demande_id      BIGINT NOT NULL UNIQUE,
    proposed_budget DOUBLE PRECISION NOT NULL,
    message         TEXT,
    counter_budget  DOUBLE PRECISION,
    counter_message TEXT,
    status          negotiation_status DEFAULT 'PENDING',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_nego_demande
        FOREIGN KEY (demande_id) REFERENCES demande(id) ON DELETE CASCADE
);


-- ================================================================
-- MODULE PARAMÈTRES SYSTÈME
-- ================================================================

CREATE TABLE parametres (
    id          SERIAL PRIMARY KEY,
    cle         VARCHAR(100) UNIQUE NOT NULL,
    valeur      TEXT,
    description TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO parametres (cle, valeur, description) VALUES
    ('delai_reponse_heures', '24',                       'Délai max de réponse pour un prestataire (heures)'),
    ('frais_deplacement',    '0',                         'Frais de déplacement par défaut (DA)'),
    ('tva_taux',             '19',                        'Taux de TVA en pourcentage'),
    ('version_app',          '1.0.0',                     'Version actuelle de l''application'),
    ('maintenance_mode',     'false',                     'Mode maintenance (true/false)'),
    ('email_contact',        'contact@servicetiarit.dz',  'Email de contact général'),
    ('telephone_support',    '0555 12 34 56',             'Numéro de téléphone du support')
ON CONFLICT (cle) DO NOTHING;


-- ================================================================
-- INDEXES
-- ================================================================

-- Authentication
CREATE INDEX idx_user_email        ON users(email);
CREATE INDEX idx_refresh_user      ON refresh_token(user_id);
CREATE INDEX idx_session_user      ON session(user_id);
CREATE INDEX idx_login_attempt_user ON login_attempt(user_id);

-- Provider
CREATE INDEX idx_provider_user ON provider(user_id);
CREATE INDEX idx_provider_category_pivot ON provider_category(category_id);
CREATE INDEX idx_service_provider ON service(provider_id);
CREATE INDEX idx_service_category ON service(category_id);
CREATE INDEX idx_task_service ON task(service_id);
CREATE INDEX idx_portfolio_provider ON portfolio_image(provider_id);

-- Avis
CREATE INDEX idx_avis_client         ON avis(client_id);
CREATE INDEX idx_avis_prestataire    ON avis(prestataire_id);
CREATE INDEX idx_avis_service        ON avis(service_id);
CREATE INDEX idx_avis_note           ON avis(note_globale);
CREATE INDEX idx_avis_created        ON avis(created_at DESC);
CREATE INDEX idx_avis_helpful        ON avis(helpful_count DESC);
CREATE INDEX idx_avis_verified       ON avis(is_verified_purchase);
CREATE INDEX idx_avis_deleted        ON avis(is_deleted) WHERE is_deleted = FALSE;
CREATE INDEX idx_avis_medias         ON avis_medias(avis_id);
CREATE INDEX idx_avis_reponses_avis  ON avis_reponses(avis_id);
CREATE INDEX idx_avis_reponses_user  ON avis_reponses(user_id);
CREATE INDEX idx_avis_helpful_avis   ON avis_helpful(avis_id);
CREATE INDEX idx_avis_helpful_user   ON avis_helpful(user_id);
CREATE INDEX idx_avis_reports_avis   ON avis_reports(avis_id);
CREATE INDEX idx_avis_reports_status ON avis_reports(status);
CREATE INDEX idx_moderation_status   ON moderation_queue(status);
CREATE INDEX idx_moderation_avis     ON moderation_queue(avis_id) WHERE avis_id IS NOT NULL;
CREATE INDEX idx_ai_avis             ON avis_ai_analysis(avis_id);
CREATE INDEX idx_ai_sentiment        ON avis_ai_analysis(sentiment);
CREATE INDEX idx_trust_prestataire   ON trust_scores(prestataire_id);
CREATE INDEX idx_trust_score         ON trust_scores(trust_score DESC);
CREATE INDEX idx_trust_level         ON trust_scores(trust_level);

-- Messages
CREATE INDEX idx_sender   ON messages(sender_id);
CREATE INDEX idx_receiver ON messages(receiver_id);
CREATE INDEX idx_read_at  ON messages(read_at);

-- Demandeur
CREATE INDEX idx_demandeur_user       ON demandeur(user_id);
CREATE INDEX idx_demande_demandeur    ON demande(demandeur_id);
CREATE INDEX idx_demande_provider     ON demande(provider_id);
CREATE INDEX idx_demande_service      ON demande(service_id);
CREATE INDEX idx_demande_status       ON demande(status);
CREATE INDEX idx_demande_task_demande ON demande_task(demande_id);
CREATE INDEX idx_nego_demande         ON negotiation(demande_id);
CREATE INDEX idx_commune_wilaya       ON commune(wilaya);


-- ================================================================
-- TRIGGERS & FONCTIONS
-- ================================================================

-- Fonction générique : mise à jour automatique de updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_demandeur_updated_at
    BEFORE UPDATE ON demandeur
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_demande_updated_at
    BEFORE UPDATE ON demande
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_negotiation_updated_at
    BEFORE UPDATE ON negotiation
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_parametres_updated_at
    BEFORE UPDATE ON parametres
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- Trigger : mise à jour automatique de demande.total_amount
CREATE OR REPLACE FUNCTION update_demande_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE demande
    SET total_amount = (
        SELECT COALESCE(SUM(subtotal), 0)
        FROM demande_task
        WHERE demande_id = COALESCE(NEW.demande_id, OLD.demande_id)
    )
    WHERE id = COALESCE(NEW.demande_id, OLD.demande_id);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_demande_total
    AFTER INSERT OR UPDATE OR DELETE ON demande_task
    FOR EACH ROW EXECUTE FUNCTION update_demande_total();


-- Trigger : helpful_count sur avis
CREATE OR REPLACE FUNCTION update_avis_helpful_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE avis SET helpful_count = helpful_count + 1
        WHERE id = NEW.avis_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE avis SET helpful_count = GREATEST(helpful_count - 1, 0)
        WHERE id = OLD.avis_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_avis_helpful
    AFTER INSERT OR DELETE ON avis_helpful
    FOR EACH ROW EXECUTE FUNCTION update_avis_helpful_count();


-- Trigger : reply_count sur avis
CREATE OR REPLACE FUNCTION update_avis_reply_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE avis SET reply_count = reply_count + 1
        WHERE id = NEW.avis_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE avis SET reply_count = GREATEST(reply_count - 1, 0)
        WHERE id = OLD.avis_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_avis_reply
    AFTER INSERT OR DELETE ON avis_reponses
    FOR EACH ROW EXECUTE FUNCTION update_avis_reply_count();


-- Trigger : updated_at sur avis
CREATE TRIGGER trigger_avis_updated_at
    BEFORE UPDATE ON avis
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- Trigger : trust_score automatique
CREATE OR REPLACE FUNCTION update_trust_score()
RETURNS TRIGGER AS $$
DECLARE
    v_prestataire_id BIGINT;
    v_total          INTEGER;
    v_moyenne        NUMERIC;
    v_positifs       INTEGER;
    v_neutres        INTEGER;
    v_negatifs       INTEGER;
    v_verifies       INTEGER;
    v_score          NUMERIC;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_prestataire_id := OLD.prestataire_id;
    ELSE
        v_prestataire_id := NEW.prestataire_id;
    END IF;

    SELECT
        COUNT(*)         FILTER (WHERE is_deleted = FALSE),
        COALESCE(AVG(note_globale) FILTER (WHERE is_deleted = FALSE), 0),
        COUNT(*)         FILTER (WHERE note_globale >= 4 AND is_deleted = FALSE),
        COUNT(*)         FILTER (WHERE note_globale =  3 AND is_deleted = FALSE),
        COUNT(*)         FILTER (WHERE note_globale <= 2 AND is_deleted = FALSE),
        COUNT(*)         FILTER (WHERE is_verified_purchase = TRUE AND is_deleted = FALSE)
    INTO v_total, v_moyenne, v_positifs, v_neutres, v_negatifs, v_verifies
    FROM avis
    WHERE prestataire_id = v_prestataire_id;

    v_score :=
        (v_moyenne * 8)
        + LEAST(v_total, 30)
        + CASE WHEN v_total > 0
               THEN (v_positifs * 30.0 / v_total)
               ELSE 0
          END;

    v_score := LEAST(v_score, 100);

    INSERT INTO trust_scores (
        prestataire_id, total_reviews, positive_reviews,
        neutral_reviews, negative_reviews,
        avg_rating, verified_reviews,
        trust_score, last_calculated
    ) VALUES (
        v_prestataire_id, v_total, v_positifs,
        v_neutres, v_negatifs,
        ROUND(v_moyenne, 2), v_verifies,
        ROUND(v_score, 2), CURRENT_TIMESTAMP
    )
    ON CONFLICT (prestataire_id) DO UPDATE SET
        total_reviews    = EXCLUDED.total_reviews,
        positive_reviews = EXCLUDED.positive_reviews,
        neutral_reviews  = EXCLUDED.neutral_reviews,
        negative_reviews = EXCLUDED.negative_reviews,
        avg_rating       = EXCLUDED.avg_rating,
        verified_reviews = EXCLUDED.verified_reviews,
        trust_score      = EXCLUDED.trust_score,
        last_calculated  = EXCLUDED.last_calculated;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_trust_score
    AFTER INSERT OR UPDATE OR DELETE ON avis
    FOR EACH ROW EXECUTE FUNCTION update_trust_score();


-- Fonction : génération de référence de demande (BC-YYYYMM-XXXX)
CREATE OR REPLACE FUNCTION generer_reference()
RETURNS TEXT AS $$
DECLARE
    nouvelle_ref TEXT;
    annee        TEXT;
    mois         TEXT;
    seq          INT;
BEGIN
    annee := TO_CHAR(CURRENT_DATE, 'YYYY');
    mois  := TO_CHAR(CURRENT_DATE, 'MM');

    SELECT COALESCE(
        MAX(CAST(SUBSTRING(reference FROM '-([0-9]+)$') AS INTEGER)), 0
    ) + 1
    INTO seq
    FROM demande
    WHERE reference LIKE 'BC-' || annee || mois || '-%';

    nouvelle_ref := 'BC-' || annee || mois || '-' || LPAD(seq::TEXT, 4, '0');
    RETURN nouvelle_ref;
END;
$$ LANGUAGE plpgsql;


-- ================================================================
-- VUES
-- ================================================================

CREATE OR REPLACE VIEW view_avis_complet AS
SELECT
    a.id,
    a.commentaire,
    a.note_globale,
    a.note_prix,
    a.note_qualite,
    a.note_rapidite,
    a.note_communication,
    a.is_verified_purchase,
    a.is_anonymous,
    a.is_edited,
    a.helpful_count,
    a.reply_count,
    a.created_at,
    a.updated_at,
    u.id                                     AS client_id,
    u.username                               AS client_username,
    p.id                                     AS prestataire_id,
    p.first_name || ' ' || p.last_name       AS prestataire_nom,
    s.id                                     AS service_id,
    s.title                                  AS service_titre,
    (SELECT COUNT(*) FROM avis_medias WHERE avis_id = a.id) AS media_count,
    ts.trust_score,
    ts.trust_level,
    ai.sentiment                             AS ai_sentiment,
    ai.keywords                              AS ai_keywords
FROM avis a
JOIN  users            u  ON a.client_id      = u.id
JOIN  provider         p  ON a.prestataire_id = p.id
LEFT JOIN service      s  ON a.service_id     = s.id
LEFT JOIN trust_scores ts ON p.id             = ts.prestataire_id
LEFT JOIN avis_ai_analysis ai ON a.id         = ai.avis_id
WHERE a.is_deleted = FALSE;


CREATE OR REPLACE VIEW view_stats_prestataire AS
SELECT
    p.id,
    p.first_name || ' ' || p.last_name       AS contact,
    p.is_verified,
    p.created_at                             AS date_inscription,
    COUNT(a.id)                              AS total_avis,
    ROUND(COALESCE(AVG(a.note_globale), 0)::NUMERIC, 2) AS note_moyenne,
    COUNT(CASE WHEN a.note_globale >= 4 THEN 1 END)     AS avis_positifs,
    COUNT(CASE WHEN a.note_globale =  3 THEN 1 END)     AS avis_neutres,
    COUNT(CASE WHEN a.note_globale <= 2 THEN 1 END)     AS avis_negatifs,
    ROUND(
        COUNT(CASE WHEN a.note_globale >= 4 THEN 1 END) * 100.0
        / NULLIF(COUNT(a.id), 0),
    2)                                       AS taux_satisfaction,
    ts.trust_score,
    ts.trust_level,
    CASE ts.trust_level
        WHEN 'EXCELLENT'    THEN 'Prestataire de confiance'
        WHEN 'TRES_FIABLE'  THEN 'Tres fiable'
        WHEN 'FIABLE'       THEN 'Fiable'
        WHEN 'A_SURVEILLER' THEN 'A surveiller'
        WHEN 'RISQUE'       THEN 'Risque'
        ELSE                     'Nouveau prestataire'
    END                                      AS badge_confiance
FROM provider p
LEFT JOIN avis         a  ON p.id = a.prestataire_id AND a.is_deleted = FALSE
LEFT JOIN trust_scores ts ON p.id = ts.prestataire_id
GROUP BY
    p.id, p.first_name, p.last_name,
    p.is_verified, p.created_at,
    ts.trust_score, ts.trust_level;


CREATE OR REPLACE VIEW view_top_prestataires AS
SELECT
    p.id,
    p.first_name || ' ' || p.last_name       AS contact,
    ts.trust_score,
    ts.trust_level,
    ts.total_reviews,
    ts.avg_rating,
    RANK() OVER (ORDER BY ts.trust_score DESC) AS rang
FROM provider p
JOIN trust_scores ts ON p.id = ts.prestataire_id
WHERE ts.total_reviews >= 3
ORDER BY ts.trust_score DESC
LIMIT 100;


CREATE OR REPLACE VIEW vue_demandes_details AS
SELECT
    d.id                                        AS demande_id,
    d.reference,
    d.status,
    d.created_at,
    d.address,
    c.name                                      AS commune,
    d.desired_date,
    d.total_amount,
    dem.first_name || ' ' || dem.last_name      AS demandeur_nom,
    p.first_name  || ' ' || p.last_name         AS provider_nom,
    p.phone                                     AS provider_telephone,
    COUNT(dt.id)                                AS nb_taches,
    COALESCE(SUM(dt.subtotal), 0)               AS total_calcule
FROM demande d
LEFT JOIN demandeur    dem ON d.demandeur_id = dem.id
LEFT JOIN provider     p   ON d.provider_id  = p.id
LEFT JOIN commune      c   ON d.commune_id   = c.id
LEFT JOIN demande_task dt  ON d.id           = dt.demande_id
GROUP BY d.id, dem.id, p.id, c.id
ORDER BY d.created_at DESC;



--================
--INSERTION
--================


 
-- ================================================================
-- 1. ROLE
-- ================================================================
INSERT INTO role (name, description) VALUES
    ('ADMIN',     'Administrateur système avec tous les droits'),
    ('PROVIDER',  'Prestataire de services'),
    ('DEMANDEUR', 'Demandeur de services');


-- ================================================================
-- 2. PERMISSION
-- ================================================================
INSERT INTO permission (code_name, description, module) VALUES
    ('USER_CREATE',       'Créer un utilisateur',           'AUTH'),
    ('USER_DELETE',       'Supprimer un utilisateur',       'AUTH'),
    ('USER_VIEW',         'Voir les utilisateurs',          'AUTH'),
    ('SERVICE_MANAGE',    'Gérer les services',             'PROVIDER'),
    ('AVIS_MODERATE',     'Modérer les avis',               'AVIS'),
    ('DEMANDE_MANAGE',    'Gérer les demandes',             'DEMANDEUR'),
    ('MESSAGE_VIEW_ALL',  'Voir tous les messages',         'MESSAGES'),
    ('REPORT_VIEW',       'Voir les signalements',          'AVIS');


-- ================================================================
-- 3. USERS
-- ================================================================
INSERT INTO users (username, email, hashed_password, phone_number, role_id, is_active) VALUES
    ('admin_sys',     'admin@servicetiarit.dz',      '$2a$10$HASHEDPASSWORD001', '0550000001', 1, TRUE),
    ('karim_prest',   'karim.provider@email.com',    '$2a$10$HASHEDPASSWORD002', '0661112233', 2, TRUE),
    ('sara_prest',    'sara.provider@email.com',     '$2a$10$HASHEDPASSWORD003', '0662223344', 2, TRUE),
    ('ali_demandeur', 'ali.demandeur@email.com',     '$2a$10$HASHEDPASSWORD004', '0773334455', 3, TRUE),
    ('nadia_client',  'nadia.client@email.com',      '$2a$10$HASHEDPASSWORD005', '0774445566', 3, TRUE);


-- ================================================================
-- 4. ROLE_PERMISSION
-- ================================================================
INSERT INTO role_permission (role_id, permission_id) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
    (2, 4),
    (3, 6);


-- ================================================================
-- 5. REFRESH_TOKEN
-- ================================================================
INSERT INTO refresh_token (user_id, token_hash, expires_at, revoked) VALUES
    (2, 'hash_token_karim_001',  NOW() + INTERVAL '7 days', FALSE),
    (3, 'hash_token_sara_001',   NOW() + INTERVAL '7 days', FALSE),
    (4, 'hash_token_ali_001',    NOW() + INTERVAL '7 days', FALSE),
    (5, 'hash_token_nadia_001',  NOW() + INTERVAL '7 days', FALSE);


-- ================================================================
-- 6. SESSION
-- ================================================================
INSERT INTO session (user_id, session_token_hash, ip_address, user_agent, expires_at) VALUES
    (2, 'sess_hash_karim_001', '192.168.1.10', 'Mozilla/5.0 Android',  NOW() + INTERVAL '1 day'),
    (3, 'sess_hash_sara_001',  '192.168.1.11', 'Mozilla/5.0 iPhone',   NOW() + INTERVAL '1 day'),
    (4, 'sess_hash_ali_001',   '192.168.1.20', 'Mozilla/5.0 Windows',  NOW() + INTERVAL '1 day'),
    (5, 'sess_hash_nadia_001', '192.168.1.21', 'Mozilla/5.0 Android',  NOW() + INTERVAL '1 day');


-- ================================================================
-- 7. PASSWORD_RESET
-- ================================================================
INSERT INTO password_reset (user_id, reset_token_hash, expires_at, used) VALUES
    (4, 'reset_hash_ali_001',   NOW() + INTERVAL '1 hour', FALSE),
    (5, 'reset_hash_nadia_001', NOW() - INTERVAL '2 hour', TRUE);


-- ================================================================
-- 8. EMAIL_VERIFICATION
-- ================================================================
INSERT INTO email_verification (user_id, verification_token_hash, verified, expires_at) VALUES
    (2, 'verif_hash_karim_001', TRUE,  NOW() - INTERVAL '10 days'),
    (3, 'verif_hash_sara_001',  TRUE,  NOW() - INTERVAL '8 days'),
    (4, 'verif_hash_ali_001',   TRUE,  NOW() - INTERVAL '5 days'),
    (5, 'verif_hash_nadia_001', FALSE, NOW() + INTERVAL '1 day');


-- ================================================================
-- 9. LOGIN_ATTEMPT
-- ================================================================
INSERT INTO login_attempt (user_id, ip_address, success, attempt_time) VALUES
    (2, '192.168.1.10', TRUE,  NOW() - INTERVAL '2 hours'),
    (4, '192.168.1.20', FALSE, NOW() - INTERVAL '3 hours'),
    (4, '192.168.1.20', TRUE,  NOW() - INTERVAL '3 hours'),
    (5, '192.168.1.21', TRUE,  NOW() - INTERVAL '1 hour');


-- ================================================================
-- 10. USER_MFA
-- ================================================================
INSERT INTO user_mfa (user_id, secret_key, enabled) VALUES
    (1, 'MFA_SECRET_ADMIN_001', TRUE),
    (2, 'MFA_SECRET_KARIM_001', FALSE);


-- ================================================================
-- 11. AUDIT_LOG
-- ================================================================
INSERT INTO audit_log (user_id, action, entity, entity_id, ip_address) VALUES
    (1, 'CREATE_USER',    'users',   2, '10.0.0.1'),
    (1, 'CREATE_USER',    'users',   3, '10.0.0.1'),
    (2, 'UPDATE_SERVICE', 'service', 1, '192.168.1.10');


-- ================================================================
-- 12. LOCATION
-- ================================================================
INSERT INTO location (city, address, region) VALUES
    ('Tiaret',        'Rue  du Frigo ',    'Tiaret'),
    ('Tiaret',        'Cité La Cadat ',  'Tiaret'),
    ('Frenda',        'Rue du 1er Novembre',          'Tiaret'),
    ('Sougueur',      'Avenue de l''indépendance',    'Tiaret'),
    ('Mahdia',        'Rue Boite postale',             'Tiaret');


-- ================================================================
-- 13. SERVICE_CATEGORY
-- ================================================================
INSERT INTO service_category (name) VALUES
    ('Plomberie'),
    ('Électricité'),
    ('Peinture'),
    ('Menuiserie'),
    ('Climatisation'),
    ('Nettoyage'),
    ('Maçonnerie'),
    ('Jardinage');


-- ================================================================
-- 14. PROVIDER
-- ================================================================
INSERT INTO provider (user_id, first_name, last_name, phone, bio, is_verified, experience_years, status, location_id) VALUES
    (2, 'Karim',  'Benali',   '0661112233', 'Plombier professionnel avec 10 ans d''expérience à Tiaret.', TRUE,  10, 'ACTIVE', 1),
    (3, 'Sara',   'Hammadi',  '0662223344', 'Électricienne certifiée, spécialisée en installations domestiques.', TRUE, 6, 'ACTIVE', 2);


-- ================================================================
-- 15. SERVICE
-- ================================================================
INSERT INTO service (provider_id, title, description, status, price, currency, category_id, is_active, publication_date) VALUES
    (1, 'Réparation fuite d''eau',       'Détection et réparation de fuites d''eau tous types de canalisations.', 'PUBLISHED', 2500.00, 'DZD', 1, TRUE, NOW()),
    (1, 'Installation sanitaire',         'Installation complète de sanitaires (WC, lavabo, douche).',            'PUBLISHED', 8000.00, 'DZD', 1, TRUE, NOW()),
    (2, 'Installation électrique neuve',  'Mise en place d''un tableau électrique et câblage complet.',           'PUBLISHED', 15000.00,'DZD', 2, TRUE, NOW()),
    (2, 'Dépannage électrique urgent',    'Intervention rapide pour pannes électriques domestiques.',              'PUBLISHED', 1500.00, 'DZD', 2, TRUE, NOW());


-- ================================================================
-- 16. TASK
-- ================================================================
INSERT INTO task (service_id, name, description, duration, price, mandatory) VALUES
    (1, 'Diagnostic fuite',       'Localisation précise de la fuite',          30,  500.00, TRUE),
    (1, 'Remplacement joint',     'Remplacement des joints défectueux',         45,  800.00, TRUE),
    (1, 'Remplacement tuyau',     'Remplacement d''un tronçon de tuyau',       120, 1500.00, FALSE),
    (2, 'Pose WC',                'Installation et fixation du WC',             90, 2000.00, TRUE),
    (2, 'Pose lavabo',            'Installation et raccordement du lavabo',     60, 1500.00, FALSE),
    (3, 'Pose tableau électrique','Installation du tableau de distribution',    180, 5000.00, TRUE),
    (3, 'Câblage pièces',         'Câblage électrique par pièce',              120, 2500.00, TRUE),
    (4, 'Diagnostic panne',       'Identification de la panne électrique',      30,  500.00, TRUE),
    (4, 'Réparation câblage',     'Réparation du câble ou du composant défectueux', 60, 800.00, FALSE);


-- ================================================================
-- 17. PORTFOLIO_IMAGE
-- ================================================================
INSERT INTO portfolio_image (provider_id, image_url) VALUES
    (1, 'https://storage.servicetiarit.dz/portfolio/karim_01.jpg'),
    (1, 'https://storage.servicetiarit.dz/portfolio/karim_02.jpg'),
    (2, 'https://storage.servicetiarit.dz/portfolio/sara_01.jpg'),
    (2, 'https://storage.servicetiarit.dz/portfolio/sara_02.jpg');


 

-- ================================================================
-- 19. AVIS
-- ================================================================
INSERT INTO avis (client_id, prestataire_id, service_id, commentaire, note_globale, note_prix, note_qualite, note_rapidite, note_communication, is_verified_purchase, is_anonymous) VALUES
    (4, 1, 1, 'Excellent travail, karim est très professionnel et rapide. Je recommande vivement.', 5, 4, 5, 5, 5, TRUE,  FALSE),
    (5, 1, 2, 'Bonne installation, propre et soignée. Prix raisonnable.',                           4, 4, 4, 3, 4, TRUE,  FALSE),
    (4, 2, 3, 'Installation électrique parfaite, Sara explique bien chaque étape.',                 5, 5, 5, 4, 5, TRUE,  FALSE),
    (5, 2, 4, 'Dépannage rapide, problème résolu en moins d''une heure.',                           4, 3, 4, 5, 4, TRUE,  FALSE);


-- ================================================================
-- 20. AVIS_REPONSES
-- ================================================================
INSERT INTO avis_reponses (avis_id, user_id, contenu, is_prestataire) VALUES
    (1, 2, 'Merci pour votre retour positif ! C''est un plaisir de travailler avec vous.', TRUE),
    (3, 3, 'Merci beaucoup ! La sécurité et la transparence sont mes priorités.', TRUE);


-- ================================================================
-- 21. AVIS_HELPFUL
-- ================================================================
INSERT INTO avis_helpful (avis_id, user_id) VALUES
    (1, 5),
    (3, 4),
    (3, 5);


-- ================================================================
-- 22. AVIS_REPORTS
-- ================================================================
INSERT INTO avis_reports (avis_id, reporter_id, reason, description, status) VALUES
    (4, 4, 'spam', 'Cet avis semble être posté deux fois.', 'pending');


-- ================================================================
-- 23. MODERATION_QUEUE
-- ================================================================
INSERT INTO moderation_queue (avis_id, reason, status, moderated_by) VALUES
    (4, 'doublon_suspect', 'pending', NULL);


-- ================================================================
-- 24. AVIS_AI_ANALYSIS
-- ================================================================
INSERT INTO avis_ai_analysis (avis_id, sentiment, sentiment_score, keywords, toxicity_score) VALUES
    (1, 'positif', 0.97, ARRAY['professionnel','rapide','recommande'], 0.01),
    (2, 'positif', 0.85, ARRAY['bonne','propre','raisonnable'],        0.02),
    (3, 'positif', 0.98, ARRAY['parfait','securite','transparence'],   0.00),
    (4, 'positif', 0.80, ARRAY['rapide','efficace'],                   0.01);


-- ================================================================
-- 25. AVIS_MEDIAS
-- ================================================================
INSERT INTO avis_medias (avis_id, media_type, file_url, thumbnail_url, upload_order) VALUES
    (1, 'image', 'https://storage.servicetiarit.dz/avis/1/photo1.jpg', 'https://storage.servicetiarit.dz/avis/1/thumb1.jpg', 1),
    (3, 'image', 'https://storage.servicetiarit.dz/avis/3/photo1.jpg', 'https://storage.servicetiarit.dz/avis/3/thumb1.jpg', 1),
    (3, 'video', 'https://storage.servicetiarit.dz/avis/3/video1.mp4', 'https://storage.servicetiarit.dz/avis/3/vthumb1.jpg',2);


-- ================================================================
-- 26. MESSAGES
-- ================================================================
INSERT INTO messages (receiver_id, sender_id, content, read_at) VALUES
    (2, 4, 'Bonjour Karim, est-ce que vous êtes disponible cette semaine ?',         NOW() - INTERVAL '2 hours'),
    (4, 2, 'Oui, je suis disponible mercredi et jeudi. Quel créneau vous convient ?', NOW() - INTERVAL '1 hour'),
    (3, 5, 'Bonjour Sara, j''ai une panne électrique urgente.',                       NOW() - INTERVAL '30 minutes'),
    (5, 3, 'Je peux intervenir demain matin à 9h, est-ce que cela vous convient ?',   NULL);


-- ================================================================
-- 27. DEMANDEUR
-- ================================================================
INSERT INTO demandeur (user_id, first_name, last_name, phone, status, location_id) VALUES
    (4, 'Ali',   'Khelifa',  '0773334455', 'ACTIVE', 3),
    (5, 'Nadia', 'Boualem',  '0774445566', 'ACTIVE', 4);


-- ================================================================
-- 28. DEMANDE
-- ================================================================
INSERT INTO demande (reference, demandeur_id, provider_id, service_id, address, commune_id, desired_date, description, status) VALUES
    ('BC-202604-0001', 1, 1, 1, 'Rue Bouali Ahmed N°12', 1, CURRENT_DATE + INTERVAL '3 days', 'Fuite au niveau du robinet de cuisine, urgent.',        'ACCEPTED'),
    ('BC-202604-0002', 2, 2, 3, 'Cité 1000 Logements Bt 7 Appt 3', 2, CURRENT_DATE + INTERVAL '7 days', 'Installation électrique pour appartement neuf.', 'NEGOTIATING'),
    ('BC-202604-0003', 1, 1, 2, 'Rue Frenda Centre N°5', 3, CURRENT_DATE + INTERVAL '10 days', 'Installation d''un lavabo et d''un WC dans SDB.',       'PENDING');


-- ================================================================
-- 29. DEMANDE_TASK
-- ================================================================
INSERT INTO demande_task (demande_id, task_id, quantity, unit_price) VALUES
    (1, 1, 1,  500.00),
    (1, 2, 2,  800.00),
    (2, 6, 1, 5000.00),
    (2, 7, 3, 2500.00),
    (3, 4, 1, 2000.00),
    (3, 5, 1, 1500.00);


-- ================================================================
-- 30. NEGOTIATION
-- ================================================================
INSERT INTO negotiation (demande_id, proposed_budget, message, counter_budget, counter_message, status) VALUES
    (2, 18000.00, 'Je propose 18 000 DA pour l''installation complète.', 20000.00, 'Mon tarif minimum est 20 000 DA vu la surface à câbler.', 'COUNTER');


-- ================================================================
-- FIN DES INSERTS
-- ================================================================