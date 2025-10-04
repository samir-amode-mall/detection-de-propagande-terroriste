import pytesseract
from paddleocr import PaddleOCR
import easyocr

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
ocr_paddle = PaddleOCR(lang='fr')
ocr_easy = easyocr.Reader(['fr'])

def extraire_texte_individuel(image, engine="tesseract"):
    if engine == "tesseract":
        return pytesseract.image_to_string(image, lang='fra', config='--oem 1 --psm 6')
    elif engine == "paddle":
        result = ocr_paddle.ocr(image, cls=True)
        return " ".join([line[1][0] for line in result[0]])
    elif engine == "easy":
        result = ocr_easy.readtext(image)
        return " ".join([line[1] for line in result])
    else:
        raise ValueError("Moteur OCR non supporté.")
