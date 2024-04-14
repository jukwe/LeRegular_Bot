import psycopg2
import json
from cryptography.fernet import Fernet


file = open('.vscode/settings.json')

data = json.load(file)

username = data['sqltools.connections'][0]['username']
hostname = data['sqltools.connections'][0]['server']
port = data['sqltools.connections'][0]['port']
database = data['sqltools.connections'][0]['database']

password = 'LeRegularly'
# Configuration for  PostgreSQL connection
DATABASE_URL = f"postgres://{username}:{password}@{hostname}:{port}/{database}"

def initialize_db():
    # Connect to  PostgreSQL database
    conn = psycopg2.connect(DATABASE_URL)
    
    # Create a cursor object
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('CREATE TABLE IF NOT EXISTS user_wallets (user_id BIGINT PRIMARY KEY, wallet_keypair TEXT)')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_user_wallet(user_id, wallet_keypair):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Insert a row of data
    cursor.execute('INSERT INTO user_wallets (user_id, wallet_keypair) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING', (user_id, wallet_keypair))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_user_wallet(user_id):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("SELECT wallet_keypair FROM user_wallets WHERE user_id = %s", (user_id,))
    data = cursor.fetchone()
    
    conn.close()
    
    if data:
        return data[0]
    return None