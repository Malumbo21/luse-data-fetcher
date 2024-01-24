import os
from datetime import date
import hashlib
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import (credentials, firestore)

class Config:
    collection = "stock_data"


load_dotenv()

creds_file_path = os.environ.get("LISA_FIREBASE_CREDENTIALS_PATH", "credentials.json")
if not os.path.exists(creds_file_path):
    raise Exception("Credentials file path does not exist")
try:
    creds = credentials.Certificate(creds_file_path)
    firebase_admin.initialize_app(creds)
except Exception as e:
    print(e)

def create_document(data, collection=Config.collection):
    db = firestore.client()

    doc_exists = db.collection(collection).where("hash", "==", data["hash"])
    if doc_exists:
        return 1
    ref = db.collection(collection).document()
    ref.set(data)
    return 0
# todo 
def get_documents(collection=Config.colleciton,isntrument=None, start=None, end=None):
    docs = []
    db = firestore.client()
    ref = db.collection(collection)

    docs = ref.get()
    for doc in docs:
        docs.append({
            "id": doc.id,
            "data": doc.to_dict()
        })
    return docs
def generate_dict(date=None, instrument=None, bid_qty=None, bid_price=None,
                  ask_price=None, ask_qty=None, last_trade_price=None, net_change=None,
                  closing_price=None, total_turnover=None, average_price=None,
                  last_traded_size=None, week_52_high=None, week_52_low=None,
                  opening_price=None, change=None, previous_closing_price=None,
                  total_trades=None, trade_volume=None, foreign_buys=None, foreign_sells=None):
    """
    Generate a dictionary based on the provided column definitions.

    Parameters:
    - Include parameters for each column in your definitions.

    Returns:
    - dict: Generated dictionary.
    """
    md5_hash = hashlib.md5(f"{instrument}{str(date)}".encode()).hexdigest()
    return {
        'hash': md5_hash, # used to check if the data for a stock on a specific date already exists
        'date': date,
        'instrument': instrument,
        'bid_qty': bid_qty,
        'bid_price': bid_price,
        'ask_price': ask_price,
        'ask_qty': ask_qty,
        'last_trade_price': last_trade_price,
        'net_change': net_change,
        'closing_price': closing_price,
        'total_turnover': total_turnover,
        'average_price': average_price,
        'last_traded_size': last_traded_size,
        'week_52_high': week_52_high,
        'week_52_low': week_52_low,
        'opening_price': opening_price,
        'change': change,
        'previous_closing_price': previous_closing_price,
        'total_trades': total_trades,
        'trade_volume': trade_volume,
        'foreign_buys': foreign_buys,
        'foreign_sells': foreign_sells,
    }