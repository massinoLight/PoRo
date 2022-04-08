from datetime import datetime
import datetime as d
import time
from flask import Flask, render_template, request



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('choix.html')




@app.route('/modification')
def modification():
    return render_template('modification.html')


@app.route('/projets')
def projets():
    return render_template('projets.html')


@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html')

