from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app )

questions = ['question_1.html','question_2.html','question_3.html','question_4.html','question_5.html','question_6.html', 'question_7.html','question_8.html','question_9.html', 'question_10.html']
memes = ['https://cdn.discordapp.com/attachments/1104405505146896386/1141977906353020968/meme_3.jpg', 'https://cdn.discordapp.com/attachments/1104405505146896386/1141975353129193502/meme_1.jpg',
         'https://cdn.discordapp.com/attachments/1104405505146896386/1141980621825126420/34e3f4b07376ef0480c57c078958b6f4.png', 'https://cdn.discordapp.com/attachments/1104405505146896386/1141980622240358430/9b5e8acba14a73564646bb5b553388bf.png', 'https://cdn.discordapp.com/attachments/1104405505146896386/1141980622840135770/6360b44e0608788a024efe02dd07ade4.png',
         'https://cdn.discordapp.com/attachments/1104405505146896386/1141980623494455296/179221c75933c2a56239802e533c345d.png', 'https://cdn.discordapp.com/attachments/1104405505146896386/1141980624106815508/13502abc20f2f7065a025181410fd862.png', 'https://cdn.discordapp.com/attachments/1104405505146896386/1141980624555618314/4cbfdb7967ca7ac87d0d261d8bc86d56.png']
meeme = ''

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
    questions = ['question_1.html','question_2.html','question_3.html','question_4.html','question_5.html','question_6.html','question_7.html','question_8.html','question_9.html']
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

@app.route("/meme/<points>/")
def random_meme(points):
    global meeme
    return render_template("random_meme.html", points=points, meeme = random.choice(memes))



if __name__ == "__main__":
    app.run(debug=True)