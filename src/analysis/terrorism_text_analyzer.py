import spacy
from spacy.matcher import PhraseMatcher
import os
import shutil

class TerrorismTextAnalyzer:
    def __init__(self, source_folder, suspect_folder):
        self.nlp = spacy.load("fr_core_news_sm")
        self.expressions = [
            "djihad", "califat", "islamisme", "radicalisation", "martyre", "extrémisme", "wahhabisme", "sharia", "fatwa",
            "attaque", "explosion", "attentat", "massacre", "décapitation", "assassinat", "embuscade", "sabotage", "prise d'otage",
            "bombe", "kamikaze", "ceinture explosive", "fusil", "kalachnikov", "pistolet", "drone", "engin explosif improvisé",
            "al-Qaïda", "Daesh", "Hezbollah", "Boko Haram", "Al-Shabaab", "PKK", "Hamas", "Talibans",
            "leader", "recruteur", "radicalisé", "sympathisant", "propagandiste", "combattant", "chef de guerre",
            "civils", "militaires", "ambassade", "gouvernement", "écoles", "marché", "mosquée", "église", "infrastructure",
            "vidéo", "discours", "manifeste", "tract", "message crypté", "forums", "réseaux sociaux", "darkweb",
            "Syrie", "Afghanistan", "Irak", "Sahel", "Yémen", "Pakistan", "Moyen-Orient", "Maghreb",
            "haine", "vengeance", "violence", "guerre", "rébellion", "oppression", "endoctrinement",
            "revendication", "responsabilité", "message", "martyr", "cible", "ennemi", "victoire", "combat"
        ]
        self.patterns = [self.nlp.make_doc(phrase) for phrase in self.expressions]
        self.matcher = PhraseMatcher(self.nlp.vocab)
        self.matcher.add("TERRORISME", self.patterns)
        self.source_folder = source_folder
        self.suspect_folder = suspect_folder

        os.makedirs(self.suspect_folder, exist_ok=True)

    def analyze_and_move_suspect_files(self):
        for fichier in os.listdir(self.source_folder):
            if fichier.endswith(".txt"):
                chemin_fichier = os.path.join(self.source_folder, fichier)

                with open(chemin_fichier, "r", encoding="utf-8") as f:
                    texte = f.read()

                doc = self.nlp(texte)
                matches = self.matcher(doc)

                if matches:
                    shutil.move(chemin_fichier, os.path.join(self.suspect_folder, fichier))
                    print(f"🚨 Fichier déplacé : {fichier}")
