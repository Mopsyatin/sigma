from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable =False)
    password = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f'<Card {self.id}>'

@app.route("/")
def main():
    return render_template("start.html")

@app.route("/menu/<points>")
def start(points):
    return render_template("index.html",
                           points = points)

@app.route("/<level>/<points>")
def question(points, level):
    return render_template('question_1.html',
                           points = points,
                           level = level)



@app.route("/<level>/correct/<points>/")
def correct(level, points):
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

@app.route('/<points>/login', methods=['GET','POST'])
def login(points):
        error = ''
        if request.method == 'POST':
            form_login = request.form['login']
            form_password = request.form['password']
            
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.login and form_password == user.password:
                    return redirect('/menu/<points>', points = points)
            else:
                error = 'Неправильно указан пользователь или пароль'
                return render_template('login.html', error=error, points = points)

            
        else:
            return render_template('login.html', 
                                   points = points)



@app.route('/registration/<points>', methods=['GET','POST'])
def reg(points):
    if request.method == 'POST':
        login= request.form['login']
        password = request.form['password']
        

        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/login/<points>')
    
    else:    
        return render_template('registration.html', points = points)


if __name__ == "__main__":
    app.run(debug=True)