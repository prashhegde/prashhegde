import urllib
from flask import Flask, jsonify, request, render_template
from transformers import pipeline
import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

tqa = pipeline(task="table-question-answering", model="google/tapas-base-finetuned-wtq")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    user_query = request.form['query']

    # Assuming the getresult() function is responsible for fetching results
    result = getresult(user_query)

    return jsonify(result=result)

def connect_to_mongo():
    username = urllib.parse.quote_plus("prashanthegde26")
    password = urllib.parse.quote_plus("Prash@2618")
    uri = f"mongodb+srv://{username}:{password}@prashgenai.o10kpga.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)

    connection_string = f"mongodb+srv://{username}:{password}@prashgenai.o10kpga.mongodb.net/PrashGenAI?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    collection = client["PrashGenAI"]["PrashAI"]

    documents = collection.find()
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))

    return df

def getresult(query):
    # Move table fetching logic to connect_to_mongo function
    table = connect_to_mongo()
    table = table.drop(table.columns[0], axis=1)
    table = table.applymap(str)

    # Use the passed query parameter
    result = tqa(table=table, query=query)
    print(result["answer"])
    return result["answer"]

if __name__ == '__main__':
    app.run(debug=True)
