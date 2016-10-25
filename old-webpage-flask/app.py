from flask import Flask
from flask import jsonify, render_template, request, url_for, g

from os import path

app = Flask(__name__)

#-----------------------------------------------------------------------------#
# define global variables that can be accessed from any template
# https://tedboy.github.io/flask/flask_doc.templating.html#context-processors
#-----------------------------------------------------------------------------#
# location of my pdf files
app.config['PDF_PATH']="http://takwatanabe.me/pdf/"

@app.context_processor
def func_url_pdf():
    """ Create function for context processor, pointing to pdf url

    Example
    -------
    <a href={{ pdf_file('stmi2014.pdf') }}>Author preprint (.pdf)</a>

    Above renders to
    <a href=http://takwatanabe.me/pdf/stmi2014.pdf>Author preprint (.pdf)</a>
    """
    def pdf_file(filename):
        return app.config['PDF_PATH']+filename
    return dict(pdf_file=pdf_file)

#-----------------------------------------------------------------------------#
# config values in flask app
# https://tedboy.github.io/flask/flask_doc.config.html
#-----------------------------------------------------------------------------#
# relevant configs
app.config['DEBUG'] = True
app.config['GOOGLE_ANALYTICS']=True

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
@app.route("/courses.html")
def courses():
    return render_template('courses.html')

@app.route("/resources.html")
def resources():
    return render_template('resources.html')

@app.route("/research.html")
def research():
    return render_template('research.html')

if __name__ == '__main__':
    app.run(host='localhost', port= 8018)