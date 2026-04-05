# server.py
from flask import Flask
import random

app = Flask(__name__)

# Pick the secret number ONCE when the server starts
SECRET_NUMBER = random.randint(0, 9)
print(f"[DEBUG] Secret number is: {SECRET_NUMBER}")


@app.route("/")
def home():
    """Home page: ask user to guess and show a fun GIF."""
    return (
        '<h1 style="text-align: center;">Guess a number between 0 and 9</h1>'
        '<p style="text-align: center;">Type a number after the slash in the URL, e.g. <code>/3</code></p>'
        '<div style="text-align: center;">'
        '<img src="https://i.giphy.com/3o7aCSPqXE5C6T8tBC.webp" width="300">'
        "</div>"
    )


@app.route("/<int:guess>")
def check_number(guess):
    """Check the user's guess against the secret number."""
    if guess < SECRET_NUMBER:
        # TOO LOW
        return (
            '<h1 style="color: red; text-align: center;">Too low, try again!</h1>'
            '<div style="text-align: center;">'
            '<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" width="300">'
            "</div>"
        )

    elif guess > SECRET_NUMBER:
        # TOO HIGH
        return (
            '<h1 style="color: purple; text-align: center;">Too high, try again!</h1>'
            '<div style="text-align: center;">'
            '<img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif" width="300">'
            "</div>"
        )

    else:
        # JUST RIGHT
        return (
            '<h1 style="color: green; text-align: center;">You found me!</h1>'
            '<div style="text-align: center;">'
            '<img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif" width="300">'
            "</div>"
        )


if __name__ == "__main__":
    # Run on port 5000 by default (you can change if you want)
    app.run(debug=True)
