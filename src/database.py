"""
Create the database table for stock holdings

Database schema:
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- ticker: TEXT NOT NULL (e.g., 'AAPL')
- shares: REAL NOT NULL (e.g., 10.5)
- purchase_price: REAL NOT NULL (e.g., 150.25)
- purchase_date: TEXT NOT NULL (e.g., '2023-10-15')
- account: TEXT (e.g., 'TFSA')
- notes: TEXT (optional notes about the holding)
- created_at: TEXT DEFAULT CURRENT_TIMESTAMP (timestamp when the record was created)
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

    def close(self):
        self.connection.close() #close the database connection

    def create_holdings_table(self):
        """Create the holdings table in the database if it doesn't exist."""

        create_table_query = """
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            shares REAL NOT NULL,
            purchase_price REAL NOT NULL,
            purchase_date TEXT NOT NULL,
            account TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor = self.connection.cursor() # used to interact with the database
        cursor.execute(create_table_query) #execute the create table query
        self.connection.commit() #commit the changes to the database
        cursor.close() #close the cursor

    def add_holding(self, ticker: str, shares: float, purchase_price: float, purchase_date: str, account: str = 'Default', notes: str = ''):
        """ Add a new stock holding to the database."""

        insert_query = """
        INSERT INTO holdings (ticker, shares, purchase_price, purchase_date, account, notes)
        VALUES (?, ?, ?, ?, ?, ?);
        """

        cursor = self.connection.cursor()
        cursor.execute(insert_query, (ticker, shares, purchase_price, purchase_date, account, notes))
        self.connection.commit()
        cursor.close()

    def get_holdings(self):
        """ Retrieve all stock holdings from the database."""

        select_query = "SELECT * FROM holdings ORDER BY purchase_date DESC;"

        cursor = self.connection.cursor()
        cursor.execute(select_query)
        results = cursor.fetchall()

        holdings = [dict(id=row[0], ticker=row[1], shares=row[2], purchase_price=row[3],
                         purchase_date=row[4], account=row[5], notes=row[6], created_at=row[7]) for row in results]
        
        cursor.close()
        return holdings
    
    