from fuzzywuzzy import fuzz

def fusionner_textes(texte_tesseract, texte_paddle, texte_easy):
    phrases_tesseract = texte_tesseract.splitlines()
    phrases_paddle = texte_paddle.splitlines()
    phrases_easy = texte_easy.splitlines()
    texte_fusionne = []
    max_lignes = max(len(phrases_tesseract), len(phrases_paddle), len(phrases_easy))

    for i in range(max_lignes):
        phrases = [
            phrases_tesseract[i] if i < len(phrases_tesseract) else "",
            phrases_paddle[i] if i < len(phrases_paddle) else "",
            phrases_easy[i] if i < len(phrases_easy) else ""
        ]
        texte_fusionne.append(max(phrases, key=lambda x: fuzz.ratio(x, phrases[0])))

    return " ".join(texte_fusionne)
