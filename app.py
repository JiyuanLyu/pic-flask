# Import the packages and
# the function render_template() (will define later)
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
    This function will display messages with rander_template()
    from random_messages() in view.html
    """

    # Set a limit number of the shown messages
    num = 5
    # Display the limit number messages in the view.html
    shown = random_messages(num)
    return render_template('view.html', messages = shown)

