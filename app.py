from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from flask import Flask, redirect, render_template, request, abort

from data import db_session
from data.category import Category
from data.jobs import JobsForm, Jobs
from data.login_form import LoginForm
from data.news import News, NewsForm
from data.register_form import RegisterForm
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login_blogs.html",
                               message="Wrong email or password", form=form)
    return render_template("login_blogs.html", title="Login", form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True) \
        if not current_user.is_authenticated else \
        db_sess.query(News).filter((News.user == current_user)
                                   | (News.is_private != True))
    return render_template("index_blogs.html", news=news)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register_blogs.html", title="Register",
                                   form=form, message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register_blogs.html", title="Register",
                                   form=form, message="User already exists")
        user = User(name=form.name.data, email=form.email.data,
                    about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register_blogs.html", title="Register", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/news", methods=["GET", "POST"])
@login_required
def add_news():
    form = NewsForm()
    db_sess = db_session.create_session()
    form.categories.choices = [(c.id, c.name) for c in db_sess.query(Category).all()]
    if form.validate_on_submit():
        news = News(
            title=form.title.data,
            content=form.content.data,
            is_private=form.is_private.data,
            user_id=current_user.id
        )
        news.categories = db_sess.query(Category).filter(Category.id.in_(form.categories.data)).all()
        db_sess.add(news)
        db_sess.commit()
        return redirect("/")
    return render_template("news.html", title="Add News", form=form)


@app.route("/news/<int:id>", methods=["GET", "POST"])
@login_required
def edit_news(id):
    form = NewsForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if not news:
        abort(404)
    form.categories.choices = [(c.id, c.name) for c in db_sess.query(Category).all()]
    if request.method == "GET":
        form.title.data = news.title
        form.content.data = news.content
        form.is_private.data = news.is_private
        form.categories.data = [c.id for c in news.categories]
    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        news.categories = db_sess.query(Category).filter(Category.id.in_(form.categories.data)).all()
        db_sess.commit()
        return redirect("/")
    return render_template("news.html", title="Edit News", form=form)


@app.route("/news_delete/<int:id>", methods=["GET", "POST"])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/")


@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    db_sess = db_session.create_session()
    if request.method == "POST":
        category_name = request.form.get("category_name")
        if category_name and not db_sess.query(Category).filter(
                Category.name == category_name).first():
            category = Category(name=category_name)
            db_sess.add(category)
            db_sess.commit()
    categories = db_sess.query(Category).all()
    return render_template("categories.html", categories=categories)


@app.route("/jobs", methods=["GET", "POST"])
@login_required
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.team_leader == current_user.id)
    return render_template("jobs.html", jobs=jobs)


@app.route("/jobs/add", methods=["GET", "POST"])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            team_leader=current_user.id
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/jobs")
    return render_template("job_form.html", title="Add Task", form=form)


@app.route("/jobs/<int:id>", methods=["GET", "POST"])
@login_required
def edit_job(id):
    form = JobsForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
    if not job:
        abort(404)
    if request.method == "GET":
        form.job.data = job.job
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
    if form.validate_on_submit():
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect("/jobs")
    return render_template("job_form.html", title="Edit Task", form=form)


@app.route("/jobs_delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader
                                     == current_user.id).first()
    if not job:
        abort(404)
    db_sess.delete(job)
    db_sess.commit()
    return redirect("/jobs")


def main():
    db_name = input("Enter database path (e.g., db/blogs.db): ")
    db_session.global_init(db_name)
    app.run()


if __name__ == "__main__":
    main()
