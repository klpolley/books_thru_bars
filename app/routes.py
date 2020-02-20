from flask import render_template, flash, redirect, url_for, request

from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

@app.route('/map', methods=['GET', 'POST'])
def map():
    return render_template('map.html', title="Map")