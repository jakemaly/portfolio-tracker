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
from config import DATABASE_PATH

class PortfolioDatabase:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.create_holdings_table() #create the holdings table if it doesn't exist

    def connect(self):
        """Create a database connection."""
        return sqlite3.connect(self.db_path)

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

        conn = self.connect() #create a connection to the database
        cursor = conn.cursor() #create a cursor object

        cursor.execute(create_table_query) #execute the create table query
        
        conn.commit() #commit the changes to the database
        conn.close() #close the connection

    def add_holding(self, ticker: str, shares: float, purchase_price: float, purchase_date: str, account: str = 'Default', notes: str = ''):
        """ Add a new stock holding to the database."""

        insert_query = """
        INSERT INTO holdings (ticker, shares, purchase_price, purchase_date, account, notes)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(insert_query, (ticker, shares, purchase_price, purchase_date, account, notes))

        conn.commit()
        conn.close()

    def get_holdings(self) -> list[dict]:
        """ Retrieve all stock holdings from the database. Returns a list of dictionaries."""

        select_query = "SELECT * FROM holdings ORDER BY purchase_date DESC;"

        conn = self.connect()
        conn.row_factory = sqlite3.Row # Returns rows as dictionaries
        cursor = conn.cursor()

        cursor.execute(select_query)

        results = cursor.fetchall()

        holdings = [dict(row) for row in results]
        
        conn.close()

        return holdings
    
    def get_holding_by_id(self, holding_id: int) -> dict | None:
        """ Retrieve a stock holding by its ID. Returns a dictionary or None if not found."""

        select_query = "SELECT * FROM holdings WHERE id = ?;"

        conn = self.connect()
        conn.row_factory = sqlite3.Row # Returns rows as dictionaries
        cursor = conn.cursor()

        cursor.execute(select_query, (holding_id,))

        result = cursor.fetchone()

        conn.close()

        return dict(result) if result else None
    
    def get_holdings_by_ticker(self, ticker: str) -> list[dict]:
        """ Retrieve stock holdings by ticker symbol. Returns a list of dictionaries."""

        select_query = "SELECT * FROM holdings WHERE ticker = ? ORDER BY purchase_date DESC;"

        conn = self.connect()
        conn.row_factory = sqlite3.Row # Returns rows as dictionaries
        cursor = conn.cursor()

        cursor.execute(select_query, (ticker,))

        results = cursor.fetchall()

        holdings = [dict(row) for row in results]
        
        conn.close()

        return holdings
    
    def get_unique_tickers(self) -> list[str]:
        """ Retrieve a list of unique ticker symbols from the holdings."""

        select_query = "SELECT DISTINCT ticker FROM holdings ORDER BY ticker;"

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(select_query)

        results = cursor.fetchall()

        tickers = [row[0] for row in results]
        
        conn.close()

        return tickers
    
    def update_holding(self, holding_id: int, ticker: str, shares: float, purchase_price: float, purchase_date: str, account: str = 'Default', notes: str = '') -> bool:
        """ Update a stock holding by its ID. Returns True if a row was updated, False otherwise."""

        update_query = """
        UPDATE holdings
        SET ticker = ?, shares = ?, purchase_price = ?, purchase_date = ?, account = ?, notes = ?
        WHERE id = ?;
        """

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(update_query, (ticker, shares, purchase_price, purchase_date, account, notes, holding_id))

        conn.commit()
        rows_updated = cursor.rowcount
        conn.close()

        return rows_updated > 0
    
    def delete_holding(self, holding_id: int) -> bool:
        """ Delete a stock holding by its ID. Returns True if a row was deleted, False otherwise."""

        delete_query = "DELETE FROM holdings WHERE id = ?;"

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(delete_query, (holding_id,))

        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()

        return rows_deleted > 0