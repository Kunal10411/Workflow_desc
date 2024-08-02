from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///work.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    desc = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title} - {self.desc}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('desc')
        new_work = Work(title=title, desc=desc)
        db.session.add(new_work)
        db.session.commit()

    all_work = Work.query.all()
    return render_template("index.html", allWork=all_work)



@app.route('/delete/<int:id>')
def delete(id):
    work=Work.query.filter_by(id=id).first()
    db.session.delete(work)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=="POST":
        title = request.form.get('title')
        desc = request.form.get('desc')
        work=Work.query.filter_by(id=id).first()
        work.title=title
        work.desc=desc
        db.session.add(work)
        db.session.commit()
        return redirect("/")

    work=Work.query.filter_by(id=id).first()
    return render_template("update.html", work=work)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
