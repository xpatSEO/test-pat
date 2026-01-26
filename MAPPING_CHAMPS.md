# MAPPING COMPLET DES CHAMPS - Format JSON WordPress

## 📋 Table des matières
1. [Structure de premier niveau](#1-structure-de-premier-niveau)
2. [Champs post_data](#2-champs-post_data)
3. [Champs post_meta](#3-champs-post_meta)
4. [Champs acf_fields](#4-champs-acf_fields)
5. [Champs dans post_content (blocs ACF)](#5-champs-dans-post_content)
6. [Règles de formatage](#6-règles-de-formatage)

---

## 1. Structure de premier niveau

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `post_data` | `dict` | ✅ | Données principales du post WordPress |
| `post_meta` | `dict` | ✅ | Métadonnées WordPress et ACF |
| `taxonomies` | `list` | ✅ | Taxonomies (catégories, tags) - peut être vide |
| `feature_img` | `list[string, int, int, bool]` | ✅ | Image mise en avant [url, width, height, is_intermediate] |
| `acf_fields` | `dict` | ✅ | Champs ACF désérialisés |
| `post_type` | `string` | ✅ | Type de post (ex: "metier") |

---

## 2. Champs post_data

| Champ | Type | Format | Obligatoire | Exemple |
|-------|------|--------|-------------|---------|
| `ID` | `integer` | Nombre entier | ✅ | `678` ou `0` (auto-généré) |
| `post_author` | `string` | ID utilisateur | ✅ | `"39"` |
| `post_date` | `string` | YYYY-MM-DD HH:MM:SS | ✅ | `"2025-04-24 16:57:17"` |
| `post_date_gmt` | `string` | YYYY-MM-DD HH:MM:SS | ✅ | `"2025-04-24 14:57:17"` |
| `post_content` | `string` | HTML/Blocs Gutenberg | ✅ | Contenu avec blocs ACF |
| `post_title` | `string` | Texte | ✅ | `"Expert-comptable VTC..."` |
| `post_excerpt` | `string` | Texte | ✅ | `""` (peut être vide) |
| `post_status` | `string` | Statut WP | ✅ | `"publish"` ou `"draft"` |
| `comment_status` | `string` | Statut | ✅ | `"closed"` ou `"open"` |
| `ping_status` | `string` | Statut | ✅ | `"closed"` ou `"open"` |
| `post_password` | `string` | Texte | ✅ | `""` (vide par défaut) |
| `post_name` | `string` | Slug URL | ✅ | `"transport-personnes"` |
| `to_ping` | `string` | URLs | ✅ | `""` (vide par défaut) |
| `pinged` | `string` | URLs | ✅ | `""` (vide par défaut) |
| `post_modified` | `string` | YYYY-MM-DD HH:MM:SS | ✅ | `"2026-01-19 16:52:50"` |
| `post_modified_gmt` | `string` | YYYY-MM-DD HH:MM:SS | ✅ | `"2026-01-19 15:52:50"` |
| `post_content_filtered` | `string` | Texte | ✅ | `""` (vide) |
| `post_parent` | `integer` | ID du parent | ✅ | `0` (pas de parent) |
| `guid` | `string` | URL unique | ✅ | `"https://staging.site.../?post_type=metier&#038;p=678"` |
| `menu_order` | `integer` | Ordre d'affichage | ✅ | `15` |
| `post_type` | `string` | Type | ✅ | `"metier"` |
| `post_mime_type` | `string` | MIME type | ✅ | `""` (vide pour post) |
| `comment_count` | `string` | Nombre | ✅ | `"0"` |
| `filter` | `string` | Filtre | ✅ | `"raw"` |

---

## 3. Champs post_meta

> ⚠️ **IMPORTANT** : Tous les champs post_meta sont des `list[string]`, même pour les valeurs numériques.

| Champ | Type | Exemple | Description |
|-------|------|---------|-------------|
| `_thumbnail_id` | `list[string]` | `["23619"]` | ID de l'image mise en avant |
| `_edit_last` | `list[string]` | `["39"]` | Dernier éditeur |
| `_edit_lock` | `list[string]` | `["1768838017:39"]` | Verrou d'édition |
| `_acf_changed` | `list[string]` | `["1"]` | Indique si ACF a changé |
| `_wp_page_template` | `list[string]` | `["template-job-service.php"]` | Template de page |
| `_wp_old_slug` | `list[string]` | `["e-commerce", "..."]` | Anciens slugs |
| `block_type` | `list[string]` | `["with_form"]` | Type de bloc |
| `_block_type` | `list[string]` | `["field_65c094db0144d"]` | Field key ACF |
| `form_title` | `list[string]` | `["Prendre rendez-vous..."]` | Titre du formulaire |
| `_form_title` | `list[string]` | `["field_65c093610b07c"]` | Field key ACF |
| `template_form_id` | `list[string]` | `["7"]` | ID du formulaire |
| `_template_form_id` | `list[string]` | `["field_65e720072e7d8"]` | Field key ACF |
| `form_source` | `list[string]` | `["KEO VTC"]` | Source du formulaire |
| `_form_source` | `list[string]` | `["field_623c33e6d0c96"]` | Field key ACF |
| `hide_actions` | `list[string]` | `["0"]` | Masquer actions |
| `_hide_actions` | `list[string]` | `["field_633c11fc17d35"]` | Field key ACF |
| `hide_logo` | `list[string]` | `["0"]` | Masquer logo |
| `_hide_logo` | `list[string]` | `["field_6470b5798a4d6"]` | Field key ACF |
| `commentary` | `list[string]` | `[""]` | Commentaire |
| `_commentary` | `list[string]` | `["field_63e6248d95c32"]` | Field key ACF |
| `_custom_header_design` | `list[string]` | `["yes"]` | Design de header personnalisé |
| `title` | `list[string]` | `["Expert-comptable VTC..."]` | Titre alternatif |
| `_yoast_wpseo_title` | `list[string]` | `["Cabinet d'expertise..."]` | Titre SEO Yoast |
| `_yoast_wpseo_metadesc` | `list[string]` | `["Pourquoi faire appel..."]` | Meta description Yoast |
| `_yoast_wpseo_content_score` | `list[string]` | `["90"]` | Score de contenu Yoast |
| `_yoast_wpseo_estimated-reading-time-minutes` | `list[string]` | `["1"]` | Temps de lecture estimé |
| `_yoast_wpseo_wordproof_timestamp` | `list[string]` | `[""]` | Timestamp WordProof |
| `_pys_head_footer` | `list[string]` | `["a:7:{...}"]` | Scripts head/footer (sérialisé PHP) |
| `_oembed_*` | `list[string]` | `["<iframe..."]` | Cache oEmbed |

---

## 4. Champs acf_fields

> Ces champs représentent les valeurs ACF désérialisées (utilisées par les templates).

| Champ | Type | Exemple | Description |
|-------|------|---------|-------------|
| `form_source` | `string` | `"KEO VTC"` | Source du formulaire |
| `hide_actions` | `boolean` | `false` | Masquer les actions |
| `commentary` | `string` | `""` | Commentaire |
| `hide_logo` | `boolean` | `false` | Masquer le logo |
| `block_type` | `string` | `"with_form"` | Type de bloc |
| `form_title` | `string` | `"Prendre rendez-vous..."` | Titre du formulaire |
| `template_form_id` | `string` | `"7"` | ID du template de formulaire |

---

## 5. Champs dans post_content

### 5.1 Structure des blocs ACF

Les blocs ACF dans `post_content` suivent ce format :
```html
<!-- wp:acf/nom-du-bloc {"name":"acf/nom-du-bloc","data":{CHAMPS_ACF},"mode":"edit"} /-->
```

### 5.2 Types de champs ACF

#### A. IDs d'images/icônes (directs)

| Pattern | Type | Format | Exemple |
|---------|------|--------|---------|
| `kb_*_img` | `integer` | Nombre entier | `"kb_header_metier_img":23227` |
| `kb_*_icon` | `integer` | Nombre entier | `"kb_avantages_item_icon":28506` |
| `_kb_*_img` | `string` | Field key ACF | `"_kb_header_metier_img":"field_68527a9b86417"` |
| `_kb_*_icon` | `string` | Field key ACF | `"_kb_avantages_item_icon":"field_67cf08c12bbfc"` |

#### B. Textes (titres, descriptions, URLs)

| Pattern | Type | Format | Exemple |
|---------|------|--------|---------|
| `kb_*_title` | `string` | Texte/HTML | `"kb_header_metier_title":"Expert-comptable..."` |
| `kb_*_desc` | `string` | Texte/HTML | `"kb_header_metier_desc":"Pour se lancer..."` |
| `kb_*_subtitle` | `string` | Texte/HTML | `"kb_offers_subtitle":"De la création..."` |
| `kb_*_url` | `string` | URL | `"kb_header_metier_btn_url":"/nous-contacter/"` |
| `kb_*_link` | `string` | URL | `"kb_avantages_btn_link":"/nous-contacter"` |
| `kb_*_btn_txt` | `string` | Texte | `"kb_header_metier_btn_txt":"Obtenez un devis"` |
| `kb_*_mention` | `string` | Texte | `"kb_header_metier_mention":"Gratuit et sans engagement."` |
| `_kb_*_title` | `string` | Field key ACF | `"_kb_header_metier_title":"field_68527a9b86396"` |

#### C. Booléens et flags

| Pattern | Type | Format | Exemple |
|---------|------|--------|---------|
| `kb_*_show_*` | `string` | "0" ou "1" | `"kb_header_metier_show_btn":"1"` |
| `kb_*_text_small` | `string` | "0" ou "1" | `"kb_header_metier_text_small":"1"` |

#### D. Compteurs et listes

| Pattern | Type | Format | Exemple |
|---------|------|--------|---------|
| `kb_*_list` (compteur) | `integer` | Nombre d'items | `"kb_partners_list":10` |
| `kb_*_items` (compteur) | `integer` | Nombre d'items | `"kb_avantages_columns_items":3` |
| `kb_*_list` (array) | `array[string]` | ⚠️ **Strings** dans l'array | `"kb_offers_list":["25896","24919","25897","25898"]` |
| `metiers` | `array[string]` | ⚠️ **Strings** dans l'array | `"metiers":["943","13457","986","946","940","18501","955"]` |

#### E. Champs répéteurs (pattern indexé)

Les champs répéteurs ACF utilisent un index numérique :

| Pattern | Type | Exemple |
|---------|------|---------|
| `kb_*_list_N_kb_*` | variable | `"kb_partners_list_0_kb_partners_item_img":23752` |
| `kb_*_items_N_kb_*` | variable | `"kb_avantages_columns_items_0_kb_avantages_columns_item_title":"..."` |

Où `N` est l'index (0, 1, 2, ...).

---

## 6. Règles de formatage

### ✅ RÈGLE #1 : IDs directs = INTEGER

```json
"kb_header_metier_img": 23227
"kb_partners_list_0_kb_partners_item_img": 23752
"kb_avantages_list_0_kb_avantages_item_icon": 23802
```

### ✅ RÈGLE #2 : IDs dans arrays = STRING

```json
"kb_offers_list": ["25896","24919","25897","25898"]
"metiers": ["943","13457","986","946","940","18501","955"]
```

### ✅ RÈGLE #3 : Field keys ACF = STRING

```json
"_kb_header_metier_img": "field_68527a9b86417"
"_kb_header_metier_title": "field_68527a9b86396"
```

### ✅ RÈGLE #4 : Compteurs = INTEGER

```json
"kb_partners_list": 10
"kb_avantages_columns_items": 3
"kb_faq_list": 5
```

### ✅ RÈGLE #5 : Textes et URLs = STRING

```json
"kb_header_metier_title": "Expert-comptable pour <span>les chauffeurs VTC</span>"
"kb_header_metier_desc": "Pour se lancer dans le secteur..."
"kb_header_metier_btn_url": "/nous-contacter/"
```

### ✅ RÈGLE #6 : Booléens = STRING "0" ou "1"

```json
"kb_header_metier_show_btn": "1"
"kb_header_metier_text_small": "1"
```

### ✅ RÈGLE #7 : post_meta = TOUJOURS list[string]

```json
"_thumbnail_id": ["23619"]
"_edit_last": ["39"]
"template_form_id": ["7"]
"hide_actions": ["0"]
```

---

## 📊 Tableau récapitulatif des types

| Contexte | Champ | Type | Exemple |
|----------|-------|------|---------|
| post_data | ID, post_parent, menu_order | `integer` | `678` |
| post_data | Tous les autres | `string` | `"transport-personnes"` |
| post_meta | **TOUS** | `list[string]` | `["23619"]` |
| acf_fields | form_source, form_title, template_form_id | `string` | `"KEO VTC"` |
| acf_fields | hide_actions, hide_logo | `boolean` | `false` |
| post_content (ACF) | kb_*_img, kb_*_icon (direct) | `integer` | `23227` |
| post_content (ACF) | _kb_* (field keys) | `string` | `"field_xxx"` |
| post_content (ACF) | kb_*_list (compteur) | `integer` | `10` |
| post_content (ACF) | kb_*_list (array), metiers | `array[string]` | `["25896","24919"]` |
| post_content (ACF) | kb_*_title, kb_*_desc, kb_*_url | `string` | `"Titre..."` |
| post_content (ACF) | kb_*_show_*, booléens | `string` | `"1"` ou `"0"` |
| feature_img | - | `[string, int, int, bool]` | `["https://...", 596, 1014, false]` |

---

## ⚠️ Erreurs courantes à éviter

| ❌ Incorrect | ✅ Correct | Raison |
|-------------|-----------|---------|
| `"kb_offers_list":[25896,24919]` | `"kb_offers_list":["25896","24919"]` | IDs dans arrays doivent être strings |
| `"kb_header_metier_img":"23227"` | `"kb_header_metier_img":23227` | IDs directs doivent être integers |
| `"_thumbnail_id":"23619"` | `"_thumbnail_id":["23619"]` | post_meta doit être un array |
| `"kb_partners_list":"10"` | `"kb_partners_list":10` | Compteurs doivent être integers |
| `"post_data":{"ID":null}` | `"post_data":{"ID":0}` | Utiliser 0 au lieu de null |

---

## 📝 Notes importantes

1. **Caractères spéciaux** : Les caractères HTML doivent être échappés avec `\u003c` (pour `<`) et `\u003e` (pour `>`)
2. **Guillemets** : Les guillemets dans les strings doivent être échappés : `\"`
3. **Newlines** : Les retours à la ligne dans les strings utilisent `\r\n`
4. **Dates** : Format strict `YYYY-MM-DD HH:MM:SS` (24h)
5. **URLs dans guid** : Utiliser `&#038;` pour le `&` dans les URLs

---

**Dernière mise à jour** : 2026-01-26
**Basé sur** : metier_ID_678_data.json (référence)
