import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():

    # Get and parse education information from .env
    education_entries = json.loads(os.getenv("EDUCATION_JSON", "[]"))

    # Get and parse visited countries from .env
    countries_str = os.getenv("COUNTRIES", "")  # e.g., "USA,CAN,GBR"
    visited_countries = [code.strip() for code in countries_str.split(",") if code.strip()]

    return render_template('index.html', title="MLH Fellow", educations=education_entries, countries=visited_countries, url=os.getenv("URL"))

@app.route('/hobbies')
def hobby():
    img_path_prefix = "/static/img/hobby_imgs/"
    
    # Get and parse hobbies and image file names from .env
    raw_hobby_json = os.getenv("HOBBIES_JSON", "[]")
    parsed_hobby = json.loads(raw_hobby_json)
    
    # Add full image path to each hobby
    hobbies = [{"name": item["name"], "img": img_path_prefix + item["img"]} for item in parsed_hobby]

    return render_template('hobby.html', title="Hobbies", hobbies=hobbies)
