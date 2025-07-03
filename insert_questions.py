import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://mounirongali99:z7eevIOrku7rN08o@cluster0.jvlw0p5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['quizdb']
questions_col = db['questions']

# Clear old questions
questions_col.delete_many({})

# Load from questions.json
with open('questions.json', 'r') as file:
    questions = json.load(file)

# Insert into MongoDB
questions_col.insert_many(questions)

print("Questions inserted successfully from JSON file.")
