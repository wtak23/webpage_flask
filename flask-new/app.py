from flask import Flask
from flask import jsonify, render_template, request, url_for
app = Flask(__name__)

app.config['DEBUG'] = True


options = dict(google_analytics = False)


@app.route("/")
@app.route("/index.html")
def index():
    return render_template('index.html',title="Welcome to Tak's homepage")

@app.route("/generic.html")
def generic():
    return render_template('generic.html',title="Generic Outline")

@app.route("/research.html")
def research():
    return render_template('research.html',title="Research")

@app.route("/courses.html")
def courses():
    return render_template('courses.html',title="Courses")

@app.route("/resources.html")
def resources():
    return render_template('resources.html',title="Resources")

@app.route("/elements.html")
def elements():
    return render_template('elements.html',title="Elements")


if __name__ == '__main__':
    app.run(host='localhost', port= 8000)