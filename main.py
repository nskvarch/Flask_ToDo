import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
from model import Task, User

app = Flask(__name__)
app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'

# app.secret_key = os.environ.get("SECRET_KEY").encode()


@app.route('/')
def home():
    return redirect(url_for('all_tasks'))


@app.route("/all")
def all_tasks():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template("all.jinja2", tasks=Task.select())


@app.route("/create", methods=["GET", "POST"])
def create_task():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        task = Task(taskname=request.form["taskname"])
        task.save()

        return redirect(url_for("all_tasks"))
    else:
        return render_template("create.jinja2")


@app.route("/incomplete", methods=["GET", "POST"])
def incomplete():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        user = User.select().where(User.username == session["username"]).get()
        Task.update(completed=datetime.now(), completed_by=user).where(Task.id == request.form["task_id"]).execute()

    return render_template("incomplete.jinja2", tasks=Task.select().where(Task.completed_by.is_null()))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = User.select().where(User.username == request.form["username"]).get()
        except User.DoesNotExist:
            return render_template("login.jinja2", error="Incorrect Username and or Password")

        if user and pbkdf2_sha256.hash(request.form["username"]):
            session["username"] = request.form["username"]
            return redirect(url_for("all_tasks"))

        else:
            return render_template("login.jinja2", error="Incorrect Username and or Password")

    else:
        return render_template("login.jinja2")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
