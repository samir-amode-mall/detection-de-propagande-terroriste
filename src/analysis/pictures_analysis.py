import cv2
from src.analysis.ocr_modules.preprocessing import pretraiter_image
from src.analysis.ocr_modules.ocr import extraire_texte_individuel
from src.analysis.ocr_modules.fusion import fusionner_textes
from src.analysis.ocr_modules.correction import corriger_orthographe

class ImageAnalyzer:
    def analyze_image(self, image_path):
        image_originale = cv2.imread(image_path)
        if image_originale is None:
            raise ValueError(f"Impossible de charger l'image à partir de : {image_path}")
        image_pretraitee = pretraiter_image(image_path)
        from src.analysis.ocr_modules.ocr import extraire_texte_individuel
        texte_tesseract = extraire_texte_individuel(image_pretraitee, engine="tesseract")
        texte_paddle = extraire_texte_individuel(image_originale, engine="paddle")
        texte_easy = extraire_texte_individuel(image_originale, engine="easy")
        texte_fusionne = fusionner_textes(texte_tesseract, texte_paddle, texte_easy)
        texte_corrige = corriger_orthographe(texte_fusionne)
        return texte_corrige
