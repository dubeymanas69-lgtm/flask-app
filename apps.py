from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)


 
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()



@app.route("/")
def home():
    todo = Todo(title="first todo", desc="blah blah")
    db.session.add(todo)
    db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html" , alltodo = alltodo)

@app.route("/show")
def products():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'this is manas page '

@app.route("/akriti")
def akriti_page():
    return render_template("akriti.html")


# This single route handles all /data GET and POST requests correctly.
@app.route("/data", methods=["GET", "POST"])
def data_page():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")

        if title and desc:
            new_todo = Todo(title=title, desc=desc)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for("data_page"))
        else:
            return "Please provide both title and description", 400

    alltodo = Todo.query.all()
    return render_template("dataentries.html", alltodo=alltodo)

if __name__ == "__main__":
    app.run(debug=True)