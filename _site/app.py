# Import the packages and
# the function render_template() (will define later)
import cmd
from random import random
from flask import Flask, g, render_template, request
import sqlite3
app = Flask(__name__)

# First, define a main() function
@app.route("/")
def main():
    """
    This function will return the home base page
    with render_template()
    """ 

    return render_template("base.html")

# Then, define a submit() function to
# put the input message into the database
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    """
    This function will use render_template()
    to submit function into the database
    """
    
    if request.method == 'GET':
        # Use render_template() to GET the message
        return render_template('submit.html')
    else:
        # Use insert_message() to INSERT the message
        # into database
        insert_message(request)
        return render_template('submit.html', thanks=True)

# Define a function for user to
# view messages in the database
@app.route('/view/')
def view():
    """
    This function will display messages with render_template()
    from random_messages() in view.html
    """

    # Set a limit number of the shown messages
    num = 10
    # Display the limit number messages in the view.html
    shown = random_messages(num)
    return render_template('view.html', messages = shown)

# Then write a Python function `get_message_db()` to handle creating the database of messages
def get_message_db():
    """
    This function will check the database `message_db` in the `g`
    and the table `messages` exists in `message_db`,
    create if they do not exist.
    """

    # Firstly, check if there are a database called `message_db`
    # in `g` attribute of the app
    if 'message_db' not in g:
        # If not, create one
        g.message_db = sqlite3.connect("messages_db.sqlite")
    cursor = g.message_db.cursor()

    # Create table `messages` if it does not exist with SQLite
    # The table should include an `id`` column (integer),
    # a `handle`` column (text), and a `message`` column (text)
    cmd = "CREATE TABLE IF NOT EXISTS messages (id INTEGER, handle TEXT, message TEXT)"
    cursor.execute(cmd)

    # Return the connnection
    return g.message_db

# Write a funtcion `insert_message(request)` to handle inserting a user message into the database `message_db`
def insert_message(request):
    """
    This function will extract the `message` and the `handle`
    from `request`, and then using a cursor to insert the message
    into the database `message_db`
    """

    # Extract the message and handle
    user_message = request.form["message"]
    user_handle = request.form["name"]

    # Use the returning connection of `get_message_db()`
    db = get_message_db()
    cursor = db.cursor()

    # Count the user id
    user_id = cursor.execute("SELECT COUNT(*) FROM messages;").fetchone()[0]+1
    # Insert the message into the database `message_db`
    cursor.execute("INSERT INTO messages (id, message, handle) VALUES (?, ?, ?)",
                   (user_id, user_message, user_handle))
    # Ensure the inserted row has been saved
    db.commit()
    # Close the database connection
    db.close()


def random_messages(n):
    """
    This function will return a collection of `n` random messages
    from the database `message_db`.
    """

    # Connect to the database
    db = get_message_db()
    cursor = db.cursor()
    random_n = cursor.execute(f'SELECT message, handle FROM messages ORDER BY RANDOM() LIMIT {n}').fetchall()
    # Close the connection
    db.close()

    return random_n
