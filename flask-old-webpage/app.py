from flask import Flask
from flask import jsonify, render_template, request, url_for, g

from os import path
# flask.request <- https://tedboy.github.io/flask/quickstart/quickstart7.html
# https://tedboy.github.io/flask/generated/generated/flask.Flask.html
app = Flask(__name__)
print 'app = ', app.name
print 'static = ', path.dirname(app.static_folder)

#=============================================================================#
# config values in flask app
# https://tedboy.github.io/flask/flask_doc.config.html
#=============================================================================#
app.config['DEBUG'] = True

# https://tedboy.github.io/flask/generated/generated/flask.Config.html
for key in sorted(app.config.iterkeys(),key=lambda s: s.lower()):
    print key,app.config[key]
# for key,val in app.config.items():
#     print key,val
#-----------------------------------------------------------------------------#

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

# @app.route('/hello.html')
# def hello():
#     return 'Hello, World'

#https://tedboy.github.io/flask/quickstart/quickstart4.html
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

# @app.route('/user/<username>')
# def profile(username):
#     return 'Username = {}'.format(username)

# see https://tedboy.github.io/flask/quickstart/quickstart4.html to see wth i'm doing below
with app.test_request_context():
    print url_for('hello')
    print url_for('index')
    print url_for('profile', username='Takanori Watanabe')
    print url_for('static', filename='style.css')
    #/hello
    #/
    #/user/Takanori%20Watanabe
    #/static/style.css


#=============================================================================#
# Time example (from thinkful metaphor)
# https://realpython.com/blog/python/primer-on-jinja-templating/#custom-filters
#=============================================================================#
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


#=============================================================================#
# back to my stuffs..
#=============================================================================#
options = dict(google_analytics = False)
@app.route("/courses.html")
def courses():
    return render_template('courses.html', **options)

@app.route("/resources.html")
def resources():
    return render_template('resources.html', **options)

@app.route("/research.html")
def research():
    return render_template('research.html', **options)

if __name__ == '__main__':
    #https://www.tutorialspoint.com/flask/flask_application.htm
    #app.run(host, port, debug, options)
    app.run(host='localhost', port= 8028)