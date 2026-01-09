from pymongo import MongoClient
import copy

client = MongoClient("mongodb://localhost:27017/")
db = client["text_analysis_db"]
collection = db["extracted_insights"]

def save_to_db(data: dict):
    db_data = copy.deepcopy(data)   # 🔑 IMPORTANT LINE
    inserted = collection.insert_one(db_data)
    return str(inserted.inserted_id)
