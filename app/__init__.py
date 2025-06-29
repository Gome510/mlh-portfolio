import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))


@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html')


# Example for work experience
@app.route('/work')
def work():
    work_experiences = [
        {
            "title": "Software Engineer",
            "date": "2023 - Present",
            "company": "Tech Co",
            "bullets": [
                "Developed cool stuff.",
                "Led a team of 5."
            ]
        },
        # ...more jobs...
    ]
    return render_template('work_experience.html', work_experiences=work_experiences)
