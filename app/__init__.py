import os
import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)

print(mydb)

class TimelinePost (Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name:
        return "Invalid name", 400
    if not email or "@" not in email:
        return "Invalid email", 400
    if not content:
        return "Invalid content", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return jsonify(model_to_dict(timeline_post))

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/')
def index():
    work_experiences = [
        {
            "title": "Software Development Intern",
            "date": "Feb 2024 - Dec 2024",
            "company": "Abbott Diabetes Care",
            "bullets": [
                "Developed features for Abbott mobile apps, improving usability and engagement for patients and providers.",
                "Created new user tutorials and configuration options for React Native mobile apps.",
                "Achieved 90% test coverage on mobile app screens and UI library using react-testing-library and reg-viz/storycap, decreasing bug reports by 15%.",
                "Developed data visualizations for the UI library with D3.js, used in 32 instances across 3 apps.",
                "Documented the UI library with Storybook and tested with functional and visual regression tests."
            ]
        },
        {
            "title": "Software Engineering Intern",
            "date": "Jul 2024 - Sep 2024",
            "company": "Coforma",
            "bullets": [
                "Developed tools for government reporting to support the Centers for Medicare & Medicaid Services.",
                "Created a script to generate Storybook files, saving 60+ hours across 100+ components.",
                "Documented APIs with Swagger, boosting backend development speed by 50%.",
                "Standardized project READMEs to cut documentation time by 80%."
            ]
        },
        {
            "title": "Shopify Web Developer & UX Writer",
            "date": "May 2023 - Mar 2024",
            "company": "Phil's Drills",
            "bullets": [
                "Managed and optimized e-commerce operations to improve product visibility and streamline checkout processes.",
                "Optimized user interfaces and Shopify themes, raising sales by 141% and reducing cart abandonment by 34%."
            ]
        },
        {
            "title": "Web Development Intern",
            "date": "Jul 2023 - Dec 2023",
            "company": "Bay Valley Tech",
            "bullets": [
                "Built and deployed 5 React apps with Vercel, reducing Firebase workflows to cut development time by 40%."
            ]
        },
        {
            "title": "Web Design Teacher",
            "date": "Aug 2023 - Dec 2023",
            "company": "Arise High School",
            "bullets": [
                "Guided 20+ high school students to create portfolio websites, boosting technical proficiency and digital literacy."
            ]
        }
    ]
    educations = [
        {
            "degree": "Master of Education & Teaching Credential",
            "date": "2022",
            "school": "University of California: Santa Cruz"
        },
        {
            "degree": "Bachelor of Math Education",
            "date": "2021",
            "school": "University of California: Santa Cruz"
        },
        {
            "degree": "Associate of Computer Programming",
            "date": "2025",
            "school": "Laney College"
        }
    ]
    hobbies = [
        "Urban Photography",
        "Board Game Design"
    ]
    return render_template(
        'index.html',
        work_experiences=work_experiences,
        educations=educations,
        hobbies=hobbies,
        title="MLH Fellow",
        url=os.getenv("URL")
    )


@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html')

@app.route('/timeline')
def timeline():
    posts = [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]
    return render_template('timeline.html', posts=posts)