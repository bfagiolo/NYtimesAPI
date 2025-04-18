

class Article:
    def __init__(self, title, section, summary, url, pub_date):
        self.title = title
        self.section = section
        self.summary = summary
        self.url = url
        self.pub_date = pub_date

    def display(self):
        print(f"📰 {self.title}")
        print(f"   🗂️ Section: {self.section}")
        if len(self.summary) > 5:
            print(f"   📝 {self.summary}")
        print(f"   🗓️ Published: {self.pub_date}")
        print(f"   🔗 {self.url}\n")
