from flask import render_template, send_file, flash, redirect
from app import app
from app.prob import plot_data
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
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


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    print('hit')
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("hit in")
        flash('Login Requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', form=form)
