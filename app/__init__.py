import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import json
from pathlib import Path
from peewee import MySQLDatabase
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)

personal_info_path = Path(__file__).with_name("personal_info.json")
    
with open(personal_info_path, encoding="utf-8") as pif:
    personal_info = json.load(pif)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost], safe=True)

#POst API Endpoints
@app.route('/api/timeline_post', methods=['POST'])
def add_timeline_post():
    data = request.form or request.get_json()

    # Validate input
    name = data.get('name')
    email = data.get('email')
    content = data.get('content')

    if not name:
        return jsonify({"error": "Invalid name"}), 400
    if not content:
        return jsonify({"error": "Invalid content"}), 400
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email"}), 400

    post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(post), 201

# Get API Endpoint
@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_posts():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    posts_list = [model_to_dict(post) for post in posts]
    return jsonify(posts_list)

# Delete API Endpoint
@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        post = TimelinePost.get_by_id(post_id)
        post.delete_instance()
        return jsonify({'message': 'Deleted successfully'}), 200
    except TimelinePost.DoesNotExist:
        return jsonify({'error': 'Post not found'}), 404

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


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")


