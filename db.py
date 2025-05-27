from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.environ['MONGO_FLASK']

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Create database if they don't exist already
db = client['db_Flask']

# Create collection named data if it doesn't exist already
usersCollection = db['users']