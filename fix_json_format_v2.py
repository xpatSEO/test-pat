#!/usr/bin/env python3
"""
Script pour corriger le format du fichier all_landings_wpai.json
afin qu'il corresponde au format attendu (metier_ID_678_data.json)

VERSION 2: Corrige le format des arrays (garde les strings DANS les arrays)
"""

import json
import re
import sys
from typing import Any, Dict, List


def fix_acf_block_values(content: str) -> str:
    """
    Corrige les valeurs dans les blocs ACF du post_content:
    1. Convertit les IDs d'images DIRECTS de string à int
    2. Désérialise les arrays qui sont en string (mais garde les strings DANS l'array)

    FORMAT CORRECT:
    - Arrays: "kb_offers_list":["25896","24919","25897","25898"]
    - IDs directs: "kb_header_metier_img":23227
    """

    # 1. Pattern pour les IDs d'images DIRECTS en string -> convertir en int
    # Exemple: "kb_header_metier_img":"23227" => "kb_header_metier_img":23227
    def convert_img_ids(match):
        field_name = match.group(1)
        img_id = match.group(2)
        return f'"{field_name}":{img_id}'

    # Patterns pour les champs d'images (IDs directs uniquement)
    img_patterns = [
        r'"(kb_[^"]*_img)":"(\d+)"',  # kb_header_metier_img":"23227"
        r'"(kb_[^"]*_icon)":"(\d+)"', # kb_avantages_item_icon":"23802"
    ]

    for pattern in img_patterns:
        content = re.sub(pattern, convert_img_ids, content)

    # 2. Pattern pour les arrays sérialisés comme strings
    # Exemple: "kb_offers_list":"[25896, 24919]" => "kb_offers_list":["25896","24919"]
    # IMPORTANT: Garder les valeurs DANS l'array comme STRINGS
    def convert_arrays(match):
        field_name = match.group(1)
        array_content = match.group(2)
        # Parser l'array pour extraire les valeurs
        # Supprimer les crochets
        values_str = array_content.strip('[]')
        # Séparer par les virgules et nettoyer les espaces
        values = [v.strip() for v in values_str.split(',')]
        # Reconstruire l'array avec les valeurs en strings
        array_json = '["' + '","'.join(values) + '"]'
        return f'"{field_name}":{array_json}'

    # Pattern pour détecter les arrays sérialisés
    content = re.sub(r'"(kb_[^"]+_list|metiers|_metiers)":"(\[[^\]]+\])"', convert_arrays, content)

    # 3. Pattern pour les compteurs numériques (ex: "kb_partners_list":"10" => "kb_partners_list":10)
    def convert_numeric_counts(match):
        field_name = match.group(1)
        count = match.group(2)
        return f'"{field_name}":{count}'

    content = re.sub(r'"(kb_[^"]*_list|kb_[^"]*_items)":"(\d+)"', convert_numeric_counts, content)

    return content


def extract_first_image_id(content: str) -> int:
    """Extrait le premier ID d'image trouvé dans le post_content"""
    match = re.search(r'"kb_[^"]*_img[^"]*":(\d+)', content)
    if match:
        return int(match.group(1))
    return 0


def fix_post_data(post_data: Dict[str, Any]) -> Dict[str, Any]:
    """Corrige les champs manquants dans post_data"""

    # Si ID est null, le mettre à 0 (WordPress générera un nouvel ID)
    if post_data.get('ID') is None:
        post_data['ID'] = 0

    # Ajouter post_password si manquant
    if 'post_password' not in post_data:
        post_data['post_password'] = ""

    # Générer un GUID si manquant (basé sur le post_name)
    if 'guid' not in post_data:
        post_name = post_data.get('post_name', 'unknown')
        post_data['guid'] = f"https://staging.site.keobiz.fr/?post_type=metier&#038;p={post_data['ID']}"

    # Corriger le post_content pour les valeurs ACF
    if 'post_content' in post_data:
        post_data['post_content'] = fix_acf_block_values(post_data['post_content'])

    return post_data


def fix_post_meta(post_meta: Dict[str, Any], post_data: Dict[str, Any]) -> Dict[str, Any]:
    """Corrige les champs manquants dans post_meta"""

    # Extraire l'ID de l'image principale depuis le contenu
    thumbnail_id = extract_first_image_id(post_data.get('post_content', ''))

    # Ajouter _thumbnail_id si manquant
    if '_thumbnail_id' not in post_meta and thumbnail_id > 0:
        post_meta['_thumbnail_id'] = [str(thumbnail_id)]

    # Ajouter d'autres champs importants qui pourraient manquer
    if '_edit_last' not in post_meta:
        post_meta['_edit_last'] = ["39"]

    if '_acf_changed' not in post_meta:
        post_meta['_acf_changed'] = ["1"]

    if '_wp_page_template' not in post_meta:
        post_meta['_wp_page_template'] = ["template-job-service.php"]

    return post_meta


def create_feature_img(post_data: Dict[str, Any]) -> List[Any]:
    """Crée le champ feature_img à partir du post_content"""

    # Extraire l'ID de l'image principale
    img_id = extract_first_image_id(post_data.get('post_content', ''))

    if img_id > 0:
        # Format: [url, width, height, is_intermediate]
        # On ne peut pas deviner l'URL exacte, donc on met une URL générique
        return [
            f"https://staging.site.keobiz.fr/wp-content/uploads/2025/03/image-{img_id}.webp",
            596,
            1014,
            False
        ]

    # Image par défaut si aucune image n'est trouvée
    return [
        "https://staging.site.keobiz.fr/wp-content/uploads/2025/03/default.webp",
        596,
        1014,
        False
    ]


def fix_post(post: Dict[str, Any]) -> Dict[str, Any]:
    """Corrige un post complet"""

    # Supprimer le champ _stats s'il existe
    if '_stats' in post:
        del post['_stats']

    # Corriger post_data
    if 'post_data' in post:
        post['post_data'] = fix_post_data(post['post_data'])

    # Corriger post_meta
    if 'post_meta' in post and 'post_data' in post:
        post['post_meta'] = fix_post_meta(post['post_meta'], post['post_data'])

    # Ajouter feature_img si manquant
    if 'feature_img' not in post and 'post_data' in post:
        post['feature_img'] = create_feature_img(post['post_data'])

    return post


def main():
    input_file = '/home/user/test-pat/all_landings_wpai.json'
    output_file = '/home/user/test-pat/all_landings_wpai_fixed.json'

    print("Chargement du fichier JSON...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors du chargement du fichier: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("❌ Le fichier JSON doit contenir un tableau de posts")
        sys.exit(1)

    print(f"Nombre de posts à corriger: {len(data)}")

    # Corriger chaque post
    fixed_data = []
    errors = []

    for i, post in enumerate(data):
        try:
            fixed_post = fix_post(post)
            fixed_data.append(fixed_post)

            if (i + 1) % 10 == 0:
                print(f"Traité: {i + 1}/{len(data)} posts...")
        except Exception as e:
            error_msg = f"Post {i}: {str(e)}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg}")

    print(f"\n✅ Correction terminée: {len(fixed_data)}/{len(data)} posts corrigés")

    if errors:
        print(f"\n⚠️  {len(errors)} erreurs rencontrées:")
        for error in errors[:5]:  # Afficher les 5 premières erreurs
            print(f"  - {error}")

    # Sauvegarder le fichier corrigé
    print(f"\nSauvegarde dans {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Fichier sauvegardé avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        sys.exit(1)

    # Afficher un résumé des corrections
    print("\n" + "="*80)
    print("RÉSUMÉ DES CORRECTIONS APPLIQUÉES")
    print("="*80)
    print("✓ Suppression du champ '_stats'")
    print("✓ Ajout de 'post_password' dans post_data")
    print("✓ Ajout/correction de 'guid' dans post_data")
    print("✓ Correction de 'ID' (null → 0)")
    print("✓ Conversion des IDs d'images DIRECTS (string → int)")
    print("✓ Désérialisation des arrays (garde les strings DANS l'array)")
    print("✓ Ajout du champ 'feature_img'")
    print("✓ Ajout de '_thumbnail_id' dans post_meta")
    print("="*80)


if __name__ == "__main__":
    main()
