from flask import render_template, flash, redirect
from app import app
from app.prob import plot_chamber, plot_ambient
from app.forms import LoginForm
from bokeh.resources import INLINE


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/chamber/', defaults={'name': None})
@app.route('/chamber/<name>')
def chamber(name):
    prob = {
        'chamber_temp': 65.2,
        "chamber_humidity": 68.3,
        'ambient_temp': 72,
        "ambient_humidity": 30
    }
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    chamber_temp_script, chamber_temp_div = plot_chamber()
    ambient_temp_script, ambient_temp_div = plot_ambient()
    return render_template(
        'chamber.html',
        name=name,
        prob=prob,
        plot_chamber_script=chamber_temp_script,
        plot_chamber_div=chamber_temp_div,
        plot_ambient_script=ambient_temp_script,
        plot_ambient_div=ambient_temp_div,
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
