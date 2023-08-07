from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/Question_1")
def question1():
    return render_template("question1.html")

app.run(debug = True)