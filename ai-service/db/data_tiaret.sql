-- ================================================================
-- DATA_TIARET.SQL — 40 Prestataires — Wilaya de Tiaret
-- ✅ Compatible avec bdd.sql
-- ✅ Exécuter APRÈS bdd.sql (qui insère déjà roles 1,2,3 et users 1..5)
-- ================================================================


-- ================================================================
-- ÉTAPE 1 — SERVICE_CATEGORY
-- (les IDs 1..8 utilisés dans tout le fichier)
-- ================================================================
INSERT INTO service_category (name) VALUES
    ('Plomberie'),       -- id 1
    ('Electricite'),     -- id 2
    ('Peinture'),        -- id 3
    ('Menuiserie'),      -- id 4
    ('Climatisation'),   -- id 5
    ('Nettoyage'),       -- id 6
    ('Maçonnerie'),      -- id 7
    ('Jardinage')        -- id 8
ON CONFLICT (name) DO NOTHING;


-- ================================================================
-- ÉTAPE 2 — LOCATIONS (20 adresses dans les communes de Tiaret)
-- IDs générés automatiquement (suite aux locations existantes)
-- ================================================================
INSERT INTO location (city, address, region) VALUES
    ('Tiaret',        'Rue Larbi Ben Mhidi',        'Tiaret'),
    ('Tiaret',        'Cité 1000 Logements Bt 3',   'Tiaret'),
    ('Frenda',        'Rue des Martyrs',             'Tiaret'),
    ('Sougueur',      'Cité El Wiam',                'Tiaret'),
    ('Mahdia',        'Route nationale 14',          'Tiaret'),
    ('Rahouia',       'Centre ville',                'Tiaret'),
    ('Ksar Chellala', 'Rue de la République',        'Tiaret'),
    ('Ain Deheb',     'Quartier El Moustakbal',      'Tiaret'),
    ('Dahmouni',      'Rue principale',              'Tiaret'),
    ('Guertoufa',     'Cité des fonctionnaires',     'Tiaret'),
    ('Hamadia',       'Rue du 1er Novembre',         'Tiaret'),
    ('Takhemaret',    'Centre ville',                'Tiaret'),
    ('Ain Bouchekif', 'Rue Ben Badis',               'Tiaret'),
    ('Meghila',       'Route de Tiaret',             'Tiaret'),
    ('Tiaret',        'Rue Didouche Mourad',         'Tiaret'),
    ('Frenda',        'Cité OPGI',                   'Tiaret'),
    ('Ksar Chellala', 'Quartier Nord',               'Tiaret'),
    ('Tiaret',        'Rue Amirouche',               'Tiaret'),
    ('Mahdia',        'Cité El Feth',                'Tiaret'),
    ('Sougueur',      'Avenue de la Paix',           'Tiaret');


-- ================================================================
-- ÉTAPE 3 — USERS (40 comptes prestataires, role_id=2)
-- bdd.sql a déjà inséré users id 1..5
-- Ces users commenceront à partir de l'ID suivant (6+)
-- ================================================================
INSERT INTO users (username, email, hashed_password, phone_number, role_id, is_active) VALUES
('youcef_b',    'youcef.b@artisansdz.dz',    '$2a$10$HASH_001', '0661101001', 2, TRUE),
('amine_k',     'amine.k@artisansdz.dz',     '$2a$10$HASH_002', '0661101002', 2, TRUE),
('hassan_m',    'hassan.m@artisansdz.dz',    '$2a$10$HASH_003', '0661101003', 2, TRUE),
('rachid_t',    'rachid.t@artisansdz.dz',    '$2a$10$HASH_004', '0661101004', 2, TRUE),
('omar_d',      'omar.d@artisansdz.dz',      '$2a$10$HASH_005', '0661101005', 2, TRUE),
('bilal_s',     'bilal.s@artisansdz.dz',     '$2a$10$HASH_006', '0661101006', 2, TRUE),
('mourad_f',    'mourad.f@artisansdz.dz',    '$2a$10$HASH_007', '0661101007', 2, TRUE),
('khaled_z',    'khaled.z@artisansdz.dz',    '$2a$10$HASH_008', '0661101008', 2, TRUE),
('nabil_c',     'nabil.c@artisansdz.dz',     '$2a$10$HASH_009', '0661101009', 2, TRUE),
('said_b',      'said.b@artisansdz.dz',      '$2a$10$HASH_010', '0661101010', 2, TRUE),
('tarek_h',     'tarek.h@artisansdz.dz',     '$2a$10$HASH_011', '0661101011', 2, TRUE),
('walid_n',     'walid.n@artisansdz.dz',     '$2a$10$HASH_012', '0661101012', 2, TRUE),
('hichem_r',    'hichem.r@artisansdz.dz',    '$2a$10$HASH_013', '0661101013', 2, TRUE),
('sofiane_k',   'sofiane.k@artisansdz.dz',   '$2a$10$HASH_014', '0661101014', 2, TRUE),
('zakaria_m',   'zakaria.m@artisansdz.dz',   '$2a$10$HASH_015', '0661101015', 2, TRUE),
('adel_b',      'adel.b@artisansdz.dz',      '$2a$10$HASH_016', '0661101016', 2, TRUE),
('farid_t',     'farid.t@artisansdz.dz',     '$2a$10$HASH_017', '0661101017', 2, TRUE),
('lotfi_s',     'lotfi.s@artisansdz.dz',     '$2a$10$HASH_018', '0661101018', 2, TRUE),
('riad_h',      'riad.h@artisansdz.dz',      '$2a$10$HASH_019', '0661101019', 2, TRUE),
('kamel_d',     'kamel.d@artisansdz.dz',     '$2a$10$HASH_020', '0661101020', 2, TRUE),
('aissa_b',     'aissa.b@artisansdz.dz',     '$2a$10$HASH_021', '0661101021', 2, TRUE),
('djamel_f',    'djamel.f@artisansdz.dz',    '$2a$10$HASH_022', '0661101022', 2, TRUE),
('redha_k',     'redha.k@artisansdz.dz',     '$2a$10$HASH_023', '0661101023', 2, TRUE),
('salim_z',     'salim.z@artisansdz.dz',     '$2a$10$HASH_024', '0661101024', 2, TRUE),
('hamza_t',     'hamza.t@artisansdz.dz',     '$2a$10$HASH_025', '0661101025', 2, TRUE),
('zaki_m',      'zaki.m@artisansdz.dz',      '$2a$10$HASH_026', '0661101026', 2, TRUE),
('issam_n',     'issam.n@artisansdz.dz',     '$2a$10$HASH_027', '0661101027', 2, TRUE),
('malek_s',     'malek.s@artisansdz.dz',     '$2a$10$HASH_028', '0661101028', 2, TRUE),
('fares_h',     'fares.h@artisansdz.dz',     '$2a$10$HASH_029', '0661101029', 2, TRUE),
('yazid_b',     'yazid.b@artisansdz.dz',     '$2a$10$HASH_030', '0661101030', 2, TRUE),
('nassim_k',    'nassim.k@artisansdz.dz',    '$2a$10$HASH_031', '0661101031', 2, TRUE),
('mehdi_r',     'mehdi.r@artisansdz.dz',     '$2a$10$HASH_032', '0661101032', 2, TRUE),
('ramzi_d',     'ramzi.d@artisansdz.dz',     '$2a$10$HASH_033', '0661101033', 2, TRUE),
('ayoub_t',     'ayoub.t@artisansdz.dz',     '$2a$10$HASH_034', '0661101034', 2, TRUE),
('sabri_f',     'sabri.f@artisansdz.dz',     '$2a$10$HASH_035', '0661101035', 2, TRUE),
('hakim_z',     'hakim.z@artisansdz.dz',     '$2a$10$HASH_036', '0661101036', 2, TRUE),
('badr_m',      'badr.m@artisansdz.dz',      '$2a$10$HASH_037', '0661101037', 2, TRUE),
('toufik_n',    'toufik.n@artisansdz.dz',    '$2a$10$HASH_038', '0661101038', 2, TRUE),
('antar_k',     'antar.k@artisansdz.dz',     '$2a$10$HASH_039', '0661101039', 2, TRUE),
('lazhar_b',    'lazhar.b@artisansdz.dz',    '$2a$10$HASH_040', '0661101040', 2, TRUE);


-- ================================================================
-- ÉTAPE 4 — PROVIDERS
-- user_id  : les 40 users qu'on vient d'insérer
-- location_id : on utilise les IDs générés par les locations ci-dessus
-- On utilise des sous-requêtes pour éviter les IDs hardcodés
-- ================================================================
INSERT INTO provider
    (user_id, first_name, last_name, phone, bio,
     is_verified, experience_years, rating_average, trust_score,
     rating_count, status, is_available, location_id)
SELECT u.id, p.first_name, p.last_name, p.phone, p.bio,
       p.is_verified, p.exp, p.rating, p.trust,
       p.rcnt, 'ACTIVE', p.avail,
       l.id
FROM (VALUES
-- Plombiers
('youcef_b',  'Youcef',  'Boudiaf',   '0661101001', 'Plombier professionnel à Tiaret. Détection fuites et installation sanitaire.',     TRUE,  8,  4.7, 82.0, 21, TRUE,  'Tiaret',        'Rue Larbi Ben Mhidi'),
('amine_k',   'Amine',   'Kerrar',    '0661101002', 'Expert plomberie industrielle et résidentielle. Intervention rapide.',             TRUE,  5,  4.3, 71.0, 14, TRUE,  'Tiaret',        'Cité 1000 Logements Bt 3'),
('hassan_m',  'Hassan',  'Meziani',   '0661101003', 'Plombier certifié à Frenda. Fuite, WC, lavabo, douche.',                           TRUE,  10, 4.9, 94.0, 32, TRUE,  'Frenda',        'Rue des Martyrs'),
('rachid_t',  'Rachid',  'Tebboune',  '0661101004', 'Plombier à Sougueur, 7 ans expérience. Disponible 6j/7.',                          FALSE, 7,  4.1, 65.0,  9, TRUE,  'Sougueur',      'Cité El Wiam'),
('omar_d',    'Omar',    'Djebbar',   '0661101005', 'Spécialiste installation sanitaire neuve à Mahdia.',                               TRUE,  4,  3.9, 58.0,  7, FALSE, 'Mahdia',        'Route nationale 14'),
('bilal_s',   'Bilal',   'Saoudi',    '0661101006', 'Plombier à Rahouia. Tarifs compétitifs, travail soigné.',                          FALSE, 6,  4.4, 73.0, 12, TRUE,  'Rahouia',       'Centre ville'),
('mourad_f',  'Mourad',  'Ferhat',    '0661101007', 'Plombier à Ksar Chellala. Urgences acceptées.',                                    TRUE,  9,  4.6, 80.0, 18, TRUE,  'Ksar Chellala', 'Rue de la République'),
('khaled_z',  'Khaled',  'Zerrouki',  '0661101008', 'Plombier à Ain Deheb. Installation et réparation tous types.',                    FALSE, 3,  3.8, 52.0,  5, TRUE,  'Ain Deheb',     'Quartier El Moustakbal'),
-- Électriciens
('nabil_c',   'Nabil',   'Charef',    '0661101009', 'Électricien certifié à Tiaret. Tableau, câblage, dépannage urgent.',               TRUE,  7,  4.8, 88.0, 25, TRUE,  'Tiaret',        'Rue Larbi Ben Mhidi'),
('said_b',    'Said',    'Benmansour','0661101010', 'Électricien à Dahmouni. Installation neuve et réparation.',                        TRUE,  5,  4.2, 68.0, 11, TRUE,  'Dahmouni',      'Rue principale'),
('tarek_h',   'Tarek',   'Hamdi',     '0661101011', 'Électricien industriel et domestique à Tiaret. 11 ans.',                           TRUE,  11, 4.9, 95.0, 38, TRUE,  'Tiaret',        'Cité 1000 Logements Bt 3'),
('walid_n',   'Walid',   'Nasri',     '0661101012', 'Électricien à Guertoufa. Interventions rapides.',                                  FALSE, 4,  3.7, 50.0,  6, FALSE, 'Guertoufa',     'Cité des fonctionnaires'),
('hichem_r',  'Hichem',  'Rahali',    '0661101013', 'Électricien à Hamadia. Prises, interrupteurs, éclairage LED.',                    TRUE,  6,  4.5, 77.0, 16, TRUE,  'Hamadia',       'Rue du 1er Novembre'),
('sofiane_k', 'Sofiane', 'Khelifi',   '0661101014', 'Électricien à Frenda. Câblage complet appartements neufs.',                        TRUE,  8,  4.6, 81.0, 20, TRUE,  'Frenda',        'Cité OPGI'),
('zakaria_m', 'Zakaria', 'Mellouk',   '0661101015', 'Électricien à Sougueur. Dépannage et mise en conformité.',                         FALSE, 3,  3.9, 55.0,  8, TRUE,  'Sougueur',      'Avenue de la Paix'),
('adel_b',    'Adel',    'Boukhelifa','0661101016', 'Électricien à Takhemaret. Toutes installations électriques.',                     TRUE,  9,  4.7, 84.0, 22, TRUE,  'Takhemaret',    'Centre ville'),
-- Peintres
('farid_t',   'Farid',   'Touati',    '0661101017', 'Peintre décorateur à Tiaret. Intérieur, extérieur, textures.',                     TRUE,  6,  4.5, 76.0, 17, TRUE,  'Tiaret',        'Rue Amirouche'),
('lotfi_s',   'Lotfi',   'Sahraoui',  '0661101018', 'Peintre à Ksar Chellala. Travail propre et rapide.',                               FALSE, 4,  4.0, 60.0,  9, TRUE,  'Ksar Chellala', 'Quartier Nord'),
('riad_h',    'Riad',    'Hamiani',   '0661101019', 'Peintre en bâtiment à Tiaret. Façades et intérieurs.',                             TRUE,  7,  4.4, 74.0, 13, TRUE,  'Tiaret',        'Rue Didouche Mourad'),
('kamel_d',   'Kamel',   'Dahmane',   '0661101020', 'Peintre à Ain Bouchekif. Enduits, plâtre, peinture.',                             FALSE, 5,  4.1, 63.0, 10, FALSE, 'Ain Bouchekif', 'Rue Ben Badis'),
('aissa_b',   'Aissa',   'Benali',    '0661101021', 'Peintre à Mahdia. Spécialisé finitions haut de gamme.',                            TRUE,  8,  4.6, 79.0, 15, TRUE,  'Mahdia',        'Cité El Feth'),
('djamel_f',  'Djamel',  'Fergani',   '0661101022', 'Peintre à Frenda. Devis gratuit, travail garanti.',                                TRUE,  6,  4.3, 70.0, 12, TRUE,  'Frenda',        'Rue des Martyrs'),
-- Menuisiers
('redha_k',   'Redha',   'Kaddour',   '0661101023', 'Menuisier à Tiaret. Portes, fenêtres, placards sur mesure.',                      TRUE,  9,  4.7, 83.0, 19, TRUE,  'Tiaret',        'Rue Larbi Ben Mhidi'),
('salim_z',   'Salim',   'Ziani',     '0661101024', 'Menuisier aluminium et bois à Sougueur.',                                          TRUE,  6,  4.4, 72.0, 14, TRUE,  'Sougueur',      'Cité El Wiam'),
('hamza_t',   'Hamza',   'Tlemcani',  '0661101025', 'Menuisier à Frenda. Cuisines équipées et meubles.',                               FALSE, 4,  3.8, 54.0,  6, TRUE,  'Frenda',        'Cité OPGI'),
('zaki_m',    'Zaki',    'Maarouf',   '0661101026', 'Menuisier à Tiaret. Bois massif, réparation et création.',                         TRUE,  7,  4.5, 75.0, 15, TRUE,  'Tiaret',        'Cité 1000 Logements Bt 3'),
('issam_n',   'Issam',   'Nouasria',  '0661101027', 'Menuisier à Ksar Chellala. Stores, persiennes, PVC.',                             FALSE, 5,  4.0, 62.0,  9, FALSE, 'Ksar Chellala', 'Rue de la République'),
('malek_s',   'Malek',   'Saidi',     '0661101028', 'Menuisier à Dahmouni. Travaux de finition et installation.',                      TRUE,  8,  4.6, 78.0, 16, TRUE,  'Dahmouni',      'Rue principale'),
-- Climatisation
('fares_h',   'Fares',   'Hadjadj',   '0661101029', 'Technicien climatisation à Tiaret. Installation, maintenance, recharge gaz.',     TRUE,  7,  4.8, 87.0, 24, TRUE,  'Tiaret',        'Rue Amirouche'),
('yazid_b',   'Yazid',   'Bouguerra', '0661101030', 'Technicien clim à Sougueur. Toutes marques, SAV rapide.',                          TRUE,  5,  4.3, 70.0, 13, TRUE,  'Sougueur',      'Avenue de la Paix'),
('nassim_k',  'Nassim',  'Khelifi',   '0661101031', 'Installation et réparation climatiseurs à Frenda.',                               FALSE, 3,  3.9, 56.0,  7, TRUE,  'Frenda',        'Rue des Martyrs'),
('mehdi_r',   'Mehdi',   'Rahmani',   '0661101032', 'Technicien climatisation à Mahdia. Urgences acceptées.',                          TRUE,  6,  4.5, 76.0, 14, TRUE,  'Mahdia',        'Route nationale 14'),
('ramzi_d',   'Ramzi',   'Daoud',     '0661101033', 'Technicien clim à Tiaret. Froid industriel et domestique.',                        TRUE,  9,  4.7, 85.0, 20, TRUE,  'Tiaret',        'Rue Didouche Mourad'),
-- Maçonnerie
('ayoub_t',   'Ayoub',   'Toubal',    '0661101034', 'Maçon à Tiaret. Construction, rénovation, carrelage.',                             TRUE,  10, 4.6, 80.0, 18, TRUE,  'Tiaret',        'Rue Larbi Ben Mhidi'),
('sabri_f',   'Sabri',   'Ferradj',   '0661101035', 'Maçon à Rahouia. Dalle, mur, enduit, fondation.',                                 FALSE, 6,  4.1, 64.0,  9, TRUE,  'Rahouia',       'Centre ville'),
('hakim_z',   'Hakim',   'Zemouri',   '0661101036', 'Maçon à Ain Deheb. Gros œuvre et second œuvre.',                                  TRUE,  8,  4.4, 73.0, 13, FALSE, 'Ain Deheb',     'Quartier El Moustakbal'),
('badr_m',    'Badr',    'Mostefai',  '0661101037', 'Maçon à Sougueur. Rénovation complète appartements.',                             TRUE,  5,  4.2, 67.0, 11, TRUE,  'Sougueur',      'Cité El Wiam'),
-- Nettoyage
('toufik_n',  'Toufik',  'Nabi',      '0661101038', 'Nettoyage professionnel à Tiaret. Appartements, bureaux, chantiers.',             FALSE, 4,  4.0, 60.0,  8, TRUE,  'Tiaret',        'Cité 1000 Logements Bt 3'),
('antar_k',   'Antar',   'Kara',      '0661101039', 'Service nettoyage à Tiaret et Sougueur. Équipement professionnel.',               FALSE, 3,  3.8, 53.0,  6, TRUE,  'Tiaret',        'Rue Amirouche'),
-- Jardinage
('lazhar_b',  'Lazhar',  'Bensalem',  '0661101040', 'Jardinier paysagiste à Tiaret. Entretien jardins, taille, gazon.',               TRUE,  6,  4.3, 69.0, 10, TRUE,  'Tiaret',        'Rue Larbi Ben Mhidi')
) AS p(uname, first_name, last_name, phone, bio, is_verified, exp, rating, trust, rcnt, avail, city, address)
JOIN users     u ON u.username = p.uname
JOIN location  l ON l.city = p.city AND l.address = p.address;


-- ================================================================
-- ÉTAPE 5 — SERVICES (1 par prestataire)
-- ================================================================
INSERT INTO service
    (provider_id, title, description, status, price, currency,
     category_id, is_active, publication_date)
SELECT p.id, sv.title, sv.description, 'PUBLISHED',
       sv.price, 'DZD', sc.id, TRUE, NOW()
FROM (VALUES
-- Plombiers
('youcef_b',  'Réparation fuite eau',         'Détection et réparation fuites, canalisations.',        2500, 'Plomberie'),
('amine_k',   'Installation sanitaire',        'WC, lavabo, douche — installation complète.',          3000, 'Plomberie'),
('hassan_m',  'Plomberie urgence',             'Intervention urgence fuite et canalisation bouchée.',  1800, 'Plomberie'),
('rachid_t',  'Pose robinetterie',             'Remplacement et pose robinets toutes marques.',        1200, 'Plomberie'),
('omar_d',    'Réparation canalisation',       'Remplacement tronçons tuyaux endommagés.',             3500, 'Plomberie'),
('bilal_s',   'Installation chauffe-eau',      'Pose chauffe-eau électrique ou gaz.',                  4500, 'Plomberie'),
('mourad_f',  'Plomberie générale',            'Tous travaux plomberie résidentielle.',                2000, 'Plomberie'),
('khaled_z',  'Débouchage canalisations',      'Débouchage WC, lavabo, évier, douche.',                1500, 'Plomberie'),
-- Électriciens
('nabil_c',   'Câblage électrique neuf',       'Installation tableau et câblage complet appartement.', 15000,'Electricite'),
('said_b',    'Dépannage électrique urgent',   'Intervention rapide pannes électriques.',              1500, 'Electricite'),
('tarek_h',   'Installation tableau élec',     'Pose tableau de distribution et disjoncteurs.',        8000, 'Electricite'),
('walid_n',   'Pose prises et interrupteurs',  'Installation prises, interrupteurs.',                  800,  'Electricite'),
('hichem_r',  'Éclairage LED',                 'Spots, dalles LED, éclairage extérieur.',              2500, 'Electricite'),
('sofiane_k', 'Mise en conformité élec',       'Mise aux normes installation électrique.',             6000, 'Electricite'),
('zakaria_m', 'Câblage réseau informatique',   'Câbles réseau RJ45 et prises informatiques.',         3000, 'Electricite'),
('adel_b',    'Réparation court-circuit',      'Diagnostic et réparation court-circuits.',             1200, 'Electricite'),
-- Peintres
('farid_t',   'Peinture intérieure',           'Peinture murs et plafonds, toutes couleurs.',          800,  'Peinture'),
('lotfi_s',   'Peinture façade extérieure',    'Peinture et ravalement façades.',                      1200, 'Peinture'),
('riad_h',    'Décoration intérieure',         'Peinture décorative, textures, stucco.',               1500, 'Peinture'),
('kamel_d',   'Enduit et plâtre',              'Application enduit, plâtre, ratissage murs.',          600,  'Peinture'),
('aissa_b',   'Peinture boiseries',            'Peinture portes, fenêtres, volets.',                   500,  'Peinture'),
('djamel_f',  'Lasure et vernis',              'Traitement bois lasure et vernis.',                    700,  'Peinture'),
-- Menuisiers
('redha_k',   'Fabrication portes sur mesure', 'Portes intérieures bois massif sur mesure.',          12000,'Menuiserie'),
('salim_z',   'Menuiserie aluminium',          'Fenêtres, portes-fenêtres alu double vitrage.',       18000,'Menuiserie'),
('hamza_t',   'Cuisine équipée',               'Fabrication et installation cuisine bois.',           35000,'Menuiserie'),
('zaki_m',    'Placards et rangements',        'Conception et pose placards intégrés.',               15000,'Menuiserie'),
('issam_n',   'Réparation menuiserie',         'Réparation portes, fenêtres, parquet.',                2000,'Menuiserie'),
('malek_s',   'Pose parquet et stratifié',     'Pose parquet flottant, stratifié, moquette.',          900, 'Menuiserie'),
-- Climatisation
('fares_h',   'Installation climatiseur',      'Pose split toutes marques.',                           5000, 'Climatisation'),
('yazid_b',   'Maintenance climatisation',     'Entretien annuel, nettoyage.',                         2000, 'Climatisation'),
('nassim_k',  'Recharge gaz climatiseur',      'Recharge R32/R410A.',                                  3500, 'Climatisation'),
('mehdi_r',   'Réparation climatiseur',        'Diagnostic et réparation pannes.',                     2500, 'Climatisation'),
('ramzi_d',   'Installation froid commercial', 'Chambre froide, vitrine réfrigérée.',                 25000,'Climatisation'),
-- Maçonnerie
('ayoub_t',   'Rénovation complète',           'Rénovation appartement clé en main.',                 50000,'Maçonnerie'),
('sabri_f',   'Carrelage et faïence',          'Pose carrelage sol et murs.',                          1200, 'Maçonnerie'),
('hakim_z',   'Construction mur et clôture',   'Murs, clôtures, dalles béton.',                        8000, 'Maçonnerie'),
('badr_m',    'Enduit ciment et crépi',        'Application enduit ciment et crépi.',                  700,  'Maçonnerie'),
-- Nettoyage
('toufik_n',  'Nettoyage appartement',         'Nettoyage complet après travaux.',                     3000, 'Nettoyage'),
('antar_k',   'Nettoyage bureaux',             'Entretien locaux commerciaux.',                        2000, 'Nettoyage'),
-- Jardinage
('lazhar_b',  'Entretien jardin',              'Tonte, taille, désherbage.',                           2500, 'Jardinage')
) AS sv(uname, title, description, price, cat_name)
JOIN users            u  ON u.username  = sv.uname
JOIN provider         p  ON p.user_id   = u.id
JOIN service_category sc ON sc.name     = sv.cat_name;


-- ================================================================
-- ÉTAPE 6 — PROVIDER_CATEGORY
-- ================================================================
INSERT INTO provider_category (provider_id, category_id)
SELECT DISTINCT s.provider_id, s.category_id
FROM service s
JOIN provider p ON p.id = s.provider_id
JOIN users    u ON u.id = p.user_id
WHERE u.username LIKE '%_b' OR u.username LIKE '%_k'
   OR u.username LIKE '%_m' OR u.username LIKE '%_t'
   OR u.username LIKE '%_s' OR u.username LIKE '%_h'
   OR u.username LIKE '%_f' OR u.username LIKE '%_d'
   OR u.username LIKE '%_n' OR u.username LIKE '%_z'
   OR u.username LIKE '%_r'
ON CONFLICT DO NOTHING;

-- Plus simple et fiable :
INSERT INTO provider_category (provider_id, category_id)
SELECT DISTINCT s.provider_id, s.category_id FROM service s
ON CONFLICT DO NOTHING;


-- ================================================================
-- ÉTAPE 7 — AVIS (20 avis sur les meilleurs prestataires)
-- client_id = 4 (ali_demandeur) et 5 (nadia_client) — déjà dans bdd.sql
-- ================================================================
INSERT INTO avis
    (client_id, prestataire_id, service_id, commentaire,
     note_globale, note_prix, note_qualite, note_rapidite,
     note_communication, is_verified_purchase, is_anonymous)
SELECT
    u_client.id,
    prov.id,
    svc.id,
    av.commentaire,
    av.ng, av.np, av.nq, av.nr, av.nc,
    TRUE, FALSE
FROM (VALUES
('ali_demandeur',  'youcef_b',  'Youcef est très sérieux, fuite réparée en 30 min.',         5,4,5,5,5),
('nadia_client',   'youcef_b',  'Bon travail, propre et efficace. Prix correct.',             4,4,4,4,4),
('ali_demandeur',  'hassan_m',  'Hassan expert, diagnostic précis et réparation rapide.',     5,5,5,5,5),
('nadia_client',   'hassan_m',  'Excellent plombier, je recommande vivement.',                5,4,5,5,4),
('ali_demandeur',  'nabil_c',   'Nabil a fait un câblage parfait. Tableau impeccable.',       5,4,5,4,5),
('nadia_client',   'nabil_c',   'Électricien sérieux et ponctuel.',                          4,4,4,4,4),
('ali_demandeur',  'tarek_h',   'Tarek le meilleur électricien de Tiaret.',                  5,5,5,5,5),
('nadia_client',   'tarek_h',   'Installation parfaite. Aucun problème depuis 6 mois.',      5,4,5,4,5),
('ali_demandeur',  'farid_t',   'Farid a peint tout l appartement. Résultat magnifique.',    5,4,5,4,5),
('nadia_client',   'aissa_b',   'Aissa travaille très bien. Finitions soignées.',            4,4,4,3,4),
('ali_demandeur',  'redha_k',   'Redha m a fabriqué des portes sur mesure superbes.',        5,3,5,4,5),
('nadia_client',   'zaki_m',    'Zaki a installé mes placards parfaitement.',                5,4,5,5,5),
('ali_demandeur',  'fares_h',   'Fares a installé mon clim rapidement.',                     5,4,5,5,4),
('nadia_client',   'ramzi_d',   'Ramzi compétent et ponctuel.',                              4,4,4,4,4),
('ali_demandeur',  'ayoub_t',   'Ayoub a rénové mon appartement. Très beau résultat.',       5,4,5,4,5),
('nadia_client',   'sabri_f',   'Carrelage bien posé, propre et solide.',                    4,3,4,4,4),
('ali_demandeur',  'toufik_n',  'Nettoyage impeccable après les travaux.',                   5,4,5,5,5),
('nadia_client',   'lazhar_b',  'Lazhar entretient mon jardin depuis 1 an.',                 4,4,4,4,4),
('ali_demandeur',  'hichem_r',  'Hichem a posé toutes les prises de ma maison.',             5,5,5,4,5),
('nadia_client',   'adel_b',    'Adel a refait toute l installation électrique.',            5,4,5,5,5)
) AS av(client_uname, prov_uname, commentaire, ng, np, nq, nr, nc)
JOIN users    u_client ON u_client.username = av.client_uname
JOIN users    u_prov   ON u_prov.username   = av.prov_uname
JOIN provider prov     ON prov.user_id      = u_prov.id
JOIN service  svc      ON svc.provider_id   = prov.id;


-- ================================================================
-- ÉTAPE 8 — TRUST_SCORES (meilleurs prestataires)
-- ================================================================
INSERT INTO trust_scores
    (prestataire_id, trust_score, total_reviews, positive_reviews,
     neutral_reviews, negative_reviews, avg_rating,
     verified_reviews, response_rate, report_count)
SELECT p.id, ts.trust_score, ts.total, ts.pos, ts.neu, ts.neg,
       ts.avg_r, ts.verif, ts.resp, 0
FROM (VALUES
('hassan_m',  94.0, 32, 31, 1, 0, 4.9, 32, 98.0),
('tarek_h',   95.0, 38, 37, 1, 0, 4.9, 38, 99.0),
('nabil_c',   88.0, 25, 24, 1, 0, 4.8, 25, 96.0),
('fares_h',   87.0, 24, 23, 1, 0, 4.8, 24, 94.0),
('mourad_f',  80.0, 18, 16, 2, 0, 4.6, 18, 90.0),
('redha_k',   83.0, 19, 18, 1, 0, 4.7, 19, 92.0),
('youcef_b',  82.0, 21, 19, 2, 0, 4.7, 21, 95.0),
('ramzi_d',   85.0, 20, 19, 1, 0, 4.7, 20, 93.0),
('adel_b',    84.0, 22, 21, 1, 0, 4.7, 22, 91.0),
('ayoub_t',   80.0, 18, 17, 1, 0, 4.6, 18, 89.0)
) AS ts(uname, trust_score, total, pos, neu, neg, avg_r, verif, resp)
JOIN users    u ON u.username = ts.uname
JOIN provider p ON p.user_id  = u.id
ON CONFLICT (prestataire_id) DO NOTHING;


-- ================================================================
-- FIN — 40 prestataires insérés avec succès
-- ================================================================
SELECT 'Data inserted: ' || COUNT(*) || ' providers' AS result FROM provider;