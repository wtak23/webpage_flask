from flask import Flask
from flask import jsonify, render_template, request, url_for, g

from os import path

#*****************************************************************************#
# some self-tutorial
#*****************************************************************************#
# flask.request <- https://tedboy.github.io/flask/quickstart/quickstart7.html
# https://tedboy.github.io/flask/generated/generated/flask.Flask.html
app = Flask(__name__)
print 'app = ', app.name
print 'static = ', path.dirname(app.static_folder)


# https://tedboy.github.io/flask/generated/generated/flask.Config.html
for key in sorted(app.config.iterkeys(),key=lambda s: s.lower()):
    print key,app.config[key]
# for key,val in app.config.items():
#     print key,val
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# to get url_for listen to me
# http://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
# http://flask.pocoo.org/docs/0.11/quickstart/#url-building
#https://tedboy.github.io/flask/quickstart/quickstart4.html 4. Routing
# https://tedboy.github.io/flask/quickstart/quickstart4.html#url-building
#-----------------------------------------------------------------------------#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()

# @app.route('/aboutme')
# def aboutme():
#     return render_template('aboutme.html')

@app.route('/user/<username>')
def profile(username): pass


# see https://tedboy.github.io/flask/quickstart/quickstart4.html to see wth i'm doing below
with app.test_request_context():
    print "===== url_for test ====="
    # print url_for('hello') # <- removed since i removed def hello(): above
    print url_for('profile', username='Takanori Watanabe')
    print url_for('static', filename='style.css')
    #/hello
    #/
    #/user/Takanori%20Watanabe
    #/static/style.css


#-----------------------------------------------------------------------------#
# Time example (from thinkful metaphor)
#-----------------------------------------------------------------------------#
# custom filter
# https://tedboy.github.io/flask/flask_doc.templating.html#registering-filters
# https://realpython.com/blog/python/primer-on-jinja-templating/#custom-filters
#-----------------------------------------------------------------------------#
import datetime
# Using the @app.template_filter() decorator we are registering the datetimefilter() function as a filter.
@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

# now "test.html" can use datetimefilter as a jinja filter
@app.route("/test.html")
def test():
    return render_template('test.html', 
        current_time=datetime.datetime.now())

#*****************************************************************************#
# Ok, let's now finally render my webpage
#*****************************************************************************#
#-----------------------------------------------------------------------------#
# define global variables that can be accessed from any template
#https://tedboy.github.io/flask/flask_doc.templating.html#context-processors
#-----------------------------------------------------------------------------#
# location of my pdf files
app.config['PDF_PATH']="http://takwatanabe.me/pdf/"

# @app.context_processor
# def var_url_pdf():
#     """ Allows  acces to {{ url_pdf }} anywhere in the template """
#     return dict(url_pdf="takwatanabe.me/pdf")

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
    #https://www.tutorialspoint.com/flask/flask_application.htm
    #app.run(host, port, debug, options)
    app.run(host='localhost', port= 8028)