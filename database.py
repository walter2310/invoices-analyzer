import pg8000
from dotenv import load_dotenv
import os
from io import StringIO

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = pg8000.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

def save_to_database(df):
    """Save DataFrame to PostgreSQL database"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return False

        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_date VARCHAR(20),
            supplier VARCHAR(255),
            description TEXT,
            amount NUMERIC(10,2),
            currency VARCHAR(20),
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Convert DataFrame to list of tuples
        data_tuples = [tuple(x) for x in df.to_numpy()]

        # SQL insert query
        insert_query = """
        INSERT INTO invoices (
            invoice_date,
            supplier,
            description,
            amount,
            currency
        ) VALUES (%s, %s, %s, %s, %s)
        """

        # Execute batch insert
        cursor.executemany(insert_query, data_tuples)

        conn.commit()
        print(f"✅ Successfully inserted {len(df)} records")
        return True

    except Exception as e:
        print("Error saving to database:", e)
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()