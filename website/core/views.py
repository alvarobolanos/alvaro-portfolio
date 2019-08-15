from flask import render_template, request, Blueprint
from website.models import BlogPost

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    return render_template('index.html',blog_posts=blog_posts)

@core.route('/about')
def about():
    return render_template('about.html')

@core.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')