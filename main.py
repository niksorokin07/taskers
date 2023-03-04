from flask import Flask, render_template, redirect, request
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField
from wtforms import SelectMultipleField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.db_session import SqlAlchemyBase
from data.users import User
from data.jobs import Jobs
from data.news import News
from data.hazard_levels import HazardLevel
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/blogs.db")
dbs = db_session.create_session()
dbs.commit()


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age')
    position = StringField('Position')
    speciality = StringField('Speciality')
    address = StringField("Address")
    submit = SubmitField('Register')


class JobForm(FlaskForm):
    email = SelectField('Team leader email', choices=[], validators=[DataRequired()])
    name = StringField('Title of job', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = SelectMultipleField('Collaborators', choices=[])
    start_date = DateTimeField('Start date', format='%Y-%m-%d %H:%M:%S',
                               default=datetime.datetime(year=2023, month=1, day=1, hour=1, minute=1, second=1))
    end_date = DateTimeField('End date', format='%Y-%m-%d %H:%M:%S',
                             default=datetime.datetime(year=2023, month=1, day=1, hour=1, minute=1, second=1))
    hazard_level = IntegerField('Hazard level', default=0)
    is_finished = BooleanField('Is finished?')
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template('handle_authentification.html', news=news)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        else:
            return render_template('login.html', message="Неправильный логин или пароль!", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            address=form.address.data,
            speciality=form.speciality.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Register form', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobForm()
    dbs = db_session.create_session()
    res = dbs.query(User).all()
    for el in res:
        form.email.choices.append(el.email)
        form.collaborators.choices.append(str(el.id))
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.name.data
        job.team_leader = current_user.id
        job.collaborators = ','.join(form.collaborators.data)
        job.is_finished = form.is_finished.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.work_size = form.work_size.data
        hazard = HazardLevel()
        hazard.level = form.hazard_level.data
        job.hazard_level.append(hazard)
        db_sess.add(job)
        db_sess.commit()
        return redirect("/alljobs")
    return render_template('addjob.html', form=form)


@app.route('/alljobs')
def all_jobs():
    dbs = db_session.create_session()
    res = dbs.query(Jobs).all()
    jobs = []
    for el in res:
        title = el.job
        time = el.end_date - el.start_date
        team_leader = f"{el.user.name} {el.user.surname}"
        collaborators = el.collaborators
        isf = el.is_finished
        lvl = el.hazard_level[-1].level
        jobs.append([title, team_leader, time, collaborators, isf, el.user.id, el.id, lvl])
    return render_template('alljobs.html', jobs=jobs)


@app.route('/addjob/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    dbs = db_session.create_session()
    res = dbs.query(User).all()
    for el in res:
        form.email.choices.append(el.email)
        form.collaborators.choices.append(str(el.id))
    if request.method == "GET":
        dbs = db_session.create_session()
        job = dbs.query(Jobs).filter((Jobs.id == id), (Jobs.user == current_user)).first()
        if job:
            form.name.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.end_date.data = job.end_date
            form.email.data = job.user.email
            form.is_finished.data = job.is_finished
            if job.hazard_level:
                form.hazard_level.data = job.hazard_level[-1].level
            else:
                form.hazard_level.data = 0
        else:
            pass
    if form.validate_on_submit():
        dbs = db_session.create_session()
        job = dbs.query(Jobs).filter((Jobs.id == id), (Jobs.user == current_user)).first()
        user = dbs.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template('addjob.html', message='Неверно указана почта', form=form)
        if job:
            job.job = form.name.data
            job.team_leader = current_user.id
            job.collaborators = ','.join(form.collaborators.data)
            job.is_finished = form.is_finished.data
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.work_size = form.work_size.data
            hl = HazardLevel()
            hl.level = form.hazard_level.data
            job.hazard_level.append(hl)
            dbs.commit()
            return redirect('/alljobs')
        else:
            pass
    return render_template('addjob.html', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    dbs = db_session.create_session()
    jobs = dbs.query(Jobs).filter((Jobs.id == id), (Jobs.user == current_user)).first()
    if jobs:
        dbs.delete(jobs)
        dbs.commit()
    else:
        pass
    return redirect('/alljobs')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')