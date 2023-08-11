from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app )

questions = ['question_1.html','question_2.html','question_3.html','question_4.html','question_5.html','question_6.html']

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable =False)
    points = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'<User {self.id}>'

@app.route("/")
def main():
    return render_template("start.html")

@app.route("/menu/<points>")
def start(points):
    global questions
    questions = ['question_1.html','question_2.html','question_3.html','question_4.html','question_5.html','question_6.html']
    return render_template("index.html",
                           points = points)

@app.route("/leader/<points>")
def leader(points):
    users = User.query.order_by(User.points.desc()).filter(User.points > 0).all()
    return render_template("leader.html",
                           points = points,
                           users = users)

@app.route("/<level>/<points>")
def question(points, level):
    random_question = random.choice(questions)
    questions.remove(random_question)
    return render_template(f"{random_question}",
                           points = points,
                           level = level,)



@app.route("/<level>/correct/<points>/")
def correct(level, points):
    if int(level) == 5:
        global questions
        questions = ['question_1.html','question_2.html','question_3.html','question_4.html','question_5.html','question_6.html']
    return render_template("correct.html",
                           level = level,
                           points = points,
                           next_level = str(int(level) + 1),
                           win = str(int(points) + (int(level) * 200000)),
                           curr_level = int(level),
                           )


@app.route("/mistake/<points>")
def mistake(points):
    return render_template("mistake.html",
                           points = points)

@app.route("/registration/<points>/", methods=['GET','POST'])
def reg(points):
    if request.method == 'POST':
        login= request.form['login']
        points = points

        user = User(login=login, points = points)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/menu/' + points)
        
    return render_template('registration.html', points = points)


if __name__ == "__main__":
    app.run(debug=True)