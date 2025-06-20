import os
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():

    try:
        experiences = json.loads(os.getenv("EXPERIENCE_JSON", "[]"))
        education= json.loads(os.getenv("EDUCATION_JSON", "[]"))
        hobbies= json.loads(os.getenv("HOBBIES_JSON", "[]"))
    except json.JSONDecodeError as e:
        print("Error parsing EXPERIENCE_JSON:", e)
        experiences = []
        education = []
        hobbies = []


    return render_template('index.html', title="MLH Fellow", experiences=experiences, education=education, hobbies=hobbies, url=os.getenv("URL"))
