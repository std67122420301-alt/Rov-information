from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Hero

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

import os


app = Flask(__name__)

app.secret_key = "123456"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():

    if Hero.query.count() == 0:

        heroes = [

Hero(name="Nakroth",role="Assassin",image="https://static.wikia.nocookie.net/arenaofvalor/images/e/e0/Nakroth.jpg",difficulty=5,hp=3000,attack=250,defense=120,speed=95),

Hero(name="Yorn",role="Marksman",image="https://static.wikia.nocookie.net/arenaofvalor/images/5/5c/Yorn.jpg",difficulty=2,hp=2800,attack=310,defense=100,speed=80),

Hero(name="Thane",role="Tank",image="https://static.wikia.nocookie.net/arenaofvalor/images/c/c4/Thane.jpg",difficulty=1,hp=4500,attack=150,defense=300,speed=60),

Hero(name="Zata",role="Mage",image="https://static.wikia.nocookie.net/arenaofvalor/images/8/89/Zata.jpg",difficulty=4,hp=2600,attack=320,defense=90,speed=85),

Hero(name="Murad",role="Assassin",image="https://static.wikia.nocookie.net/arenaofvalor/images/4/4a/Murad.jpg",difficulty=5,hp=2900,attack=260,defense=130,speed=92),

]

        for hero in heroes:
            db.session.add(hero)

        db.session.commit()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")

        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password,password):

            login_user(user)
            return redirect(url_for("dashboard"))

        else:
            error = "Username or Password incorrect"

    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():

    search = request.args.get("search")
    role = request.args.get("role")

    query = Hero.query

    if search:
        query = query.filter(Hero.name.contains(search))

    if role:
        query = query.filter_by(role=role)

    heroes = query.all()

    return render_template("dashboard.html", heroes=heroes)


@app.route("/add", methods=["GET","POST"])
@login_required
def add():

    if request.method == "POST":

        hero = Hero(

            name=request.form["name"],
            role=request.form["role"],
            image=request.form["image"],
            difficulty=request.form["difficulty"],
            hp=request.form["hp"],
            attack=request.form["attack"],
            defense=request.form["defense"],
            speed=request.form["speed"],
            user_id=current_user.id

        )

        db.session.add(hero)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("add_hero.html")


@app.route("/delete/<int:id>")
@login_required
def delete(id):

    hero = Hero.query.get_or_404(id)

    db.session.delete(hero)
    db.session.commit()

    return redirect(url_for("dashboard"))


@app.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit(id):

    hero = Hero.query.get_or_404(id)

    if request.method == "POST":

        hero.name = request.form["name"]
        hero.role = request.form["role"]
        hero.image = request.form["image"]
        hero.difficulty = request.form["difficulty"]
        hero.hp = request.form["hp"]
        hero.attack = request.form["attack"]
        hero.defense = request.form["defense"]
        hero.speed = request.form["speed"]

        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("edit_hero.html", hero=hero)

@app.route("/search", methods=["GET","POST"])
@login_required
def search():

    hero = None

    if request.method == "POST":

        name = request.form["name"]

        hero = Hero.query.filter(
            Hero.name.contains(name)
        ).first()

    return render_template("search.html", hero=hero)

if __name__ == "__main__":
    app.run(debug=True)