import os
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json


load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():

    try:
        about_info = json.loads(os.getenv("ABOUT_JSON", "{}"))
        education_entries = json.loads(os.getenv("EDUCATION_JSON", "[]"))
        experiences = json.loads(os.getenv("EXPERIENCE_JSON", "[]"))
        countries_str = os.getenv("COUNTRIES", "")  # e.g., "USA,CAN,GBR"
        visited_countries = [code.strip() for code in countries_str.split(",") if code.strip()]
    except json.JSONDecodeError as e:
        print("Error parsing EXPERIENCE_JSON:", e)
        about_info = {}
        education_entries = []
        experiences = []
        visited_countries = []

    return render_template('index.html', title="MLH Fellow", about_info=about_info, educations=education_entries, experiences=experiences, countries=visited_countries, url=os.getenv("URL"))
  
@app.route('/hobbies')
def hobby():
    img_path_prefix = "/static/img/hobby_imgs/"
    
    # Get and parse hobbies and image file names from .env
    raw_hobby_json = os.getenv("HOBBIES_JSON", "[]")
    parsed_hobby = json.loads(raw_hobby_json)
    
    # Add full image path to each hobby
    hobbies = [{"name": item["name"], "img": img_path_prefix + item["img"]} for item in parsed_hobby]

    return render_template('hobby.html', title="Hobbies", hobbies=hobbies)