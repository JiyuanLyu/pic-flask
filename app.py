from flask import Flask, g, render_template, request
import sqlite3
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html")

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        insert_message(request)
        return render_template('submit.html', thanks=True)
