from fpdf import FPDF
import os
from datetime import datetime
from src.report.report_generator import generate_pie_chart

class PDFGenerator:
    def __init__(self, output_folder="reports"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        self.logo_path = "src/ui/assets/file.png"

    def generate_pdf(self, text, analysis_result, save_path=None):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        if os.path.exists(self.logo_path):
            pdf.image(self.logo_path, x=10, y=8, w=30)

        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(200, 10, " Rapport d'Analyse de Texte ", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, f" Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(15)

        # Résumé
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, "Résumé de l'Analyse :", ln=True, align='L')
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, f" Sentiment détecté : {analysis_result['sentiment']}")
        pdf.multi_cell(0, 8, f" Confiance du modèle : {analysis_result['confidence']}%")
        pdf.ln(5)

        # Texte avec surlignage
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, " Texte analysé (avec surlignage) :", ln=True, align='L')
        pdf.ln(5)

        keywords = analysis_result.get("keywords", {})
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0)

        words = text.split()
        line_height = 6

        for word in words:
            clean_word = word.strip(".,!?;:«»“”\"\'()").lower()
            if clean_word in keywords:
                pdf.set_font("Arial", style='B', size=12)
                pdf.set_text_color(200, 0, 0)
            else:
                pdf.set_font("Arial", style='', size=12)
                pdf.set_text_color(0, 0, 0)
            pdf.write(line_height, word + " ")

        pdf.ln(8)

        # Mots-clés
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, " Mots-clés détectés :", ln=True, align='L')
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        if keywords:
            pdf.multi_cell(0, 8, ", ".join(keywords.keys()))
        else:
            pdf.multi_cell(0, 8, "Aucun mot-clé détecté.")
        pdf.ln(5)

        # Statistiques
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, " Statistiques :", ln=True, align='L')
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, f" Nombre de mots analysés : {len(text.split())}")
        pdf.multi_cell(0, 8, f" Score de propagande : {analysis_result['confidence']}%")
        pdf.ln(10)

        from fpdf import FPDF
import os
from datetime import datetime
from src.report.report_generator import generate_pie_chart

class PDFGenerator:
    def __init__(self, output_folder="reports"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        self.logo_path = "src/ui/assets/file.png"

    def generate_pdf(self, text, analysis_result, save_path=None):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        if os.path.exists(self.logo_path):
            pdf.image(self.logo_path, x=10, y=8, w=30)

        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(200, 10, " Rapport d'Analyse de Texte ", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, f" Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(15)

        # Résumé
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, "Résumé de l'Analyse :", ln=True, align='L')
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, f" Sentiment détecté : {analysis_result['sentiment']}")
        pdf.multi_cell(0, 8, f" Confiance du modèle : {analysis_result['confidence']}%")
        pdf.ln(5)

        # Texte avec surlignage
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, " Texte analysé (avec surlignage) :", ln=True, align='L')
        pdf.ln(5)

        keywords = analysis_result.get("keywords", {})
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0)

        words = text.split()
        line_height = 6

        for word in words:
            clean_word = word.strip(".,!?;:«»“”\"\'()").lower()
            if clean_word in keywords:
                pdf.set_font("Arial", style='B', size=12)
                pdf.set_text_color(200, 0, 0)
            else:
                pdf.set_font("Arial", style='', size=12)
                pdf.set_text_color(0, 0, 0)
            pdf.write(line_height, word + " ")

        pdf.ln(8)

        # Mots-clés
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, " Mots-clés détectés :", ln=True, align='L')
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        if keywords:
            pdf.multi_cell(0, 8, ", ".join(keywords.keys()))
        else:
            pdf.multi_cell(0, 8, "Aucun mot-clé détecté.")
        pdf.ln(5)

        # Statistiques
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, " Statistiques :", ln=True, align='L')
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, f" Nombre de mots analysés : {len(text.split())}")
        pdf.multi_cell(0, 8, f" Score de propagande : {analysis_result['confidence']}%")
        pdf.ln(10)

        # Signature
        pdf.set_font("Arial", style='I', size=10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, "Analyse générée automatiquement par le système - Projet ENSICAEN 2025", ln=True, align='C')
        pdf.set_text_color(0, 0, 0)

        # Camembert
        chart_path = generate_pie_chart(keywords)
        if chart_path:
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, "Répartition des mots-clés suspects :", ln=True, align='L')
            pdf.ln(5)
            pdf.image(chart_path, x=30, w=150)

        if save_path:
            pdf_filename = save_path
        else:
            pdf_filename = os.path.join(
                self.output_folder,
                f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )

        pdf.output(pdf_filename)
        return pdf_filename


        # Signature
        pdf.set_font("Arial", style='I', size=10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, "Analyse générée automatiquement par le système - Projet ENSICAEN 2025", ln=True, align='C')
        pdf.set_text_color(0, 0, 0)


        if save_path:
            pdf_filename = save_path
        else:
            pdf_filename = os.path.join(
                self.output_folder,
                f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )

        pdf.output(pdf_filename)
        return pdf_filename
