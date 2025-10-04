from preprocessing import pretraiter_image
from ocr import extraire_texte
from fusion import fusionner_textes
from correction import corriger_orthographe
from rapport import generer_rapport
import os

# Configuration des chemins
IMAGE_PATH = '../images/affiche_18-juin-1940.png'
OUTPUT_DIR = '../output/'

def main():
    # Prétraitement de l'image
    image_pretraitee = pretraiter_image(IMAGE_PATH)

    # Extraction du texte avec plusieurs OCR
    texte_tesseract, texte_paddle, texte_easy = extraire_texte(image_pretraitee)

    # Fusion des textes
    texte_fusionne = fusionner_textes(texte_tesseract, texte_paddle, texte_easy)

    # Correction orthographique
    texte_corrige = corriger_orthographe(texte_fusionne)

    # Sauvegarde du texte fusionné et corrigé
    with open(os.path.join(OUTPUT_DIR, 'texte_fusionne_ultimate.txt'), 'w', encoding='utf-8') as f:
        f.write(texte_fusionne)
    with open(os.path.join(OUTPUT_DIR, 'texte_corrige_ultimate.txt'), 'w', encoding='utf-8') as f:
        f.write(texte_corrige)

    # Génération du rapport
    generer_rapport(texte_tesseract, texte_paddle, texte_easy, texte_fusionne, texte_corrige, OUTPUT_DIR)

if __name__ == "__main__":
    main()
