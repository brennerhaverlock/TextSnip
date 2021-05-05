from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from text_snip.models import Post, PostCategory, User
from text_snip.main.forms import PostForm, LoginForm, SignUpForm, Post
from text_snip import bcrypt


# Import app and db from events_app package needed to start application
from text_snip import app, db

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)
# Create your routes here.

##########################################
#           Auth                       #
##########################################

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print('You are logged in')
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    print('You are not logged in')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))


##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_posts = Post.query.all()
    print(all_posts)
    return render_template('home.html', all_posts=all_posts)

@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title = form.title.data,
            description = form.description.data,
            created_by = current_user,
        )
        db.session.add(post)
        db.session.commit()

        flash('New post was created')
        return redirect(url_for('main.post_detail', post_id=post.id))

    return render_template('new_post.html', form = form)

@main.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.address.data
        db.session.add(post)
        db.session.commit()

        flash('Post was updated')
        return redirect(url_for('main.post_detail', post_id=post.id))

    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post, form = form)


@main.route('/view_posts')
@login_required
def view_posts():
    user = current_user

    return render_template('view_posts.html', user=user)

@main.route('/add_to_profile/<post_id>', methods=['POST'])
@login_required
def add_to_profile(post_id):
    user = current_user
    post = Post.query.get(post_id)
    user.posts.append(post)
    db.session.add(user)
    db.session.commit()
    flash('Post added to profile successfully')
    return redirect(url_for('main.view_posts'))




