import sqlite3
import pandas as pd
import logging
import io
from pathlib import Path

class Database:
    def __init__(self):
        # Get current directory where database.py is located
        current_dir = Path(__file__).parent
        # Create a 'data' directory
        data_dir = current_dir / 'data'
        data_dir.mkdir(exist_ok=True)
        # Set database path
        self.db_path = data_dir / 'properties.db'
        self.conn = None
        self.cursor = None
        self.connect()
        self.setup_database()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            raise

    def setup_database(self):
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY,
                name TEXT,
                host_id INTEGER,
                host_name TEXT,
                neighbourhood_group TEXT,
                neighbourhood TEXT,
                latitude REAL,
                longitude REAL,
                room_type TEXT,
                price INTEGER,
                minimum_nights INTEGER,
                number_of_reviews INTEGER,
                last_review TEXT,
                reviews_per_month REAL,
                calculated_host_listings_count INTEGER,
                availability_365 INTEGER,
                number_of_reviews_ltm INTEGER,
                license TEXT
            )
        ''')

        # Your sample data loading code here
        self.load_sample_data()
        self.conn.commit()

    def load_sample_data(self):
        # Your existing data string and loading logic
        # data = """address|price|bedrooms|bathrooms|description
        # 123 Main St|300000|3|2|Beautiful house with garden, close to schools
        # 456 Oak Ave|450000|4|3|Spacious family home, recently renovated kitchen
        # 789 Pine Rd|275000|2|1|Cozy starter home, great for first-time buyers"""

        df = pd.read_csv('la_listings_vis.csv')

        #df = pd.read_csv(io.StringIO(data), sep='|')
        df.to_sql('properties', self.conn, if_exists='replace', index=False)

    def execute_query(self, query):
        try:
            result = pd.read_sql_query(query, self.conn)
            return result
        except Exception as e:
            logging.error(f"Error executing SQL query: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()