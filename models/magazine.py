from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category):
        self._id = None
        self._name = self.validate_name(name)
        self._category = self.validate_category(category)
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        conn.commit()
        self._id = cursor.lastrowid

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if not (2 <= len(name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        return name

    @staticmethod
    def validate_category(category):
        if not isinstance(category, str):
            raise ValueError("Category must be a string")
        if len(category) == 0:
            raise ValueError("Category must be longer than 0 characters")
        return category

    def articles(self):
        from models.article import Article
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        return [Article(row["id"], row["title"], row["content"], Author(row["author_id"], ""), self) for row in rows]

    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        return [Author(row["id"], row["name"]) for row in rows]

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS magazines')
        conn.commit()

    def article_titles(self):
        # Fetch articles associated with the magazine
        articles = self.articles()
        # If no articles found, return None
        if not articles:
            return None
        # Extract titles from articles
        titles = [article.title for article in articles]
        return titles

    def contributing_authors(self):
        from models.author import Author
        # Fetch articles associated with the magazine
        articles = self.articles()
        # If no articles found, return None
        if not articles:
            return None
        # Count the number of articles written by each author
        author_counts = {}
        for article in articles:
            if article.author_id in author_counts:
                author_counts[article.author_id] += 1
            else:
                author_counts[article.author_id] = 1
        # Filter authors who have written more than 2 articles
        contributing_authors = []
        for author_id, count in author_counts.items():
            if count > 2:
                author = Author.find_by_id(author_id)
                if author:
                    contributing_authors.append(author)
        # If no authors found, return None
        if not contributing_authors:
            return None
        return contributing_authors
