from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/<way>")
def question1(way):
    way = way
    return render_template("question1.html")

@app.route("/<way>")
def question2(way):
    way = way
    return render_template("question_2.html")

@app.route("/correct")
def correct():
    return render_template("correct.html")

@app.route("/mistake")
def mistake():
    return render_template("mistake.html")

app.run(debug = True)