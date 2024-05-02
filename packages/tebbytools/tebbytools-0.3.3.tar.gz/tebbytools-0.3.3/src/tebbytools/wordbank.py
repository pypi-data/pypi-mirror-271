import json
import os
import sqlite3
from datetime import datetime, timedelta

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_FILE_PATH = os.path.expanduser("~/tebbytools/wordbank.db")


class WordBank:
    """
    A class for managing a word bank for language learning.
    """

    def __init__(self, file_path=None):
        """
        Initialize LangBank with an optional database file path.
        If no file path is provided, a default one will be used.
        """
        if file_path is None:
            # Default file path: ~/langbank/bank.json
            self.file_path = DEFAULT_FILE_PATH
        else:
            self.file_path = file_path
        self.setup_bank()

    def set_file_path(self, file_path):
        """
        Set the file path for the word bank.
        """
        self.file_path = file_path

    def setup_bank(self):
        """
        Create the word bank database file and parent directories if they do not exist.
        """
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self.create_table()

    def create_connection(self):
        """
        Create a connection to the SQLite database.
        Returns:
            The connection object.
        """
        return sqlite3.connect(self.file_path)

    def create_table(self):
        """
        Create the word bank table in the SQLite database.
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS wordbank (
                word TEXT NOT NULL,
                datetime TEXT NOT NULL,
                tags TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def add_word(self, word, date_time=datetime.now(), tags=None):
        """
        Add a new word to the wordbank
        Args:
            word: the word to add
            tags: a list of string tags
        """
        tags_str = json.dumps(tags) if tags else None
        date_time_str = date_time.strftime(DATETIME_FORMAT)
        conn = self.create_connection()
        c = conn.cursor()
        # Insert the word into the database
        c.execute(
            """
            INSERT INTO wordbank (word, datetime, tags)
            VALUES (?, ?, ?)
            """,
            (word, date_time_str, tags_str),
        )
        conn.commit()
        conn.close()

    def get_all_words(self):
        """
        Get a list of all the words in the bank
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute("SELECT word FROM wordbank")
        words = [row[0] for row in c.fetchall()]
        conn.close()
        return words

    def get_all_unique_words(self):
        """
        Get a list of all the unique words in the bank
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute("SELECT DISTINCT word FROM wordbank")
        words = [row[0] for row in c.fetchall()]
        conn.close()
        return words

    def get_words_from_past_n_days(self, n=0):
        """
        Get a list of all the words added in the past n days, where n=0 will return the words added today
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute(
            """
            SELECT word FROM wordbank
            WHERE datetime >= ?
            """,
            ((datetime.now() - timedelta(days=n)).strftime(DATETIME_FORMAT),),
        )
        words = [row[0] for row in c.fetchall()]
        conn.close()
        return words

    def get_todays_words(self):
        """
        Get the list of words added today
        """
        return self.get_words_from_past_n_days(0)

    def get_todays_new_words(self):
        """
        Get a list of the words added today that only appear once in the bank
        """
        todays_words = self.get_todays_words()
        new_words = [word for word in todays_words if self.occurences(word) == 1]
        return new_words

    def get_words_by_tag(self, tag):
        """
        Get a list of all the words with a specific tag
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute(
            """
            SELECT word FROM wordbank
            WHERE tags LIKE ?
            """,
            (f"%{tag}%",),
        )
        words = [row[0] for row in c.fetchall()]
        conn.close()
        return words

    def get_words_by_date(self, date):
        """
        Get a list of all the words added on a specific date
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute(
            """
            SELECT word FROM wordbank
            WHERE datetime LIKE ?
            """,
            (f"{date}%",),
        )
        words = [row[0] for row in c.fetchall()]
        conn.close()
        return words

    def occurences(self, word):
        """
        Get the number of times a word has been added to the bank
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute(
            """
            SELECT COUNT(*) FROM wordbank
            WHERE word = ?
            """,
            (word,),
        )
        count = c.fetchone()[0]
        conn.close()
        return count
