from flask import render_template, send_file
from app import app
from app.prob import plot_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chamber/', defaults={'name': None})
@app.route('/chamber/<name>')
def chamber(name):
    probs = [{
        'temp': 72,
        "humidity": 68
    }, {
        'temp': 55,
        "humidity": 70
    }, {
        'temp': 50,
        "humidity": 60
    }]
    return render_template('chamber.html', name=name, probs=probs)


@app.route('/plot')
def plot():
    bytes_obj = plot_data()
    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')