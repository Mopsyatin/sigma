from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/1")
def question1():
    return render_template("question_1.html")

@app.route("/1/1")
def question2():
    return render_template("question_2.html")

@app.route("/correct")
def correct():
    return render_template("correct_question_1.html")

@app.route("/mistake")
def mistake():
    return render_template("mistake.html")

app.run(debug = True)