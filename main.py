from flask import Flask, render_template, redirect, request
import datetime
import sqlite3
import random
from flask_restful import Api
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField
from wtforms import SelectMultipleField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from data.users import User
from data.jobs import Jobs
from data.rooms import Rooms
from data.notifications import Notifications
from data.intensity_levels import IntensityLevel
from data import db_session, users_resource, rooms_resource, jobs_resource
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/blogs.db")
dbs = db_session.create_session()
# for el in dbs.query(Jobs).all():
#    if 2 <= el.id <= 3:
#       dbs.delete(el)
dbs.commit()
job_status_transcriber = ["Начат", "Окончен", "Выполняется", "Отменён", "Выполнен", "Не выполнен", "Приостановлен"]


def search_results(query):
    conn = sqlite3.connect('db/blogs.db')
    cur = conn.cursor()
    results = cur.execute(f'SELECT * FROM jobs WHERE job LIKE "{query}%"').fetchall()
    conn.close()
    return results


class LoginForm(FlaskForm):
    email = EmailField('Почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    name = StringField('Имя:', validators=[DataRequired()])
    age = IntegerField('Возраст:')
    position = StringField('Позиция:')
    speciality = StringField('Специальность:')
    address = StringField("Адрес:")
    submit = SubmitField('Зарегистрироваться')


class JobForm(FlaskForm):
    email = SelectField('Почта тимлида:', choices=[], validators=[DataRequired()])
    name = StringField('Название работы:', validators=[DataRequired()])
    about = StringField('Описание работы:', validators=[DataRequired()])
    work_size = IntegerField('Объем работы:', validators=[DataRequired()])
    collaborators = SelectMultipleField('Соучастники:', choices=[])
    start_date = DateTimeField('Дата начала:', format='%Y-%m-%d %H:%M:%S',
                               default=datetime.datetime(year=2023, month=1, day=1, hour=1, minute=1, second=1))
    end_date = DateTimeField('Дата окончания:', format='%Y-%m-%d %H:%M:%S',
                             default=datetime.datetime(year=2023, month=1, day=1, hour=1, minute=1, second=1))
    intensity_level = SelectField('Уровень сложности:', choices=[], default=0)
    is_finished = SelectField('Статус работы:', choices=job_status_transcriber, default=0)
    submit = SubmitField('Сохранить')


class RoomForm(FlaskForm):
    title = StringField('Название комнаты:', validators=[DataRequired()])
    about = StringField('Описание комнаты:', validators=[DataRequired()])
    team_leader = SelectField('ID тимлида:', choices=[], validators=[DataRequired()])
    tasks = SelectMultipleField('Выберите задачи:', choices=[])
    collaborators = SelectMultipleField('Соучастники:', choices=[])
    submit = SubmitField('Сохранить')


class ChangeForm(FlaskForm):
    email = EmailField('Почта:', validators=[DataRequired()])
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    name = StringField('Имя:', validators=[DataRequired()])
    age = IntegerField('Возраст:')
    position = StringField('Позиция:')
    speciality = StringField('Специальность:')
    address = StringField("Адрес:")
    submit = SubmitField('Изменить')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html', current_user=current_user, title='Profile form')


@app.route('/changeprofile', methods=['GET', 'POST'])
def changeprofile():
    form = ChangeForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    form.name.data = user.name
    form.email.data = user.email
    form.surname.data = user.surname
    form.age.data = user.age
    form.position.data = user.position
    form.address.data = user.address
    form.speciality.data = user.speciality
    if form.validate_on_submit():
        if not user.check_password(form.old_password.data):
            return render_template('changeprofile.html', title='Change form',
                                   form=form,
                                   message="Неверный старый пароль!")
        if form.new_password.data != form.password_again.data:
            return render_template('changeprofile.html', title='Change form',
                                   form=form,
                                   message="Новые пароли не совпадают")
        if not db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('changeprofile.html', title='Change form',
                                   form=form,
                                   message="Вы пытаетесь стать новым пользователем")
        else:
            user.name = form.name.data
            user.email = form.email.data
            user.surname = form.surname.data
            user.age = form.age.data
            user.position = form.position.data
            user.address = form.address.data
            user.speciality = form.speciality.data
            user.set_password(form.new_password.data)
            db_sess.commit()
        return redirect(f'/login')
    return render_template('changeprofile.html', title='Register form', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/alljobs/{user.current_room}")
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
        personal_room = Rooms()
        tl = db_sess.query(User).filter(User.email == form.email.data).first()
        personal_room.title = f"Personal room for {tl.email}"
        personal_room.about = "personal room"
        personal_room.team_leader = tl.id
        note = Notifications()
        note.text = f'Добро пожаловать! Вы можете редактировать и удалять только те задачи, в которых являетесь Владельцем!'
        note.users = str(tl.email)
        note.mister = True
        db_sess.add(personal_room)
        db_sess.add(note)
        db_sess.commit()
        tl.current_room = db_sess.query(Rooms).filter(
            db_sess.query(User).filter(User.email == form.email.data).first().id == Rooms.team_leader).first().id
        db_sess.add(user)
        db_sess.commit()
        return redirect(f'/login')
    return render_template('register.html', title='Register form', form=form)


@app.route('/alljobs/<int:id>')
@login_required
def all_jobs(id):
    db_sess = db_session.create_session()
    data = []
    ct = 0
    current_room = db_sess.query(Rooms).filter(Rooms.id == id).first()
    if current_room is not None:
        if current_room.collaborators:
            if current_user.id in [current_room.team_leader] + current_room.collaborators.split(","):
                if current_room.tasks is not None:
                    x = current_room.tasks.split(", ")
                else:
                    x = None
                if x and not (len(x) == 1 and not x[0]):
                    available_tasks = tuple(map(int, x))
                else:
                    available_tasks = ()
                for el in db_sess.query(Jobs):
                    if el.id in available_tasks:
                        team_leader = f"{el.user.name} {el.user.surname}"
                        cover = str(random.randint(1, 21)) + ".png"
                        data.append((el.job, team_leader, el.id, cover))
                ans = []
                i = 0
                while i < len(data):
                    curr = []
                    for j in range(4):
                        if i >= len(data):
                            break
                        curr.append(data[i])
                        i += 1
                    ans.append(curr)
                rooms = []
                for el in db_sess.query(Rooms).filter(
                        (Rooms.team_leader.like(current_user.id) | Rooms.collaborators.like(
                            f'%{current_user.id}%'))).all():
                    rooms.append((f"{el.title} |{el.team_leader}", el.id))
                notes1 = []
                for i in dbs.query(Notifications).all():
                    a = i.users.split(',')
                    if current_user.email in a and i.mister == True:
                        notes1.append((i.text))
                        i.mister = False
                        dbs.delete(i)

                print(notes1)
                dbs.commit()
                return render_template('alljobs.html', label="Поиск задач по названию", ans=ans, rooms=rooms,
                                       crId=current_room.id, crU=current_user.email, notes1=notes1)
            else:
                return render_template('not_allowed.html', room_id=current_user.current_room, f_pr=True)
        else:
            if current_user.id in [current_room.team_leader]:
                if current_room.tasks is not None:
                    x = current_room.tasks.split(", ")
                else:
                    x = None
                if x and not (len(x) == 1 and not x[0]):
                    available_tasks = tuple(map(int, x))
                else:
                    available_tasks = ()
                for el in db_sess.query(Jobs):
                    if el.id in available_tasks:
                        team_leader = f"{el.user.name} {el.user.surname}"
                        cover = str(random.randint(1, 20)) + ".png"
                        data.append((el.job, team_leader, el.id, cover))
                ans = []
                i = 0
                while i < len(data):
                    curr = []
                    for j in range(4):
                        if i >= len(data):
                            break
                        curr.append(data[i])
                        i += 1
                    ans.append(curr)
                rooms = []
                for el in db_sess.query(Rooms).filter(
                        (Rooms.team_leader.like(current_user.id) | Rooms.collaborators.like(
                            f'%{current_user.id}%'))).all():
                    rooms.append((f"{el.title} |{el.team_leader}", el.id))
                notes1 = []
                for i in dbs.query(Notifications).all():
                    a = ""
                    a = i.users.split(',')
                    if current_user.email in a and i.mister == True:
                        notes1.append((i.text))
                        i.mister = False
                print(notes1)
                return render_template('alljobs.html', label="Поиск задач по названию", ans=ans, rooms=rooms,
                                       crId=current_room.id, crU=current_user.email, notes1=notes1)
            else:
                return render_template('not_allowed.html', room_id=current_user.current_room, f_pr=True)
    else:
        return render_template('not_allowed.html', room_id=current_user.current_room, f_pr=True)


@app.route('/search/<int:id>', methods=['POST'])
def search(id):
    dbs = db_session.create_session()
    current_room = dbs.query(Rooms).filter(Rooms.id == id).first()
    if current_room is not None:
        if current_room.collaborators:
            if current_user.id in [current_room.team_leader] + current_room.collaborators.split(","):
                query = request.form['query']
                jobs = []
                if current_room.tasks is not None:
                    x = current_room.tasks.split(", ")
                else:
                    x = None
                if x and not (len(x) == 1 and not x[0]):
                    available_tasks = tuple(map(int, x))
                else:
                    available_tasks = ()
                for el in search_results(query.lower()):
                    if el[0] in available_tasks:
                        user = dbs.query(User).filter(User.id == el[1]).first()
                        team_leader = f"{user.name} {user.surname}"
                        cover = str(random.randint(1, 20)) + ".png"
                        jobs.append((el[2], team_leader, el[0], cover))
                print(cover)
                ans = []
                i = 0
                while i < len(jobs):
                    curr = []
                    for j in range(4):
                        if i >= len(jobs):
                            break
                        curr.append(jobs[i])
                        i += 1
                    ans.append(curr)
                rooms = []
                for el in dbs.query(Rooms).filter(
                        (Rooms.team_leader.like(current_user.id) | Rooms.collaborators.like(
                            f'%{current_user.id}%'))).all():
                    rooms.append((f"{el.title} |{el.team_leader}", el.id))
                return render_template('alljobs.html', label=query, ans=ans, rooms=rooms, crId=current_room.id,
                                       crU=current_user.email)
            else:
                return render_template('not_allowed.html', room_id=id, f_pr=True)
        else:
            if current_user.id in [current_room.team_leader]:
                query = request.form['query']
                jobs = []
                if current_room.tasks is not None:
                    x = current_room.tasks.split(", ")
                else:
                    x = None
                if x and not (len(x) == 1 and not x[0]):
                    available_tasks = tuple(map(int, x))
                else:
                    available_tasks = ()
                for el in search_results(query.lower()):
                    if el[0] in available_tasks:
                        user = dbs.query(User).filter(User.id == el[1]).first()
                        team_leader = f"{user.name} {user.surname}"
                        cover = str(random.randint(1, 20)) + ".png"
                        jobs.append((el[2], team_leader, el[0], cover))
                ans = []
                i = 0
                while i < len(jobs):
                    curr = []
                    for j in range(4):
                        if i >= len(jobs):
                            break
                        curr.append(jobs[i])
                        i += 1
                    ans.append(curr)
                rooms = []
                for el in dbs.query(Rooms).filter(
                        (Rooms.team_leader.like(current_user.id) | Rooms.collaborators.like(
                            f'%{current_user.id}%'))).all():
                    rooms.append((f"{el.title} |{el.team_leader}", el.id))
                return render_template('alljobs.html', label=query, ans=ans, rooms=rooms, crId=current_room.id,
                                       crU=current_user.email)
            else:
                return render_template('not_allowed.html', room_id=current_user.current_room, f_pr=True)
    else:
        return render_template('not_allowed.html', room_id=current_user.current_room, f_pr=True)


@app.route('/job_description/<int:id>/<int:room_id>')
@login_required
def job_descr(id, room_id):
    dbs = db_session.create_session()
    task = dbs.query(Jobs).filter(Jobs.id == id).first()
    current_room = dbs.query(Rooms).filter(Rooms.id == room_id).first()
    if current_user.id in [task.team_leader] + task.collaborators.split(","):
        el = dbs.query(Jobs).filter(Jobs.id == id).first()
        title = el.job
        time = el.end_date - el.start_date
        team_leader = f"{el.user.name} {el.user.surname}"
        collaborators = el.collaborators
        isf = job_status_transcriber[int(el.is_finished)]
        lvl = el.intensity_level[-1].level
        job = [title, team_leader, time, collaborators, isf, el.user.id, el.id, lvl, el.description, el.end_date]
        return render_template("job_description.html", crId=current_room.id, job=job, room_id=room_id)
    else:
        return render_template('not_allowed.html', room_id=current_user.current_room, f_pr=True)


@app.route('/addjob/<int:id>', methods=['GET', 'POST'])
@login_required
def addjob(id):
    form = JobForm()
    dbs = db_session.create_session()
    room = dbs.query(Rooms).filter(Rooms.id == id).first()
    if room.collaborators is not None:
        if current_user.id in [room.team_leader] + room.collaborators.split(","):
            res = dbs.query(User).all()
            dbs.commit()
            form.email.choices.append(dbs.query(User).filter(User.id == current_user.id).first().email)
            for el in res:
                form.collaborators.choices.append(str(el.email))
            for i in range(11):
                form.intensity_level.choices.append(i)
            if form.validate_on_submit():
                print(room.collaborators.split(", "))
                print(current_user.id)
                room1 = room.collaborators.split(",")

                if str(current_user.id) in room1:
                    ind = True
                else:
                    ind = False

                db_sess = db_session.create_session()

                job = Jobs()
                job.job = form.name.data
                job.description = form.about.data
                job.team_leader = current_user.id
                job.collaborators = ','.join(form.collaborators.data)
                job.is_finished = job_status_transcriber.index(form.is_finished.data)
                job.start_date = form.start_date.data
                job.end_date = form.end_date.data
                job.work_size = form.work_size.data
                intensity_level = IntensityLevel()
                intensity_level.level = form.intensity_level.data
                job.intensity_level = []
                job.intensity_level.append(intensity_level)
                db_sess.add(job)
                current_room = db_sess.query(Rooms).filter(Rooms.id == id).first()
                note = Notifications()
                note.text = f'вас добавили в новую комнату{current_room.title}'
                note.users = room1
                note.mister = True
                print(current_room.tasks.split(", "))
                available_tasks = list(map(int, current_room.tasks.split(", ")))
                if available_tasks is not None:
                    available_tasks.append(job.id)
                    current_room.tasks = ', '.join(map(lambda x: str(x), available_tasks))
                else:
                    current_room.tasks = str(job.id) + ', '

                db_sess.add(current_room)
                db_sess.commit()
                return redirect(f"/alljobs/{id}")
            return render_template('addjob.html', form=form, room_id=id)
        else:
            return render_template('not_allowed.html', room_id=id, f_pr=False)
    else:
        if current_user.id in [room.team_leader]:
            res = dbs.query(User).all()
            dbs.commit()
            form.email.choices.append(dbs.query(User).filter(User.id == current_user.id).first().email)
            for el in res:
                form.collaborators.choices.append(str(el.email))
            for i in range(11):
                form.intensity_level.choices.append(i)
            if form.validate_on_submit():
                db_sess = db_session.create_session()
                job = Jobs()
                job.job = form.name.data
                job.description = form.about.data
                job.team_leader = current_user.id
                job.collaborators = ','.join(form.collaborators.data)
                job.is_finished = job_status_transcriber.index(form.is_finished.data)
                job.start_date = form.start_date.data
                job.end_date = form.end_date.data
                job.work_size = form.work_size.data
                intensity_level = IntensityLevel()
                intensity_level.level = form.intensity_level.data
                job.intensity_level = []
                job.intensity_level.append(intensity_level)
                db_sess.add(job)
                current_room = db_sess.query(Rooms).filter(Rooms.id == id).first()
                if not current_room.tasks:
                    available_tasks = []
                else:
                    available_tasks = list(map(int, current_room.tasks.split(", ")))
                if available_tasks is not None:
                    available_tasks.append(job.id)
                    current_room.tasks = ', '.join(map(lambda x: str(x), available_tasks))
                else:
                    current_room.tasks = str(job.id) + ', '
                db_sess.add(current_room)
                db_sess.commit()
                return redirect(f"/alljobs/{id}")
            return render_template('addjob.html', form=form, room_id=id)
        else:
            return render_template('not_allowed.html', room_id=id, f_pr=False)


@app.route('/addjob/<int:room_id>/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(room_id, job_id):
    form = JobForm()
    dbs = db_session.create_session()
    task = dbs.query(Jobs).filter(Jobs.id == job_id).first()
    if current_user.id in [task.team_leader] + task.collaborators.split(","):
        if current_user.id == task.team_leader:
            res = dbs.query(User).all()
            form.email.choices.append(dbs.query(User).filter(User.id == current_user.id).first().email)
            for el in res:
                form.collaborators.choices.append(str(el.email))
            for i in range(11):
                form.intensity_level.choices.append(i)
            if request.method == "GET":
                dbs = db_session.create_session()
                job = dbs.query(Jobs).filter((Jobs.id == job_id), (Jobs.user == current_user)).first()
                print(1)
                if job:
                    form.name.data = job.job
                    form.work_size.data = job.work_size
                    form.about.data = job.description
                    form.collaborators.data = job.collaborators
                    form.start_date.data = job.start_date
                    form.end_date.data = job.end_date
                    form.email.data = job.user.email
                    form.is_finished.data = job_status_transcriber[int(job.is_finished)]
                    if job.intensity_level:
                        form.intensity_level.data = job.intensity_level[-1].level
                    else:
                        form.intensity_level.data = 0
                else:
                    pass
            if form.validate_on_submit():
                dbs = db_session.create_session()
                job = dbs.query(Jobs).filter((Jobs.id == job_id), (Jobs.user == current_user)).first()
                user = dbs.query(User).filter(User.email == form.email.data).first()
                if not user:
                    return render_template('addjob.html', message='Неверно указана почта', form=form)
                if job:
                    job.job = form.name.data
                    job.team_leader = current_user.id
                    job.description = form.about.data
                    job.collaborators = ','.join(form.collaborators.data)
                    job.is_finished = job_status_transcriber.index(form.is_finished.data)
                    job.start_date = form.start_date.data
                    job.end_date = form.end_date.data
                    job.work_size = form.work_size.data
                    hl = IntensityLevel()
                    hl.level = form.intensity_level.data
                    job.intensity_level = []
                    job.intensity_level.append(hl)
                    dbs.commit()
                    return redirect(f'/alljobs/{room_id}')
                else:
                    pass
            return render_template('addjob.html', form=form, room_id=room_id)
        return render_template('not_allowed.html', room_id=room_id, f_pr=False)
    return render_template('not_allowed.html', room_id=room_id, f_pr=False)


@app.route('/job_delete/<int:room_id>/<int:job_id>', methods=['GET', 'POST'])
@login_required
def delete_job(room_id, job_id):
    dbs = db_session.create_session()
    jobs = dbs.query(Jobs).filter((Jobs.id == job_id), (Jobs.user == current_user)).first()
    rooms = dbs.query(Rooms).filter((Rooms.id == room_id)).first()
    if rooms and current_user.id == rooms.team_leader:
        if rooms.tasks:
            tasks = rooms.tasks.split(', ')
            print(tasks, job_id)
            tasks.remove(str(job_id))
            rooms.tasks = ', '.join(tasks)
        dbs.commit()
    if jobs and current_user.id == jobs.team_leader:
        dbs.delete(jobs)
        dbs.commit()
    else:
        pass
    return redirect(f'/alljobs/{room_id}')


@app.route('/allrooms')
@login_required
def all_rooms():
    dbs = db_session.create_session()
    if current_user.is_authenticated:
        res = dbs.query(Rooms).filter(
            (Rooms.team_leader.like(current_user.id) | Rooms.collaborators.like(f'%{current_user.id}%')))
        rooms = []
        for el in res:
            title = el.title
            team_leader = el.team_leader
            x = []
            collaborators = el.collaborators
            if collaborators is not None:
                for elem in collaborators:
                    elem = dbs.query(User).filter(User.id == elem).first()
                    if elem is not None:
                        x.append(elem.email)
            collaborators = ', '.join(x)
            about = el.about
            tasks = el.tasks
            x = []
            if tasks is not None:
                for elem in tasks:
                    elem = dbs.query(Jobs).filter(Jobs.id == elem).first()
                    if elem is not None:
                        x.append(elem.job)
            tasks = ', '.join(x)
            rooms.append([title, about, team_leader, tasks, collaborators, el.id])
        return render_template('allrooms.html', rooms=rooms)
    else:
        pass


@app.route('/addroom', methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()
    dbs = db_session.create_session()
    users = dbs.query(User).all()
    dbs.commit()
    tasks = dbs.query(Jobs).all()
    x = dbs.query(User).filter(User.id == current_user.id).first()
    form.team_leader.choices.append(x.email)
    for el in users:
        form.collaborators.choices.append(str(el.email))
    for el in tasks:
        form.tasks.choices.append(str(el.job))
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        room = Rooms()
        room.title = form.title.data
        room.about = form.about.data
        room.team_leader = current_user.id
        x = []
        for el in form.collaborators.data:
            el = dbs.query(User).filter((User.email == el)).first().id
            x.append(str(el))
        room.collaborators = ', '.join(x)
        x = []
        for el in form.tasks.data:
            el = dbs.query(Jobs).filter(Jobs.job == el).first().id
            x.append(str(el))
        room.tasks = ', '.join(x)
        db_sess.add(room)
        db_sess.commit()
        return redirect(f"/alljobs/{room.id}")
    return render_template('addroom.html', form=form)


@app.route('/addroom/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_room(id):
    form = RoomForm()
    dbs = db_session.create_session()
    users = dbs.query(User).all()
    room = dbs.query(Rooms).filter((Rooms.id == id), (Rooms.team_leader == current_user.id)).first()
    if room is not None and current_user.id == room.team_leader:
        tasks = dbs.query(Jobs).all()
        form.team_leader.choices.append(dbs.query(User).filter(User.id == current_user.id).first().email)
        for el in users:
            form.collaborators.choices.append(str(el.email))
        for el in tasks:
            form.tasks.choices.append(str(el.job))
        if request.method == "GET":
            dbs = db_session.create_session()
            room = dbs.query(Rooms).filter((Rooms.id == id), (Rooms.team_leader == current_user.id)).first()
            if room:
                form.title.data = room.title
                form.about.data = room.about
                room.team_leader = current_user.id
                if form.collaborators.data is not None:
                    form.collaborators.data = room.collaborators
                if form.tasks.data is not None:
                    form.tasks.data = room.tasks
            else:
                pass
        if form.validate_on_submit():
            dbs = db_session.create_session()
            room = dbs.query(Rooms).filter((Rooms.id == id), (Rooms.team_leader == current_user.id)).first()
            user = dbs.query(User).filter(User.email == form.team_leader.data).first()
            if not user:
                return render_template('addroom.html', message='Неверно указан team_leader', form=form)
            if room:
                room.title = form.title.data
                room.about = form.about.data
                room.team_leader = current_user.id
                x = []
                for el in form.collaborators.data:
                    el = dbs.query(User).filter((User.email == el)).first().id
                    x.append(str(el))
                room.collaborators = ', '.join(x)
                x = []
                for el in form.tasks.data:
                    el = dbs.query(Jobs).filter(Jobs.job == el).first().id
                    x.append(str(el))
                room.tasks = ', '.join(x)
                dbs.commit()
                return redirect('/allrooms')
            else:
                pass
        return render_template('addroom.html', form=form)
    return render_template('not_allowed.html', room_id=current_user.current_room, f_pr=True)


@app.route('/room_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_room(id):
    dbs = db_session.create_session()
    room = dbs.query(Rooms).filter((Rooms.id == id), (Rooms.team_leader == current_user.id)).first()
    if room and room.team_leader == current_user.id:
        dbs.delete(room)
        dbs.commit()
    else:
        pass
    return redirect('/allrooms')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")

    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    # для одного объекта
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<users_id>')
    # для списка объектов
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    # для одного объекта
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<jobs_id>')
    # для списка объектов
    api.add_resource(rooms_resource.RoomsListResource, '/api/v2/rooms')
    # для одного объекта
    api.add_resource(rooms_resource.RoomsResource, '/api/v2/rooms/<rooms_id>')

    app.run(port=8080, host='127.0.0.1')
