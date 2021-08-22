import sqlite3
import sys
from pathlib import Path


class feeds_db:
    def __init__(self, database):
        db = Path(database)
        self.db = sqlite3.connect(db)
        self.init_table()

    def init_table(self):
        c = self.db.cursor()
        try:
            c.execute("""
                CREATE TABLE IF NOT EXISTS feeds (
                    service TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    link TEXT,
                    guid TEXT,
                    pub_date TIMESTAMP NOT NULL,
                    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    isdeleted INTEGER DEFAULT 0 NOT NULL,
                    UNIQUE(service,title,pub_date)
                );
                """)
        except sqlite3.OperationalError as e:
            print(e)
            print("Could not initialize the feeds table :(")
            sys.exit(1)

    def insert_entry(self, service, title, desc, link, guid, pub_date):
        c = self.db.cursor()
        q = """
        INSERT INTO
            feeds (service, title, description, link, guid, pub_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            c.execute(q, (service, title, desc, link, guid, pub_date))
            print(f"\tadding {service} entry: {title}")
            self.db.commit()
        except sqlite3.IntegrityError:
            # failed to insert row because of UNIQUE constraint. carry on
            pass

    def get_entries(self):
        self.db.row_factory = sqlite3.Row
        c = self.db.cursor()
        c.execute("""
            SELECT * from feeds
                WHERE pub_date BETWEEN date('now','-1 day') AND date('now','+1 day')
                ORDER BY pub_date DESC
            """)
        return c.fetchall()
