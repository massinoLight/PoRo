from datetime import datetime
import datetime as d
import time
from flask import Flask, render_template, request






app = Flask(__name__)

@app.route('/')
def index():
    return render_template('choix.html')




@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/projets')
def contact():
    return render_template('projets.html')


@app.route('/visualisation')
def contact():
    return render_template('visualisation.html')

