import sqlite3
import pandas as pd

DB_NAME = "ai_register.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            vendor TEXT,
            department TEXT,
            purpose TEXT,
            data_classification TEXT,
            risk_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def insert_tool(tool_name, vendor, department, purpose, data_classification, risk_level):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ai_tools 
        (tool_name, vendor, department, purpose, data_classification, risk_level)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tool_name, vendor, department, purpose, data_classification, risk_level))

    conn.commit()
    conn.close()

def get_tools():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM ai_tools ORDER BY created_at DESC", conn)
    conn.close()
    return df