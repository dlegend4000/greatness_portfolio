import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/hobbies')
def hobby():
    img_path_prefix = "/static/img/hobby_imgs/"
    
    # Get and parse hobbies and image file names from .env
    raw_hobbies = os.getenv("HOBBIES", "")
    hobbies_name = [h.strip() for h in raw_hobbies.split(",") if h.strip()]
    
    raw_hobbies_imgs = os.getenv("HOBBIES_IMGS", "")
    hobbies_imgs = [img_path_prefix + img.strip() for img in raw_hobbies_imgs.split(",") if img.strip()]
    
    # Zip hobby names with corresponding image paths
    hobbies = list(zip(hobbies_name, hobbies_imgs))

    return render_template('hobby.html', title="Hobbies", hobbies=hobbies)
