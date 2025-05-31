from pymongo import MongoClient

# Local MongoDB Compass URI
client = MongoClient("mongodb://localhost:27017")

# Database and Collections
db = client['math_chatbot']
users_collection = db['users']
chat_collection = db['chats']
