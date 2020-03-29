from flask import render_template, flash, redirect, url_for, request

from app import app

from app.forms import ContactForm

from app.static.scripts.get_data import get_ithaca, retrieve_facilities, retrieve_genres, retrieve_mailings


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    return render_template('calendar.html', title='Calendar')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm
    return render_template('contact.html', title='Contact Us', form=form)


@app.route('/map', methods=['GET', 'POST'])
def map():
    facilities = retrieve_facilities()
    ithaca = get_ithaca()

    return render_template('map.html', title="Map", facilities = facilities, ithaca = ithaca)

@app.route('/chart', methods=['GET', 'POST'])
def charts():
    library, sent = retrieve_genres()
    return render_template('charts.html', title="Charts", library=library, sent=sent)

@app.route('/what-we-do', methods=['GET', 'POST'])
def data():
    facilities = retrieve_facilities()
    ithaca = get_ithaca()
    library, sent = retrieve_genres()
    mailings = retrieve_mailings()

    return render_template('data.html', title="What We Do",
                           facilities=facilities, ithaca=ithaca, library=library, sent=sent, mailings=mailings)