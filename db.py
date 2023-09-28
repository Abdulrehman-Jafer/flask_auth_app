from pymongo import MongoClient

# using connection string
client = MongoClient(
    "mongodb+srv://Abdulrehman-Jafer:Paswordhai2007@node-cluster.e3ibxci.mongodb.net/pytonCrud?retryWrites=true&w=majority"
)

# creating database

db = client.pytonCrud
