import validators
from flask import Blueprint, render_template, request, redirect
from repositories.url import UrlRepository

short = Blueprint('short', __name__)


@short.route('/')
def index():
    return render_template('index.html')


@short.route('/add_link', methods=['POST'])
def add_link():
    full_url = request.form['original_url']

    # validate received url
    if validators.url(full_url):
        pass
    else:
        raise ValueError('{} is not a valid url'.format(full_url))

    life_period = request.form['life_period']

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
