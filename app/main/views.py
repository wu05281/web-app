from flask import render_template, flash, redirect, url_for, request, current_app
from . import main
from ..models import User, db, Role, Permission, Post
from os import abort
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from flask_login import current_user, login_required
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination)


@main.route('/user/<username>')
def user(username):
    users = User.query.filter_by(username=username).first()
    if users is None:
        abort(404)
    posts = users.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=users, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    us = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=us)
    if form.validate_on_submit():
        us.email = form.email.data
        us.username = form.username.data
        us.confirmed = form.confirmed.data
        us.role = Role.query.get(form.role.data)
        us.name = form.name.data
        us.location = form.location.data
        us.about_me = form.about_me.data
        db.session.add(us)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=us.username))
    form.email.data = us.email
    form.username.data = us.username
    form.confirmed.data = us.confirmed
    form.role.data = us.role_id
    form.name.data = us.name
    form.location.data = us.location
    form.about_me.data = us.about_me
    return render_template('edit_profile.html', form=form, user=us)


@main.route('/post/<int:id>')
def post(id):
    posts = Post.query.get_or_404(id)
    return render_template('post.html', posts=[posts])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)
