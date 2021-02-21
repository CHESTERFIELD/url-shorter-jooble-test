import json

import validators
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, login_user, logout_user

from models import User
from repositories.url import UrlRepository

short = Blueprint('short', __name__)


@short.route('/')
def index():
    return render_template('index.html')


@short.route('/add_link', methods=['POST'])
def add_link():
    full_url = request.form['original_url']

    # validate received url
    if not validators.url(full_url):
        raise ValueError('{} is not a valid url'.format(full_url))

    life_period = int(request.form['life_period'])

    # validate received url
    if life_period not in range(1, 365):
        raise ValueError('{} is not a life period'.format(str(life_period)))

    # if this url already exists render it
    exist_url = UrlRepository.get_exist_url(full_url)
    if exist_url:
        return render_template('link_added.html', new_link=exist_url.url_hash, original_url=exist_url.full_url)

    result = UrlRepository.create(full_url=full_url, life_period=int(life_period))

    return render_template('link_added.html', new_link=result.url_hash, original_url=result.full_url)


@short.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@short.route('/<short_url>')
def redirect_to_url(short_url):
    url = UrlRepository.get(url_hash=short_url)
    return redirect(url.full_url), 301


@short.route('/delete', methods=['POST'])
@login_required
def delete_url():
    delete_url_id = request.form['delete_url_id']
    UrlRepository.delete(id=delete_url_id)

    return redirect(url_for('short.urls'))


@short.route('/urls')
@login_required
def urls():
    ROWS_PER_PAGE = 3

    # Get the data from the database
    page = request.args.get('page', 1, type=int)
    urls = UrlRepository.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('url/list.html', urls=urls)


@short.route('/urls/<id>')
@login_required
def url_item(id):
    url = UrlRepository.get_by_id(id=id)
    return render_template('url/item.html', url=url)


@short.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email, password=password).first()

    if user:
        login_user(user)
        return redirect(url_for('short.index'))
    else:
        # TODO GET ERROR
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


@short.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('short.index'))
