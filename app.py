from datetime import datetime
import datetime as d
import time
from flask import Flask, render_template, request



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('choix.html')




@app.route('/modification', methods=['GET', 'POST'])
def modification():
    if request.method == 'POST':
        req = request.form
        print(req.get("projet"))
        print(req.get("Piece"))
        print(req.get("projet"))
        print(req.get("projet"))



    return render_template('modification.html')


@app.route('/projets')
def projets():
    return render_template('projets.html')


@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html')

