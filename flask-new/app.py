# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify, render_template, request, url_for
app = Flask(__name__)

import re
from jinja2 import evalcontextfilter, Markup, escape

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


def ahref(url,text):
    """ Simple function to insert link

    Example usage::

        {% set url516 = 'http://web.eecs.umich.edu/~fessler/course/516/index.html' %}
        ({{ ahref(url516, "course link") }})
    """
    # http://stackoverflow.com/questions/3206344/passing-html-to-template-using-flask-jinja2
    # http://stackoverflow.com/questions/12672469/how-to-render-html-content-with-jinja-using-flask
    return Markup("<a href={}>{}</a>".format(url,text))


#=============================================================================#
# My custom filters
# https://realpython.com/blog/python/primer-on-jinja-templating/
# http://jinja.pocoo.org/docs/dev/api/#custom-filters
#=============================================================================#
@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter


# === register custom functions in the Flask jinja globals (to use in jinja template) === #
app.jinja_env.globals["ahref"] = ahref

#=============================================================================#
# linebreaks
# https://gist.github.com/cemk/1324543
#=============================================================================#
@app.template_filter()
@evalcontextfilter
def linebreaks(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)

@app.template_filter()
@evalcontextfilter
def linebreaksbr(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'%s' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)

#=============================================================================#
# Define views
#=============================================================================#
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

@app.route("/contact.html")
def contact():
    return render_template('contact.html',title="Contact Information")

@app.route("/plotly1.html")
def plotly1():
    return render_template('/_tests_/plotly1.html',title="Plotly-demo1")

@app.route("/plotly2.html")
def plotly2():
    return render_template('/_tests_/plotly2.html',title="Plotly-demo2")

@app.route("/plotly3.html")
def plotly3():
    return render_template('/_tests_/plotly3.html',title="Plotly-demo3")

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
    app.run(host='localhost', port= 8030)