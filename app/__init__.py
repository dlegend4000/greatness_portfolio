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
from peewee import OperationalError

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
        port=3306,
        # Add connection pool settings
        max_connections=20,
        stale_timeout=300,
        timeout=20
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

# Improved database connection handling
def ensure_db_connection():
    """Ensure database connection is active, reconnect if needed"""
    try:
        if mydb.is_closed():
            mydb.connect()
            print("Database reconnected")
    except Exception as e:
        print(f"Database reconnection failed: {e}")
        # Try to reconnect
        try:
            mydb.close()
            mydb.connect()
            print("Database reconnected after close")
        except Exception as e2:
            print(f"Database reconnection after close failed: {e2}")
            raise e2

# Initialize database connection
def init_db():
    try:
        mydb.connect()
        mydb.create_tables([TimelinePost], safe=True)
        print("Database connected successfully")
    except Exception as e:
        print(f"Database connection failed: {e}")
        # Don't fail startup, let it retry later

# Try to connect on startup, but don't fail if it doesn't work
init_db()

# Improved API endpoints with connection handling
@app.route('/api/timeline_post', methods=['POST'])
def add_timeline_post():
    try:
        ensure_db_connection()
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
    except OperationalError as e:
        print(f"Database operation failed: {e}")
        return jsonify({"error": "Database error, please try again"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Get API Endpoint with improved connection handling
@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_posts():
    try:
        ensure_db_connection()
        posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        posts_list = [model_to_dict(post) for post in posts]
        return jsonify(posts_list)
    except OperationalError as e:
        print(f"Database operation failed: {e}")
        return jsonify({"error": "Database error, please try again"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Delete API Endpoint with improved connection handling
@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        ensure_db_connection()
        post = TimelinePost.get_by_id(post_id)
        post.delete_instance()
        return jsonify({'message': 'Deleted successfully'}), 200
    except TimelinePost.DoesNotExist:
        return jsonify({'error': 'Post not found'}), 404
    except OperationalError as e:
        print(f"Database operation failed: {e}")
        return jsonify({"error": "Database error, please try again"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

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


