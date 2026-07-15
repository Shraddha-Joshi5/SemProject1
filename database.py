from pymongo import MongoClient

def connect_db():
    """
    Establishes connection to the local MongoDB instance 
    for general dementia project tracking.
    """
    try:
       
        client = MongoClient("mongodb://localhost:27017/")
        db = client["dementia_project"]
        print(" Connected successfully to MongoDB (dementia_project)!")
        return db
    except Exception as e:
        print(f" MongoDB Connection Error: {e}")
        return None
