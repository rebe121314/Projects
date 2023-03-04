from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import func

try:
    from app import app as app, db, Task
except ImportError:
    from __init__ import app, db, Task



# Avoids errors when the databse hasen't been used
@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/" , methods=['GET', 'POST'])
def homepage():
    """
    This is the homepage of the app
    """
    tasks = None
    error = None
    if request.method == 'POST':
            #id = (Task.query(func(Task.id).filter())) + 1
            task = Task(title=request.form.get("title"), status='todo')
            tasks = Task.query.all()

            db.session.add(task)
            db.session.commit()
            return redirect(url_for('homepage'))
    todo = Task.query.filter_by(status='todo').all()
    inprogress = Task.query.filter_by(status='inprogress').all()
    done = Task.query.filter_by(status='done').all()
    return render_template("index.html", todo=todo, inprogress=inprogress, done=done)
    


@app.route("/delete",methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
            task = Task.query.filter_by(id=request.form.get("id")).first()
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for('homepage'))
    else:
            return redirect(url_for('homepage'))
    

@app.route("/update_next", methods=['GET', 'POST'])
def update_next():
    if request.method == 'POST':
        task = Task.query.filter_by(id=request.form.get("id")).first()
        if task.status == "todo":
            task.status = "inprogress"
        elif task.status == "inprogress":
            task.status = "done"
        db.session.commit()
        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('homepage'))
   

@app.route("/update_pre", methods=['GET', 'POST'])
def update_pre():
    if request.method == 'POST':
        task = Task.query.filter_by(id=request.form.get("id")).first()
        if task.status == "inprogress":
            task.status = "todo"
        elif task.status == "done":
            task.status = "inprogress"
        db.session.commit()
        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('homepage'))
    