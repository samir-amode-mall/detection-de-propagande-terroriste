import os
from fuzzywuzzy import fuzz

def generer_rapport(texte_tesseract, texte_paddle, texte_easy, texte_fusionne, texte_corrige, output_dir):
    # Calcul des similarités entre les textes
    similarite_tesseract_paddle = fuzz.ratio(texte_tesseract, texte_paddle)
    similarite_tesseract_easy = fuzz.ratio(texte_tesseract, texte_easy)
    similarite_paddle_easy = fuzz.ratio(texte_paddle, texte_easy)

    # Génération du rapport
    rapport = f"""
=== Rapport d'analyse OCR ===

=== Texte extrait par Tesseract ===
{texte_tesseract}

=== Texte extrait par PaddleOCR ===
{texte_paddle}

=== Texte extrait par EasyOCR ===
{texte_easy}

=== Comparaison des résultats ===
>> Similarité entre Tesseract et PaddleOCR : {similarite_tesseract_paddle}%
>> Similarité entre Tesseract et EasyOCR : {similarite_tesseract_easy}%
>> Similarité entre PaddleOCR et EasyOCR : {similarite_paddle_easy}%

=== Texte fusionné (reconstitué) ===
{texte_fusionne}

=== Texte corrigé ===
{texte_corrige}
    """

    # Sauvegarde du rapport
    rapport_path = os.path.join(output_dir, 'rapport_final_ultimate.txt')
    with open(rapport_path, 'w', encoding='utf-8') as f:
        f.write(rapport)
    print(f"Rapport généré avec succès dans '{rapport_path}'.")
