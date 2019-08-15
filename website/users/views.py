from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.models import User, BlogPost
from website.users.forms import RegistrationForm, LoginForm, UpdataUserForm
from website.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

# Register User

@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Complete') #TODO: study how to use this flash as it flashes for a very short time.
        return redirect(url_for("users.login"))
    return render_template('register.html', form=form)

# Login a User

@users.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Log in Successful')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)

    return render_template('login.html', form=form)

# Logout a User
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

# Account (Update UserForm)

@users.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdataUserForm()

    if form.validate_on_submit():
        
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image =  pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    profile_image = url_for('static',filename='profile_pics/'+ current_user.profile_image)
    return render_template('account.html',profile_image=profile_image, form=form)

# User's Blog posts

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)