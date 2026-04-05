from flask import Flask, session, render_template, redirect, url_for
from pathlib import Path

import game
from config import GUESS_MIN, GUESS_MAX, PORT, DEBUG
from config import GIF_HOME, GIF_LOW, GIF_HIGH, GIF_CORRECT

app = Flask(__name__, template_folder=str(Path(__file__).parent / "templates"))
app.secret_key = "change-me-before-deploying"


@app.route("/")
def home():
    session["secret"] = game.pick_secret(GUESS_MIN, GUESS_MAX)
    return render_template(
        "index.html",
        low=GUESS_MIN,
        high=GUESS_MAX,
        gif=GIF_HOME,
    )


@app.route("/<int:guess>")
def check(guess: int):
    secret = session.get("secret")
    if secret is None:
        return redirect(url_for("home"))

    outcome = game.check_guess(secret, guess)

    if outcome == "correct":
        session.pop("secret", None)

    gifs = {"low": GIF_LOW, "high": GIF_HIGH, "correct": GIF_CORRECT}

    return render_template(
        "result.html",
        outcome=outcome,
        guess=guess,
        low=GUESS_MIN,
        high=GUESS_MAX,
        gif=gifs[outcome],
    )


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
