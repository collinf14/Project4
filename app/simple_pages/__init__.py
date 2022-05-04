from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_pages = Blueprint('simple_pages', __name__, template_folder='templates')

@simple_pages.route('/', defaults={'page': 'index'})
@simple_pages.route('/<page>')
def index():
    try:
        return render_template('%.html' % page)
    except TemplateNotFound:
        abort(404)


@simple_pages.route('/about')
def about():
    try:
        return render_template('404.html')
    except TemplateNotFound:
        abort(404)

#@simple_pages.route('/welcome')
#def welcome():
 #   try:
  #      return render_template('welcome.html')
   # except TemplateNotFound:
    #    abort(404)
