from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask import Flask,request,render_template,url_for,redirect
from sqlalchemy import Column,Integer,String,Float,Boolean,DateTime


app=Flask(__name__)
port = int(os.environ.get('PORT', 5000))
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db=SQLAlchemy(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')


class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Boolean)
    date=db.Column(db.DateTime,nullable=False)


@app.route('/')
def index():
    all_todo=Todo.query.all()

    return render_template('index.html',all_todo=all_todo)

@app.route('/add',methods=['POST'])
def add_todo():
    des=request.form['desc']
    completed=False
    date=datetime.strptime(request.form['clock'],'%a %d %m %Y %H:%M:%S')
    todo=Todo(description=des,completed=completed,date=date)
    db.session.add(todo)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/alter_checked/<int:id>',methods=['POST'])
def alter_checked(id):
    id=int(id)
    todo_by_id=Todo.query.filter_by(id=id).first()
    todo_by_id.completed=True
    db.session.add(todo_by_id)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_todo/<int:id>',methods=['POST'])
def delete_todo(id):
    id=int(id)
    todo_by_id=Todo.query.filter_by(id=id).first()
    db.session.delete(todo_by_id)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit_todo/<int:id>',methods=['POST'])
def edit_todo(id):
    id=int(id)
    desc=request.form.get('description')
    return render_template('edit_todo.html',desc=desc,id=id)

@app.route('/update_todo/<int:id>',methods=['POST'])
def update_todo(id):
    id=int(id)
    todo_by_id=Todo.query.filter_by(id=id).first()
    desc=request.form.get('description')
    date=datetime.strptime(request.form['clock'],'%a %d %m %Y %H:%M:%S')
    todo_by_id.description=desc
    todo_by_id.date=date
    db.session.commit()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

