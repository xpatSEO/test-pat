#!/usr/bin/env python3
"""
Script pour générer des descriptions marketing personnalisées par métier
avec bullet points HTML adaptés à chaque secteur d'activité
"""
import json
import re
import csv

# Charger le fichier
with open('/home/user/test-pat/all_landings_wpai_fixed.json', 'r') as f:
    data = json.load(f)

# Bibliothèque de contenus marketing par secteur et type d'avantage
MARKETING_CONTENT = {
    # BTP / Construction
    'btp': {
        'economie': [
            "Optimisation des taux de TVA (5,5%, 10%, 20%) selon vos chantiers",
            "Maîtrise de l'auto-liquidation en sous-traitance pour éviter les pénalités",
            "Réduction moyenne de 12k€ d'impôts via les dispositifs BTP"
        ],
        'temps': [
            "Automatisation de la saisie : envoyez vos factures en photo",
            "Suivi de rentabilité par chantier en temps réel",
            "Gagnez 10h/mois sur la gestion administrative"
        ],
        'securite': [
            "Dossier blindé face aux contrôles URSSAF et fiscaux",
            "Gestion CIBTP et congés intempéries incluse",
            "Expert-comptable en première ligne lors des contrôles"
        ]
    },

    # VTC / Transport
    'vtc': {
        'choix_statut': [
            "Audit gratuit de votre situation (Micro, SASU, EURL)",
            "Prise en charge de vos formalités de création",
            "Conseil en optimisation (salaire vs. dividendes)"
        ],
        'tva_frais': [
            "Expertise sur la récupération de TVA (carburant, péages)",
            "Outil de scan de vos notes de frais (essence, entretien)",
            "Calcul et optimisation de vos frais kilométriques"
        ],
        'pilotage': [
            "Expert-comptable dédié qui connaît votre secteur",
            "Synchronisation bancaire automatique",
            "Tableaux de bord simples et en temps réel"
        ]
    },

    # E-commerce / Digital
    'ecommerce': {
        'temps': [
            "Synchronisation automatique Shopify, Amazon, WooCommerce",
            "Rapprochement bancaire et TVA automatisés",
            "Économisez 15h/mois réinvesties dans le marketing"
        ],
        'conformite': [
            "Déclarations TVA intracommunautaire et OSS gérées",
            "Comptabilité conforme aux plateformes (Amazon, eBay)",
            "Zéro retard, zéro pénalité : suivi proactif garanti"
        ],
        'croissance': [
            "Conseil sur la structuration juridique (SASU, holding)",
            "Optimisation fiscale de votre rémunération",
            "Stratégie d'expansion (international, marketplace)"
        ]
    },

    # Informatique / Digital
    'informatique': {
        'temps': [
            "Récupérez 10h/mois pour vous concentrer sur vos projets",
            "Automatisation complète de la saisie comptable",
            "Interface digitale : tout en ligne, zéro paperasse"
        ],
        'fiscalite': [
            "Déduction optimisée : matériel, logiciels, home office",
            "Frais de R&D et CIR (Crédit Impôt Recherche) maximisés",
            "Conseil en rémunération pour payer moins d'impôts"
        ],
        'securite': [
            "Expert-comptable agréé : responsabilité garantie",
            "Nous vous représentons en cas de contrôle fiscal",
            "Conformité totale (RGPD, facturation électronique)"
        ]
    },

    # Restaurant / CHR
    'restaurant': {
        'tva': [
            "Maîtrise des taux de TVA restaurant (10%, 20%)",
            "Optimisation TVA sur alcools et prestations",
            "Évitez les redressements grâce à notre expertise CHR"
        ],
        'gestion': [
            "Suivi de rentabilité en temps réel (marge par plat)",
            "Gestion automatisée des notes de frais et stocks",
            "Anticipation de trésorerie pour gérer la saisonnalité"
        ],
        'expertise': [
            "Spécialiste CHR : nous connaissons vos problématiques",
            "Conseil sur l'optimisation des charges sociales",
            "Support lors des contrôles URSSAF et hygiène"
        ]
    },

    # Artisan / Artisanat
    'artisan': {
        'temps': [
            "Déléguez 100% de la compta et gagnez 10h par mois",
            "Envoyez vos factures en photo, on gère le reste",
            "Plus de temps pour vos clients et votre savoir-faire"
        ],
        'economie': [
            "Nos conseils couvrent souvent le coût de nos honoraires",
            "Optimisation fiscale (déductions, frais réels)",
            "Réduction des charges sociales grâce à nos stratégies"
        ],
        'accompagnement': [
            "Un comptable dédié qui connaît votre dossier",
            "Réponses rapides (téléphone, mail, visio)",
            "Conseil personnalisé pour développer votre activité"
        ]
    },

    # Industrie / Manufacturing
    'industrie': {
        'temps': [
            "Automatisation : facturation, notes de frais, rapprochements",
            "Libérez 15h/mois pour vous concentrer sur la production",
            "Tableaux de bord pour piloter sans perte de temps"
        ],
        'tresorerie': [
            "Prévisions de trésorerie à 3 mois : zéro surprise",
            "Anticipation des besoins d'investissement",
            "Optimisation du BFR (Besoin en Fonds de Roulement)"
        ],
        'optimisation': [
            "Identification des coûts cachés et marges négatives",
            "Conseil en fiscalité industrielle (amortissements, stocks)",
            "Maximisation du résultat net dès le premier bilan"
        ]
    },

    # CONTENU GÉNÉRIQUE (par défaut)
    'default': {
        'temps': [
            "Automatisation complète de votre saisie comptable",
            "Tableaux de bord en temps réel pour piloter sereinement",
            "Gagnez 10h par mois réinvesties dans votre activité"
        ],
        'economie': [
            "Optimisation fiscale adaptée à votre secteur",
            "Réduction des pénalités grâce à notre suivi proactif",
            "Conseil en rémunération pour maximiser votre revenu net"
        ],
        'securite': [
            "Expert-comptable agréé : responsabilité professionnelle garantie",
            "Dossier blindé en cas de contrôle (nous vous représentons)",
            "Zéro retard de déclaration grâce à notre calendrier automatisé"
        ],
        'expertise': [
            "Spécialiste de votre secteur et de vos problématiques",
            "Conseil stratégique au-delà du simple bilan",
            "Interlocuteur dédié qui comprend votre métier"
        ]
    }
}

def detect_sector(post_slug, post_title):
    """Détecte le secteur d'activité basé sur le slug et le titre"""
    text = (post_slug + ' ' + post_title).lower()

    if any(word in text for word in ['btp', 'batiment', 'construction', 'maçon', 'électricien', 'plombier', 'chantier']):
        return 'btp'
    elif any(word in text for word in ['vtc', 'taxi', 'chauffeur', 'transport-personnes']):
        return 'vtc'
    elif any(word in text for word in ['ecommerce', 'e-commerce', 'shopify', 'amazon', 'marketplace']):
        return 'ecommerce'
    elif any(word in text for word in ['informatique', 'digital', 'developpeur', 'web', 'saas', 'tech']):
        return 'informatique'
    elif any(word in text for word in ['restaurant', 'bar', 'café', 'chr', 'hotellerie', 'traiteur']):
        return 'restaurant'
    elif any(word in text for word in ['artisan', 'coiffeur', 'esthétique', 'bijoutier', 'boulanger']):
        return 'artisan'
    elif any(word in text for word in ['industrie', 'usine', 'manufacturing', 'production']):
        return 'industrie'
    else:
        return 'default'

def detect_advantage_type(title, desc):
    """Détecte le type d'avantage basé sur le titre"""
    text = (title + ' ' + desc).lower()

    # Pour VTC
    if 'statut' in text or 'choix' in text:
        return 'choix_statut'
    if 'tva' in text or 'frais' in text or 'charge' in text:
        return 'tva_frais'
    if 'pilotage' in text or 'tableau' in text or 'temps réel' in text:
        return 'pilotage'

    # Général
    if any(word in text for word in ['temps', 'heure', 'gagnez', 'gain', '10h', '15h']):
        return 'temps'
    elif any(word in text for word in ['économie', 'coût', '€', 'prix', 'argent', 'optimis']):
        return 'economie'
    elif any(word in text for word in ['sécurité', 'sérénité', 'tranquillité', 'conformité', 'contrôle']):
        return 'securite'
    elif any(word in text for word in ['tva']):
        return 'tva'
    elif any(word in text for word in ['trésorerie', 'cash', 'visibilité']):
        return 'tresorerie'
    elif any(word in text for word in ['gestion']):
        return 'gestion'
    elif any(word in text for word in ['croissance', 'développement', 'expansion']):
        return 'croissance'
    elif any(word in text for word in ['fiscalité', 'fiscal', 'impôt']):
        return 'fiscalite'
    elif any(word in text for word in ['accompagnement', 'conseil', 'expert']):
        return 'accompagnement'
    else:
        return 'expertise'

def generate_bullets(sector, advantage_type):
    """Génère les bullet points HTML adaptés"""
    content_library = MARKETING_CONTENT.get(sector, MARKETING_CONTENT['default'])

    # Chercher le type d'avantage dans la bibliothèque du secteur
    bullets = content_library.get(advantage_type)

    # Si pas trouvé, chercher dans le contenu par défaut
    if not bullets:
        bullets = MARKETING_CONTENT['default'].get(advantage_type, MARKETING_CONTENT['default']['expertise'])

    # Générer le HTML
    html = "<ul>\\r\\n"
    for bullet in bullets:
        html += f" \\t<li>{bullet}</li>\\r\\n"
    html += "</ul>"

    return html

print("Génération du contenu marketing personnalisé par métier...")
print("="*100)

# Préparer les données
csv_data = []

for idx, post in enumerate(data):
    post_slug = post['post_data'].get('post_name', f'post-{idx}')
    post_title = post['post_data'].get('post_title', 'Sans titre')
    content = post['post_data']['post_content']

    # Détecter le secteur
    sector = detect_sector(post_slug, post_title)

    # Extraire les titres et descriptions
    title_pattern = r'"kb_avantages_columns_items_(\d+)_kb_avantages_columns_item_title":"([^"]*(?:\\.[^"]*)*)"'
    desc_pattern = r'"kb_avantages_columns_items_(\d+)_kb_avantages_columns_item_desc":"([^"]*(?:\\.[^"]*)*)"'

    titles = re.findall(title_pattern, content)
    descs = re.findall(desc_pattern, content)

    # Créer un dictionnaire pour mapper les items
    items = {}
    for item_idx, title_text in titles:
        if item_idx not in items:
            items[item_idx] = {}
        items[item_idx]['title'] = title_text.encode('utf-8').decode('unicode_escape')

    for item_idx, desc_text in descs:
        if item_idx not in items:
            items[item_idx] = {}
        items[item_idx]['desc'] = desc_text.encode('utf-8').decode('unicode_escape')

    # Générer les nouveaux contenus
    row = {
        'post_slug': post_slug,
        'post_title': post_title,
        'sector_detected': sector,
        'item_0_title': items.get('0', {}).get('title', ''),
        'item_0_desc_new': generate_bullets(
            sector,
            detect_advantage_type(
                items.get('0', {}).get('title', ''),
                items.get('0', {}).get('desc', '')
            )
        ),
        'item_1_title': items.get('1', {}).get('title', ''),
        'item_1_desc_new': generate_bullets(
            sector,
            detect_advantage_type(
                items.get('1', {}).get('title', ''),
                items.get('1', {}).get('desc', '')
            )
        ),
        'item_2_title': items.get('2', {}).get('title', ''),
        'item_2_desc_new': generate_bullets(
            sector,
            detect_advantage_type(
                items.get('2', {}).get('title', ''),
                items.get('2', {}).get('desc', '')
            )
        ),
    }

    csv_data.append(row)

    if idx < 5:
        print(f"\n✓ {post_slug} → Secteur détecté: {sector}")

# Sauvegarder le CSV final
output_file = '/home/user/test-pat/metiers_descriptions_marketing.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['post_slug', 'post_title', 'sector_detected',
                  'item_0_title', 'item_0_desc_new',
                  'item_1_title', 'item_1_desc_new',
                  'item_2_title', 'item_2_desc_new']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_data)

print(f"\n{'='*100}")
print(f"✅ CSV créé: {output_file}")
print(f"   Nombre de métiers traités: {len(csv_data)}")
print(f"{'='*100}")
