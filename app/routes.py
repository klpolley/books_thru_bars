from flask import render_template, flash, redirect, url_for, request, make_response, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.urls import url_parse

from app import app, mail, csrf
from app.forms import LoginForm, ContactForm
from app.get_data import get_ithaca, retrieve_facilities, retrieve_genres, retrieve_mailings
from app.login import get_user_by_name, check_password
from app.book_retrieve import get_all_titles, get_all_authors, get_all_editors, get_genres
from app.book_submit import submit, bk_logout, bk_login
from app.library import get_books, select_sent, select_have
from flask_mail import Message
from app.email import send_email

from psycopg2 import Error


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


@app.route('/whatWeDo', methods=['GET', 'POST'])
def whatWeDo():
    facilities = retrieve_facilities()
    ithaca = get_ithaca()
    library, sent = retrieve_genres()
    mailings = retrieve_mailings()

    return render_template('whatWeDo.html', title="What We Do",
                           facilities=facilities, ithaca=ithaca, library=library, sent=sent, mailings=mailings)


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    return render_template('calendar.html', title='Calendar')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('contact_us.html', form=form)
        else:
            send_email(name=form.name.data, email=form.email.data, message=form.message.data)
            return render_template('contact_us.html', success=True)
    else:
        return render_template('contact_us.html', title='Contact Us', form=form)


# @app.route('/what-we-do', methods=['GET', 'POST'])
# def data():
#     facilities = retrieve_facilities()
#     ithaca = get_ithaca()
#     library, sent = retrieve_genres()
#     mailings = retrieve_mailings()
#
#     return render_template('data.html', title="What We Do",
#                            facilities=facilities, ithaca=ithaca, library=library, sent=sent, mailings=mailings)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('library'))

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_name(form.username.data)

        if user is None or not check_password(user, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('library')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/library', methods=['GET'])
@login_required
def library():
    books = get_books(select_have())
    return render_template('library.html', books=books)


@app.route('/library/sent', methods=['GET'])
@login_required
def sent_books():
    books = get_books(select_sent())
    return render_template('sent.html', books=books)


@app.route('/library/log-in', methods=['POST', 'GET'])
@login_required
def log_book_in():
    titles = get_all_titles()
    authors = get_all_authors()
    editors = get_all_editors()
    genres = get_genres()
    return render_template('bookin.html', books=titles, auths=authors, edits=editors, gens=genres)


@app.route('/logout_book/<id>', methods=['GET','POST'])
@login_required
def logout_book(id):
    try:
        bk_logout(id)
        resp = {'feedback': 'book logged out!', 'category': 'success'}
        return make_response(jsonify(resp), 200)
    except Error as e:
        print(f'Error {e}')
        resp = {'feedback': 'error, book not logged out', 'category': 'failure'}
        return make_response(jsonify(resp), 200)


@app.route('/login_book/<id>', methods=['GET','POST'])
@login_required
def login_book(id):
    try:
        bk_login(id)
        resp = {'feedback': 'book logged back in!', 'category': 'success'}
        return make_response(jsonify(resp), 200)
    except Error as e:
        print(f'Error {e}')
        resp = {'feedback': 'error, book not logged in', 'category': 'failure'}
        return make_response(jsonify(resp), 200)


@app.route('/submitbook', methods=['POST', 'GET'])
@login_required
def submit_book():

    data = request.form.to_dict()

    title = ''
    authors = []
    editors = []
    genre = ''
    num = 1

    for entry in data:
        if entry == 'title':
            title = data[entry].upper().replace("'", "^")
        elif entry in ['author1', 'author2', 'author3']:
            authors.append(data[entry].upper().replace("'", "^"))
        elif entry in ['editor1', 'editor2', 'editor3']:
            editors.append(data[entry].upper().replace("'", "^"))
        elif entry == 'genre':
            genre = data[entry]
        elif entry == 'quantity':
            num = data[entry]
        elif entry == 'numauth':
            if data[entry] == 'VARIOUS':
                authors = ['VARIOUS']
            elif data[entry] == 'N/A':
                authors = ['N/A']
        elif entry == 'numedit':
            if data[entry] == 'VARIOUS':
                editors = ['VARIOUS']

    try:
        submit(title, authors, editors, genre, num)
        resp = {'feedback': 'book submitted!', 'category': 'success'}
        return make_response(jsonify(resp), 200)
    except Error as e:
        print(f'Error {e}')
        resp = {'feedback': 'error, book not submitted', 'category': 'failure'}
        return make_response(jsonify(resp), 200)
