from flask import render_template, flash, redirect, url_for, request

from app import app

from app.static.scripts.get_data import get_ithaca, retrieve_facilities, retrieve_genres


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

@app.route('/map', methods=['GET', 'POST'])
def map():
    facilities = retrieve_facilities()
    ithaca = get_ithaca()

    return render_template('map.html', title="Map", facilities = facilities, ithaca = ithaca)

@app.route('/chart', methods=['GET', 'POST'])
def charts():
    library, sent = retrieve_genres()
    return render_template('charts.html', title="Charts", library=library, sent=sent)