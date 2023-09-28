from pymongo import MongoClient
from decouple import config

# using connection string

MONGO_URI = config("MONGO_URI")
client = MongoClient(MONGO_URI)

# creating database

db = client.pytonCrud
