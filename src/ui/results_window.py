from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt  
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

#  Définition des labels (doit être cohérent avec ton modèle)
LABELS = {
    "LABEL_0": "Propagande",
    "LABEL_1": "Neutre",
    "LABEL_2": "Opinion",
    "LABEL_3": "Fait",
    "LABEL_4": "Autre"
}

class ResultsWindow(QDialog):
    """Fenêtre affichant les résultats de l'analyse du modèle."""
    def __init__(self, labels, predictions):
        super().__init__()

        self.setWindowTitle(" Résultats de l'analyse")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        # Vérifier si des données sont disponibles
        if not labels or not predictions:
            layout.addWidget(QLabel("⚠️ Aucune donnée disponible pour afficher les résultats."))
        else:
            #  Générer les métriques de performance
            report = classification_report(labels, predictions, output_dict=True)
            accuracy = report["accuracy"]
            f1_score = report["weighted avg"]["f1-score"]

            #  Affichage des scores dans l'UI
            layout.addWidget(QLabel(f" Précision globale : {accuracy:.2f}"))
            layout.addWidget(QLabel(f" F1-score : {f1_score:.2f}"))

            #  Bouton pour afficher la Matrice de Confusion
            self.confusion_button = QPushButton(" Voir la Matrice de Confusion", self)
            self.confusion_button.clicked.connect(lambda: self.show_confusion_matrix(labels, predictions))
            layout.addWidget(self.confusion_button)

        # Bouton pour fermer la fenêtre
        self.close_button = QPushButton("Fermer", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def show_confusion_matrix(self, labels, predictions):
        """Affiche la matrice de confusion sous forme graphique."""
        cm = confusion_matrix(labels, predictions)
        
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=LABELS.values(), yticklabels=LABELS.values())
        plt.xlabel("Prédictions")
        plt.ylabel("Véritables classes")
        plt.title("Matrice de Confusion")
        plt.show()
