from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

# Database connection settings
DB_HOST = "dpg-d0geqv49c44c73fgt840-a.frankfurt-postgres.render.com"
DB_NAME = "cardcatch_db"
DB_USER = "cardcatch_db_user"
DB_PASSWORD = MKAxKQSwVw4PE9li5sjHD7VjQfqqCBEL

# Connect to database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Basic health check
@app.get("/")
def read_root():
    return {"status": "CardCatch API is live"}

# Model for requests (if needed later)
class CardRequest(BaseModel):
    card_name: str

# Get card price by name (simple version for now)
@app.get("/get-card/{card_name}")
def get_card_price(card_name: str):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT card_name, set_name, clean_avg_value 
        FROM cards_master
        WHERE card_name ILIKE %s
        LIMIT 1
    """
    cur.execute(query, (f"%{card_name}%",))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        return {
            "card_name": result[0],
            "set_name": result[1],
            "clean_avg_value": result[2]
        }
    else:
        return {"error": "Card not found"}
