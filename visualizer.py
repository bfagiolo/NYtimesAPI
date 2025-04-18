
import matplotlib.pyplot as plt
from collections import Counter


def show_section_pie_chart(articles):
    if not articles:
        return

    sections = [article.section for article in articles]
    counter = Counter(sections)

    plt.figure(figsize=(6, 6))
    plt.pie(counter.values(), labels=counter.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Article Section Breakdown")
    plt.axis('equal')
    plt.show()
