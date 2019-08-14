from flask import render_template, url_for, flash, request, redirect,Blueprint
from flask_login import current_user, login_required
from website import db 
from website.models import BlogPost
from website.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_post', __name__)

