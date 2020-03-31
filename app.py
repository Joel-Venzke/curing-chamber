from flask import Flask, render_template, send_file
from HumidityProb import plot_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chamber/<name>')
def chamber(name):
    return render_template('chamber.html', name=name)

@app.route('/plot')
def plot():
    bytes_obj = plot_data()

    return send_file(bytes_obj, attachment_filename='plot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

