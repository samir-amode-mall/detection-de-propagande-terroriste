import matplotlib.pyplot as plt
from collections import Counter
import re

def generate_pie_chart(word_freq, output_path="chart.png"):
    if not word_freq:
        return None

    labels = list(word_freq.keys())
    sizes = list(word_freq.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    return output_path

def highlight_keywords_in_text(text, keywords):
    if not keywords:
        return text

    sorted_keywords = sorted(keywords.keys(), key=len, reverse=True)

    for word in sorted_keywords:
        pattern = re.compile(rf'\b({re.escape(word)})\b', re.IGNORECASE)
        text = pattern.sub(r'[\1]', text)

    return text
