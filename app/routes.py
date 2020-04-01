from flask import render_template, flash, redirect
from app import app
from app.prob import plot_data
from app.prob import Prob
from app.forms import LoginForm
from bokeh.resources import INLINE


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/chamber/', defaults={'name': None})
@app.route('/chamber/<name>')
def chamber(name):
    ambientProb = Prob(4)
    chamberProb = Prob(17)
    prob = {
        'chamber_temp': chamberProb.temp,
        "chamber_humidity": chamberProb.humid,
        'ambient_temp': ambientProb.temp,
        "ambient_humidity": ambientProb.humid
    }
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    temp_script, temp_div = plot_data()
    return render_template(
        'chamber.html',
        name=name,
        prob=prob,
        plot_script=temp_script,
        plot_div=temp_div,
        js_resources=js_resources,
        css_resources=css_resources,
    )


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login Requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', form=form)
