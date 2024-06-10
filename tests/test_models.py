import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):

    def test_author_creation(self):
        author = Author("John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        magazine = Magazine("Tech Weekly", "Technology")
        author = Author("John Doe")
        article = Article("Test Title", "Test Content", author, magazine)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine("Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_author_name_change(self):
        author = Author("John Doe")
        with self.assertRaises(AttributeError):
            author.name = "Jane Doe"

    def test_author_name_type(self):
        with self.assertRaises(ValueError):
            author = Author(123)

    def test_author_name_length(self):
        with self.assertRaises(ValueError):
            author = Author("")

    def test_author_articles(self):
        author = Author("John Doe")
        articles = author.articles()
        self.assertEqual(len(articles), 0) 

    def test_author_magazines(self):
        author = Author("John Doe")
        magazines = author.magazines()
        self.assertEqual(len(magazines), 0)  

    def test_article_title_length(self):
        with self.assertRaises(ValueError):
            magazine = Magazine("Tech Weekly", "Technology")
            author = Author("John Doe")
            article = Article("", "Test Content", author, magazine)

    def test_magazine_name_type(self):
        with self.assertRaises(ValueError):
            magazine = Magazine(123, "Technology")

    def test_magazine_name_length(self):
        with self.assertRaises(ValueError):
              magazine = Magazine("", "Technology")

    def test_magazine_articles(self):
        magazine = Magazine("Tech Weekly", "Technology")
        articles = magazine.articles()
        self.assertEqual(len(articles), 0)  

    def test_magazine_contributors(self):
        magazine = Magazine("Tech Weekly", "Technology")
        contributors = magazine.contributors()
        self.assertEqual(len(contributors), 0)  

    def test_magazine_article_titles(self):
        magazine = Magazine("Tech Weekly", "Technology")
        titles = magazine.article_titles()
        self.assertIsNone(titles)  

    def test_magazine_contributing_authors(self):
        magazine = Magazine("Tech Weekly", "Technology")
        contributing_authors = magazine.contributing_authors()
        self.assertIsNone(contributing_authors)  

if __name__ == "__main__":
    unittest.main() 