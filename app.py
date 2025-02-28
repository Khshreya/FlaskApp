from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


with app.app_context():
    db.create_all()



@app.route("/", methods=['GET', 'POST'])
def hello_world(): 
    if request.method == 'POST':
        title = request.form.get('title')  # Use .get() to avoid KeyError
        desc = request.form.get('desc')

        if title and desc:  # Check if both fields have values
            todo = ToDo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()

    allTodo = ToDo.query.all()  # Fetch all todos
    return render_template('index.html', allTodo=allTodo)

    
@app.route('/show')
def show():
    allTodo = ToDo.query.all()
    print(allTodo)
    return 'This is the show page'

# Render update page
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = ToDo.query.get(sno)  # Fetch the ToDo by ID

    if not todo:
        return "Todo not found", 404  # Handle case if ID is invalid

    if request.method == 'POST':  # If form is submitted
        todo.title = request.form['title']
        todo.desc = request.form['desc']

        db.session.commit()  # Save changes to DB
        return redirect("/")
    
    return render_template('update.html', todo=todo)  # Render update page



@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')  # This will render about.html


if __name__ == "__main__":
    app.run(debug=True)
