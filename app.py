from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
    db.init_app(app)  

    with app.app_context():
        db.create_all()  # Create the database tables

    return app

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())  # Use utcnow for better practice

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"  # Corrected from self.no to self.sno


app = create_app()

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method=="POST":
      title =request.form['title']
      desc =request.form['desc']
      todo = Todo(title=title, desc=desc)
      db.session.add(todo)
      db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method =='POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    return render_template('update.html',todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False, port=5000)
