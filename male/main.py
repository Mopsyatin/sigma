from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

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
    return render_template("index.html")

@app.route("/1")
def question1():
    return render_template("question_1.html")

@app.route("/2")
def question2():
    return render_template("question_2.html")

@app.route("/3")
def question3():
     return render_template("question_3.html")

@app.route("/4")
def question4():
    return render_template("question_4.html")

@app.route("/5")
def question5():
    return render_template("question_5.html")

@app.route("/<level>/correct")
def correct(level):
    return render_template("correct.html",
                           level = str(int(level) + 1)
                           )


@app.route("/mistake")
def mistake():
    return render_template("mistake.html")

@app.route('/login', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['login']
            form_password = request.form['password']
            
            #Задание №4. Реализовать проверку пользователей
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.login and form_password == user.password:
                    return redirect('/index')
                else:
                    error = 'Неправильно указан пользователь или пароль'
                    return render_template('login.html', error=error)

            
        else:
            return render_template('login.html')



@app.route('/registration', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['login']
        password = request.form['password']
        

        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


if __name__ == "__main__":
    app.run(debug=True)