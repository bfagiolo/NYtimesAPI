import tkinter as tk
from datetime import datetime
import requests
from dateutil import parser
from article import Article
from database import has_already_searched, save_search_and_articles
import csv
from tkinter import filedialog
from visualizer import show_section_pie_chart

from database import initialize_database
initialize_database()


API_KEY = 'kbrEj0aqSPQRLIHZlZDciGNRc4ZJxC2p'  

PRIORITY_SECTIONS = {
    "World",
    "Politics",
    "U.S.",
    "Opinion",
    "Sports",
    "Business",
    "Technology",
    "Science"
}

articles_to_display = []


def export_to_csv():
    if not articles_to_display:
        return

    # location for saving csv file
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")],
                                             title="Save Articles As")
    if not file_path:
        return

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Section", "Summary", "URL", "Date"])
        for article in articles_to_display:
            writer.writerow([article.title, article.section, article.summary, article.url, article.pub_date])

def score(article):
    summary = article.get('abstract') or article.get('snippet', '')
    word_score = len(summary.split()) // 100
    section_score = 10 if article.get("section_name", "") in PRIORITY_SECTIONS else 0
    return word_score + section_score


def search_articles(entry):
    global articles_to_display
    global export_button
    result_box.delete(1.0, tk.END)
    export_button.config(state="disabled")
    graph_button.config(state="disabled")
    
    try:
        years_ago_raw = entry.get()
        years_ago = int(years_ago_raw)

        # validates input
        if "." in years_ago_raw or years_ago < 0 or years_ago > 172:
            raise ValueError
    except ValueError:
        result_box.tag_configure("error", foreground="red")
        result_box.insert(tk.END, "❌ Invalid input. Please search for a different year.\n", "error")
        return

    # forces loading message and force it to render
    result_box.insert(tk.END, f"🔍 Looking for NY Times articles on this day {years_ago} years ago...\n\n")
    result_box.update()

    # finds the target date
    today = datetime.today()
    target_year = today.year - years_ago
    month = today.month
    day = today.day
    actual_date_str = f"{target_year}-{month:02d}-{day:02d}"
    today_str = today.strftime("%Y-%m-%d")

    already_searched = has_already_searched(actual_date_str)
    if already_searched:
        result_box.insert(tk.END, f"✅ Already searched for {actual_date_str}. Displaying again (not saving).\n")


    url = f"https://api.nytimes.com/svc/archive/v1/{target_year}/{month}.json?api-key={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data["response"]["docs"]

        matching_articles = [
            article for article in articles
            if parser.parse(article["pub_date"]).day == day
        ]

        

        sorted_articles = sorted(matching_articles, key=score, reverse=True)
        top_articles = sorted_articles[:5]

        if not top_articles:
            result_box.insert(tk.END, "😔 No articles found for this date.\n")
            return

        articles_to_display = []
        for article in top_articles:
            title = article['headline']['main']
            section = article.get('section_name', 'Unknown')
            pub_date = article['pub_date'][:10]
            summary = article.get('abstract') or article.get('snippet', 'No summary available.')
            if len(summary.split()) > 30:
                summary = ' '.join(summary.split()[:30]) + "..."
            url = article['web_url']

            article_obj = Article(title, section, summary, url, pub_date)
            articles_to_display.append(article_obj)

        for a in articles_to_display:
            result_box.insert(tk.END, f"📅 {a.pub_date} | 🧠 {a.section}\n")
            result_box.insert(tk.END, f"📰 {a.title}\n")
            result_box.insert(tk.END, f"📝 {a.summary}\n")
            result_box.insert(tk.END, f"🔗 {a.url}\n\n")

        if not already_searched:
            save_search_and_articles(actual_date_str, today_str, articles_to_display)
        export_button.config(state="normal")
        graph_button.config(state="normal")

    except requests.RequestException as e:
        result_box.insert(tk.END, f"❌ Error fetching data: {e}")


# setup of my gui
root = tk.Tk()
root.title("New York Times Article Search")
root.geometry("850x600")
root.configure(padx=20, pady=20)

# the title
title_label = tk.Label(root, text="📰 New York Times Article Search", font=("Helvetica", 18, "bold"))
title_label.pack()

# top input row
top_frame = tk.Frame(root)
top_frame.pack(pady=10, fill='x')

today_str_label = tk.Label(top_frame, text=f"Today: {datetime.today().strftime('%B %d, %Y')}", font=("Helvetica", 12))
today_str_label.pack(side='left')

years_ago_label = tk.Label(top_frame, text="Years Ago (Max allowed: 172)", font=("Helvetica", 12))
years_ago_label.pack(side='right')

years_ago_entry = tk.Entry(top_frame, width=5)
years_ago_entry.insert(0, "0")  # 0 is default value
years_ago_entry.pack(side='right', padx=5)

# submit button
submit_button = tk.Button(root, text="Search", command=lambda: search_articles(years_ago_entry))
submit_button.pack(pady=5)

# the results text box
result_box = tk.Text(root, wrap="word", height=25, font=("Courier New", 11))
result_box.pack(fill="both", expand=True)

button_frame = tk.Frame(root)
button_frame.pack(fill='x', padx=10, pady=(0, 10))

export_button = tk.Button(button_frame, text="Export to CSV", state="disabled", command=export_to_csv)
export_button.pack(side="left")

graph_button = tk.Button(button_frame, text="Show Section Pie", command=lambda: show_section_pie_chart(articles_to_display), state="disabled")
graph_button.pack(side="left")

if __name__ == "__main__":
    root.mainloop()
