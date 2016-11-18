# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify, render_template, request, url_for,redirect
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
@app.route("/portfolio.html")
def portfolio():
    # same as the research page
    return render_template('research.html',title="Project Portfolio")

@app.route("/research_draft.html")
def research_draft():
    return render_template('/research_draft.html',title="Research")

@app.route("/research_original.html")
def research_orig():
    return render_template('/_tests_/research_orig.html',title="Research")

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

#-----------------------------------------------------------------------------#
# individual research pages
#-----------------------------------------------------------------------------#
@app.route("/research/registration.html")
def registration():
    return render_template('registration.html',title="Spatial Confidence Regions for Registration Uncertainty Analysis")

@app.route("/research/intersite_connectome.html")
def intersite_connectome():
    return render_template('intersite_connectome.html',title="Harmonization of inter-site Structural Connectivity Data")

@app.route("/research/supervised_nmf.html")
def supervised_nmf():
    return render_template('supervised_nmf.html',title="Supervised Non-negative Matrix Factorization with Manifold Regularization")

@app.route("/research/spatial_svm.html")
def spatial_svm():
    return render_template('spatial_svm.html',title="Spatially-informed Disease Prediction with Structured Sparse Support Vector Machine")

@app.route("/research/multitask_svm.html")
def multitask_svm():
    return render_template('multitask_svm.html',title="Multisite Connectome-based Disease Classification ")

@app.route("/aws_flask_test.html")
def aws_flask_test():
    return "<strong>I took this down since I was unexpectedly getting billed by AWS</strong> (some of the service I used apparently didn't qualify for the *Free Tier* service...)"

@app.route("/data_science.html")
def data_science():
    # return redirect('research.html')
    # redirect won't work with frozen-flask (understandably...)
    return 'Please visit <a href="http://takwatanabe.me/data_science">takwatanabe.me/data_science</a>'

@app.route("/pytak.html")
def pytak():
    # return redirect('https://github.com/wtak23/pytak')
    return 'Please visit <a href="http://takwatanabe.me/data_science/pytak.html">takwatanabe.me/data_science/pytak.html</a>'

#-----------------------------------------------------------------------------#
# jsonify url
#-----------------------------------------------------------------------------#
# $.getJSON('/doworder', disp_charts);
# @app.route('/json/course_<title>')
# def json_course(title):
#     items = dict(url='test',description=title)
#     return jsonify(items=items) 

if __name__ == '__main__':
    app.run(host='localhost', port= 8032)