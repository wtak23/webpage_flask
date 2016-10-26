# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify, render_template, request, url_for

app = Flask(__name__)

#*****************************************************************************#
# Setup relevant *config* parameters for flask app
# https://tedboy.github.io/flask/flask_doc.config.html
#*****************************************************************************#
app.config['DEBUG'] = True
app.config['GOOGLE_ANALYTICS']=True

@app.context_processor
def add_context_urlsite():
    """ Create context for function pointing to large binary files.

    I don't want Frozen-flask to keep copying large binary files to the 
    ``build`` directory, so decided to commit all my bulky files 
    once-and-for-all in my base github account.

    The function ``file_url`` can be used in any template files.

    See flask.pocoo.org/docs/0.11/templating/#context-processors

    Example
    -------
    <a href={{ file_url('pdf/stmi2014.pdf') }}>Author preprint (.pdf)</a>

    Above renders to
    <a href=http://takwatanabe.me/pdf/stmi2014.pdf>Author preprint (.pdf)</a>
    """
    def file_url(filename):
        return "http://takwatanabe.me/"+filename
    return dict(file_url=file_url)


@app.route("/")
@app.route("/index.html")
def index():
    return render_template('index.html',title=u"Takanori Watanabe (渡辺貴則)")

@app.route("/generic.html")
def generic():
    return render_template('generic.html',title="Generic Outline")

@app.route("/research.html")
def research():
    return render_template('research.html',title="Research")

@app.route("/plotly.html")
def plotly():
    return render_template('plotly.html',title="Plotly-demo")

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
    app.run(host='localhost', port= 8005)