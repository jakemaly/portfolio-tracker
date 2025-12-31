"""
Create the database table for stock holdings
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from config import DATABASE_PATH

class PortfolioDatabase:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path) #initialize the database connection if it doesn't exist
        self.create_holdings_table() #create the holdings table if it doesn't exist

    def create_holdings_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            shares REAL NOT NULL,
            purchase_price REAL NOT NULL,
            purchase_date TEXT NOT NULL
        );
        """
        cursor = self.connection.cursor() # used to interact with the database
        cursor.execute(create_table_query) #execute the create table query
        self.connection.commit() #commit the changes to the database

    def close(self):
        self.connection.close() #close the database connection