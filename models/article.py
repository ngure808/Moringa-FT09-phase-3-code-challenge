from database.connection import get_db_connection



class Article:
    def __init__(self, title, content, author, magazine):
        self._id = None
        self._title = self.validate_title(title)
        self._content = self.validate_content(content)
        self._author = author
        self._magazine = magazine
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author.id

    @property
    def magazine_id(self):
        return self._magazine.id

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                       (self._title, self._content, self._author.id, self._magazine.id))
        conn.commit()
        self._id = cursor.lastrowid

    @staticmethod
    def validate_title(title):
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if not (5 <= len(title) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        return title

    @staticmethod
    def validate_content(content):
        if not isinstance(content, str):
            raise ValueError("Content must be a string")
        return content

    @property
    def author(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?
        ''', (self.id,))
        row = cursor.fetchone()
        return Author(row["id"], row["name"]) if row else None

    @property
    def magazine(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        ''', (self.id,))
        row = cursor.fetchone()
        return Magazine(row["id"], row["name"], row["category"]) if row else None

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS articles')
        conn.commit()
