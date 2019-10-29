from flask import render_template, url_for, flash, redirect,request
from flask_soil.forms import LoginForm, RegistrationForm
from flask_soil.model import User, Post
from flask_soil import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3
import pickle
import pandas as pd

posts = [
    {
        'author': 'Edie Lampoh',
        'title': 'WHEN DO WE NEED MACHINE LEARNING?',
        'content': '''
                    When do we need machine learning rather than directly program our computers to
                    carry out the task at hand? Two aspects of a given problem may call for the use of
                    programs that learn and improve on the basis of their “experience”: the problem’s
                    complexity and the need for adaptivity.

                    Tasks That Are Too Complex to Program.

                    Tasks Performed by Animals/Humans:
                    There are numerous tasks that we human beings perform routinely, yet our introspection
                    concerning how we do them is not sufficiently elaborate to extract a well defined program.
                    Examples of such tasks include driving, speech recognition, and image understanding.
                    In all of these tasks, state of the art machine learning programs, programs that “learn
                    from their experience,” achieve quite satisfactory results, once exposed to sufficiently
                    many training examples.

                    Tasks beyond Human Capabilities:
                    Another wide family of tasks that benefit from machine learning techniques are related
                    to the analysis of very large and complex data sets: astronomical data, turning medical archives
                    into medical knowledge, weather prediction, analysis of genomic data, Web search engines,
                    and electronic commerce. With more and more available digitally recorded data, it becomes
                    obvious that there are treasures of meaningful information buried in data archives that are
                    way too large and too complex for humans to make sense of. Learning to detect meaningful
                    patterns in large and complex data sets is a promising domain in which the combination of
                    programs that learn with the almost unlimited memory capacity and ever increasing processing
                    speed of computers opens up new horizons.
                    ''',
        'date_posted': 'October 3, 3029'
    },
    {
        'author': 'Richie O\'Brain',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'October 4, 3029'
    }
]

pickle_in = open('crp_recommender.pkl', 'rb')
model = pickle.load(pickle_in)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/Blog")
def blog():
    return render_template('Blog.html', title="Blog", posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route('/ai')
@login_required
def ai():
    return render_template('AI.html')


@app.route('/login', methods=['GET', 'POST']) #GET obtains the info via the UI, POST takes cares of preproprcessing
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page= request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Log in unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title= 'Login', form=form)



@app.route('/registration', methods=['GET', 'POST']) #GET obtains the info via the UI, POST takes cares of preproprcessing
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name= form.first_name.data, last_name = form.last_name.data, name_of_farm=form.name_of_farm.data,username= form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title= 'Register', form=form)

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        pH = request.form['pH']
        N = request.form['N']
        P = request.form['P']
        K = request.form['K']
        OC = request.form['OC']
        Particles = request.form['Particles']
        Water_holding_content = request.form['Water_holding_content']
        Soil_type = request.form['Soil_type']

        input_variables = pd.DataFrame([[pH, N, P, K, OC, Particles, Water_holding_content, Soil_type]],
                                       columns=[pH, N, P, K, OC, Particles, Water_holding_content, Soil_type],
                                       dtype=float)
        prediction = model.predict(input_variables)[0]

        with sqlite3.connect("soil_data.db") as con:
            cur = con.cursor()
            cur.execute("INSERT into analysis (pH, N, P, K, OC, Particles, Water_holding_content, "
                        "Soil_type, prediction)VALUES(?,?,?,?,?,?,?,?,?)",
                        (pH, N, P, K, OC, Particles, Water_holding_content, Soil_type, prediction))
            con.commit()

    return render_template("result.html", prediction=prediction)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    image_file= url_fro('static', filename='images/'+ current_user.image_file)
    return render_template("account.html", title='Account')
