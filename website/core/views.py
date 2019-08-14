from flask import render_template, request, Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def index():
    # Will include the blog posts list in the future
    return render_template('index.html')

@core.route('/about')
def about():
    return render_template('about.html')

@core.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')