import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    experiences = [
        {
            "role": "Software Engineering Intern",
            "company": "JP Morgan Chase & Co.",
            "duration": "June 2024 – August 2024",
            "details": [
                "Developed a back-end application using Java Spring Boot, Terraform, Docker, and AWS to perform data validation and quality checks.",
                "Created a RESTful API with MySQL to store and manage data.",
                "Resolved critical data quality bugs, helping protect the security of over 80 million clients globally."
            ]
        },
        {
            "role": "Data Analyst Intern",
            "company": "Wuxi Biologics",
            "duration": "January 2023 – September 2023",
            "details": [
                "Performed analytics and visualizations on large datasets.",
                "Automated dashboard generation using R, Python, SQL, and Tableau, improving team efficiency.",
                "Resolved key Microsoft SQL issues involving over 50,000 rows of data."
            ]
        },
        {
            "role": "Mechanical Engineering Intern",
            "company": "Silent Aire",
            "duration": "July 2022 - September 2022",
            "details": [
                "Carrying out pressure/leak analysis on the doors and coming up with a design solution hence boosting its efficiency.",
                "Designing plans and specifying dimensions to be followed in building HVAC systems for data centers.",
                "Observing and documenting the Standard operating procedures for each role involved in building our hyperscale ventilation systems."
            ]
        }


    ]

    education = [
        {
            "degree": "BSc Mechanical Engineering",
            "institution": "Dublin City University",
            "duration": "2021 – 2025",
            "details": [
                "Class rep for two years"
            ]
        }

    ]

    hobbies = [
        "I love to listen to Music, I also play the piano and guitar",
        "I love Gaming, I play games like Fifa and Call of Duty all the time"
    ]    
    return render_template('index.html', title="MLH Fellow", experiences=experiences, education=education, hobbies=hobbies, url=os.getenv("URL"))
