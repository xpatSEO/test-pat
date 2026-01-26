#!/usr/bin/env python3
"""
Script pour appliquer les descriptions du fichier desc.json
au fichier all_landings_wpai_fixed.json en mappant les professions aux post_slug
"""
import json
import re
from difflib import get_close_matches

# Charger desc.json
print("="*100)
print("APPLICATION DES DESCRIPTIONS DE desc.json")
print("="*100)

with open('/home/user/test-pat/desc.json', 'r', encoding='utf-8') as f:
    desc_data = json.load(f)

# Créer un dictionnaire par profession
desc_by_profession = {item['profession'].lower(): item for item in desc_data}

print(f"\n✓ {len(desc_data)} professions chargées depuis desc.json")

# Charger all_landings_wpai_fixed.json
with open('/home/user/test-pat/all_landings_wpai_fixed.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

print(f"✓ {len(json_data)} posts chargés depuis all_landings_wpai_fixed.json")

# Mapping manuel pour les cas spécifiques
MANUAL_MAPPING = {
    'transport-personnes': 'vtc',
    'expert-comptable-vtc': 'vtc',
    'expert-comptable-btp': 'btp',
    'expert-comptable-e-commerce': 'e-commerce',
    'expert-comptable-artisan': 'artisans',
    'expert-comptable-restaurant': 'hôtellerie & restauration',
    'expert-comptable-bar': 'bar / café',
    'expert-comptable-hotel': 'hôtellerie',
    'expert-comptable-informatique': 'informatique',
    'expert-comptable-industrie': 'industrie',
    'expert-comptable-freelance': 'freelance',
    'expert-comptable-consultant': 'consultant',
    'expert-comptable-commerce': 'commerce',
    'expert-comptable-sci': 'sci',
    'expert-comptable-holding': 'holding',
    'expert-comptable-lmnp': 'lmnp',
    'expert-comptable-immobilier': 'immobilier',
    'expert-comptable-liberal': 'profession libérale',
    'expert-comptable-coiffeur': 'coiffeur / salon de coiffure',
    'expert-comptable-esthetique': 'esthéticienne',
    'expert-comptable-photographe': 'photographe freelance',
    'expert-comptable-graphiste': 'graphiste freelance',
    'expert-comptable-developpeur': 'développeur freelance',
    'expert-comptable-traiteur': 'traiteur',
    'expert-comptable-fleuriste': 'fleuriste',
    'expert-comptable-boulangerie': 'boulangerie',
    'expert-comptable-boucherie': 'boucherie / charcuterie',
    'expert-comptable-poissonnier': 'poissonnerie',
    'expert-comptable-epicerie': 'épicerie',
    'expert-comptable-nettoyage': 'entreprise de nettoyage',
    'expert-comptable-transport': 'transport de marchandises',
    'expert-comptable-electricien': 'électricien',
    'expert-comptable-plombier': 'plombier',
    'expert-comptable-menuisier': 'menuisier',
    'expert-comptable-charpentier': 'charpentier',
    'expert-comptable-serrurier': 'serrurier',
    'expert-comptable-medecin': 'médecin libéral',
    'expert-comptable-dentiste': 'dentiste libéral',
    'expert-comptable-kine': 'kinésithérapeute libéral',
    'expert-comptable-infirmiere': 'infirmière libérale (idel)',
    'expert-comptable-sage-femme': 'sage-femme libérale',
    'expert-comptable-osteopathe': 'ostéopathe libéral',
    'expert-comptable-psychologue': 'psychologue',
}

def find_profession_for_slug(post_slug, post_title):
    """Trouve la profession correspondante dans desc.json"""

    # 1. Essayer le mapping manuel d'abord
    if post_slug in MANUAL_MAPPING:
        profession = MANUAL_MAPPING[post_slug]
        if profession in desc_by_profession:
            return profession

    # 2. Extraire les mots-clés du slug
    slug_lower = post_slug.lower().replace('expert-comptable-', '').replace('-', ' ')

    # 3. Recherche directe
    if slug_lower in desc_by_profession:
        return slug_lower

    # 4. Recherche dans le titre
    title_lower = post_title.lower()
    for profession in desc_by_profession.keys():
        if profession in title_lower or profession in slug_lower:
            return profession

    # 5. Recherche fuzzy
    all_professions = list(desc_by_profession.keys())
    matches = get_close_matches(slug_lower, all_professions, n=1, cutoff=0.6)
    if matches:
        return matches[0]

    return None

# Appliquer les descriptions
print("\n" + "="*100)
print("MAPPING ET APPLICATION")
print("="*100)

updated = 0
not_found = []
mapping_log = []

for post in json_data:
    post_slug = post['post_data'].get('post_name', '')
    post_title = post['post_data'].get('post_title', '')

    # Trouver la profession correspondante
    profession = find_profession_for_slug(post_slug, post_title)

    if not profession:
        not_found.append(post_slug)
        continue

    # Récupérer les données de description
    desc_item = desc_by_profession[profession]
    mapping_log.append((post_slug, profession))

    # Remplacer les descriptions dans le post_content
    content = post['post_data']['post_content']

    # Remplacer le titre du bloc avantages
    title_pattern = r'"kb_avantages_columns_title":"([^"]*(?:\\.[^"]*)*)"'
    new_title = desc_item['kb_avantages_columns_title']
    content = re.sub(title_pattern, f'"kb_avantages_columns_title":"{new_title}"', content)

    # Remplacer chaque item (0, 1, 2)
    for i in range(3):
        # Titre de l'item
        title_field = f'kb_avantages_columns_items_{i}_kb_avantages_columns_item_title'
        new_item_title = desc_item[title_field]
        title_pattern = f'"{title_field}":"([^"]*(?:\\\\.[^"]*)*)"'
        content = re.sub(title_pattern, f'"{title_field}":"{new_item_title}"', content)

        # Description de l'item (déjà en HTML avec bullet points)
        desc_field = f'kb_avantages_columns_items_{i}_kb_avantages_columns_item_desc'
        new_item_desc = desc_item[desc_field]

        # Échapper pour JSON (\\n devient \\\\n, \\t devient \\\\t)
        new_item_desc_escaped = new_item_desc.replace('\\', '\\\\')

        desc_pattern = f'"{desc_field}":"([^"]*(?:\\\\.[^"]*)*)"'
        content = re.sub(desc_pattern, f'"{desc_field}":"{new_item_desc_escaped}"', content)

    post['post_data']['post_content'] = content
    updated += 1

print(f"\n✓ {updated} posts mis à jour avec les descriptions de desc.json")
print(f"⚠️  {len(not_found)} posts sans correspondance:")
for slug in not_found[:10]:
    print(f"   - {slug}")
if len(not_found) > 10:
    print(f"   ... et {len(not_found) - 10} autres")

# Sauvegarder
print("\n" + "="*100)
print("SAUVEGARDE")
print("="*100)

with open('/home/user/test-pat/all_landings_wpai_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("✓ Fichier sauvegardé: all_landings_wpai_fixed.json")

# Afficher le mapping
print("\n" + "="*100)
print("MAPPING APPLIQUÉ (premiers 20)")
print("="*100)
print(f"\n{'Post Slug':<40} {'Profession (desc.json)':<30}")
print("-"*100)
for slug, prof in mapping_log[:20]:
    print(f"{slug:<40} {prof:<30}")
if len(mapping_log) > 20:
    print(f"... et {len(mapping_log) - 20} autres")

# Vérification finale
print("\n" + "="*100)
print("VÉRIFICATION")
print("="*100)

first_updated = json_data[0]
content = first_updated['post_data']['post_content']
desc_match = re.search(r'"kb_avantages_columns_items_0_kb_avantages_columns_item_desc":"([^"]*(?:\\.[^"]*)*)"', content)

if desc_match:
    desc_raw = desc_match.group(1)
    # Décoder les échappements
    desc_decoded = desc_raw.encode('utf-8').decode('unicode_escape')

    print(f"\nExemple - Premier post: {first_updated['post_data']['post_name']}")
    print(f"Description item 0:")
    for line in desc_decoded.split('\n')[:5]:
        if line.strip():
            print(f"  {line}")

    if '<ul>' in desc_decoded and '<li>' in desc_decoded:
        print("\n✅ Format HTML avec bullet points détecté !")

print("\n" + "="*100)
print("TERMINÉ")
print("="*100)
