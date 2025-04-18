import unittest
from mainNYtimes import score  

PRIORITY_SECTIONS = {
    "World", "Politics", "U.S.", "Opinion", "Sports", "Business", "Technology", "Science"
}

class TestScoring(unittest.TestCase):
    def test_score_priority_section(self):
        article = {
            'abstract': "This is a very short summary.",
            'section_name': 'World'
        }
        self.assertEqual(score(article), 10)

    def test_score_non_priority_section(self):
        article = {
            'abstract': "This is a very short summary.",
            'section_name': 'Fashion'
        }
        self.assertEqual(score(article), 0)

    def test_score_long_summary(self):
        article = {
            'abstract': " ".join(["word"] * 250),  
            'section_name': 'U.S.'
        }
        self.assertEqual(score(article), 10 + (250 // 100))

if __name__ == '__main__':
    unittest.main()
