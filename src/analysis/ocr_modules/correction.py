from spellchecker import SpellChecker

# Initialisation du correcteur orthographique
spell = SpellChecker(language='fr')

def corriger_orthographe(texte):
    mots = texte.split()
    mots_corriges = []
    for mot in mots:
        correction = spell.correction(mot)
        if correction is None:
            # Si la correction est None, conserver le mot original
            mots_corriges.append(mot)
        else:
            mots_corriges.append(correction)
    return " ".join(mots_corriges)
