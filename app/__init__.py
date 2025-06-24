import os
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from pathlib import Path


load_dotenv()
app = Flask(__name__)

personal_info_path = Path(__file__).with_name("personal_info.json")
    
with open(personal_info_path, encoding="utf-8") as pif:
    personal_info = json.load(pif)


@app.route('/')
def index():

    about_info   = personal_info.get("about", {})
    educations   = personal_info.get("education", [])
    experiences  = personal_info.get("experience", [])
    countries    = personal_info.get("countries", [])
    
    return render_template('index.html', title="MLH Fellow", about_info=about_info, educations=educations, experiences=experiences, countries=countries, url=os.getenv("URL"))
  
@app.route('/hobbies')
def hobby():
    
    hobbies  = personal_info.get("hobbies", [])
    
    return render_template('hobby.html', title="Hobbies", hobbies=hobbies)