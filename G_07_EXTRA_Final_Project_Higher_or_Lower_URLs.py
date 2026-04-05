# server.py
from flask import Flask
import random

app = Flask(__name__)

# Pick the secret number ONCE when the server starts
SECRET_NUMBER = random.randint(0, 9)
print(f"[DEBUG] Secret number is: {SECRET_NUMBER}")


# -------------------------
# DECORATORS
# -------------------------

def log_route(function):
    """Log every route call with arguments and partial result."""
    def log_route_wrapper(*args, **kwargs):
        print(f"[LOG] Called {function.__name__} with {args} {kwargs}")
        result = function(*args, **kwargs)
        preview = str(result)
        print(f"[LOG] Returned: {preview[:60]}...")
        return result

    # Give the wrapper a unique, descriptive name per function
    log_route_wrapper.__name__ = f"log_{function.__name__}"
    return log_route_wrapper


def color(col):
    """Change the <h1> color of the function output."""
    def decorator(function):
        def color_wrapper(*args, **kwargs):
            content = function(*args, **kwargs)
            return f'<h1 style="color:{col}; text-align:center">{content}</h1>'

        # Unique name based on the wrapped function
        color_wrapper.__name__ = f"color_{function.__name__}"
        return color_wrapper

    return decorator


def html_tag(tag):
    """Wrap returned text in an HTML tag."""
    def decorator(function):
        def html_tag_wrapper(*args, **kwargs):
            content = function(*args, **kwargs)
            return f"<{tag}>{content}</{tag}>"

        # Unique name including the tag
        html_tag_wrapper.__name__ = f"{tag}_{function.__name__}"
        return html_tag_wrapper

    return decorator


# -------------------------
# ROUTES
# -------------------------

@app.route("/")
@log_route
def home():
    return (
        "Guess a number between 0 and 9"
        '<br><br><img src="https://i.giphy.com/3o7aCSPqXE5C6T8tBC.webp " width="300">'
    )


@app.route("/<int:guess>")
@log_route
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


# Extra route to show decorator power
@app.route("/bye")
@log_route
@html_tag("u")
@html_tag("em")
@html_tag("b")
@color("blue")
def bye():
    return "Goodbye, friend!"


# -------------------------
# RUN SERVER
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
