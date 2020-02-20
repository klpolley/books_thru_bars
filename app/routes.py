from flask import render_template, flash, redirect, url_for, request

from app import app

from app.static.scripts.get_data import retrieve_facilities


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

@app.route('/map', methods=['GET', 'POST'])
def map():
    facilities = retrieve_facilities()

    return render_template('map.html', title="Map", facilities = facilities)