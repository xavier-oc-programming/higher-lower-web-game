# Day 55 — Course Notes

**Course:** 100 Days of Code: The Complete Python Pro Bootcamp  
**Instructor:** Dr. Angela Yu  
**Topic:** HTML & URL Parsing in Flask + Higher/Lower Final Project

---

## Table of Contents

- [Flask URL Routing](#flask-url-routing)
- [URL Path Variable Types](#url-path-variable-types)
- [Running Flask in Jupyter](#running-flask-in-jupyter)
- [The Flask Debugger](#the-flask-debugger)
- [Returning HTML from Routes](#returning-html-from-routes)
- [Decorators as HTML Wrappers](#decorators-as-html-wrappers)
- [Stacking Decorators](#stacking-decorators)
- [Advanced Decorators — args and kwargs](#advanced-decorators--args-and-kwargs)
- [Parameterised Decorators](#parameterised-decorators)
- [Logging Decorator Exercise](#logging-decorator-exercise)
- [Final Project — Higher/Lower URL Game](#final-project--higherlower-url-game)
- [Extra — Decorator Showcase on the Game](#extra--decorator-showcase-on-the-game)

---

## Flask URL Routing

Flask maps URL paths to Python functions using `@app.route()`.

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Homepage</h1>"
```

---

## URL Path Variable Types

Path segments can carry typed variables using angle-bracket converters.

```python
from flask import Flask
from markupsafe import escape

app = Flask(__name__)

# String (default) — single path segment
@app.route("/user/<username>")
def show_user_profile(username):
    return f"User {escape(username)}"

# int — converts segment to integer automatically
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post {post_id} (integer)"

# path — matches the rest of the URL including slashes
@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Subpath: {escape(subpath)}"
```

**Available converters:**

| Converter | Matches |
| :--- | :--- |
| `string` | Default — any text without a slash |
| `int` | Positive integers |
| `float` | Positive floating-point numbers |
| `path` | Like `string` but also accepts slashes |
| `uuid` | UUID strings |

**Multiple variables in one route:**

```python
@app.route("/user/<username>/<int:number>")
def show_user(username, number):
    return f"User {username}, you are {number} years old."
```

> `markupsafe.escape()` sanitises user-supplied strings before inserting them into responses, preventing XSS. Flask imports it from `markupsafe` automatically when using Jinja2 templates, but it must be imported explicitly when building raw strings.

---

## Running Flask in Jupyter

Flask can run inside a Jupyter notebook with two adjustments:

```python
# use_reloader=False avoids conflicts with Jupyter's own event loop
# debug=False is safest in notebook context
app.run(port=5001, debug=False, use_reloader=False)
```

---

## The Flask Debugger

`debug=True` activates two things:

1. **Auto-reloader** — the server restarts automatically on file save.
2. **Interactive debugger** — on an unhandled exception, the browser shows a full traceback with a PIN-protected in-browser Python console per stack frame.

```python
if __name__ == "__main__":
    app.run(
        port=5001,
        debug=True,
        use_reloader=True,  # explicit; included in debug=True by default
    )
```

> Never run with `debug=True` in production — the interactive console gives arbitrary code execution to anyone who can reach the server.

---

## Returning HTML from Routes

Route functions can return raw HTML strings. Flask sets `Content-Type: text/html` automatically.

```python
@app.route("/")
def home():
    return (
        '<h1 style="text-align: center">Homepage</h1>'
        '<p>This is a paragraph.</p>'
        '<img src="https://example.com/image.jpg" width=200>'
    )
```

Adjacent string literals in parentheses are concatenated by Python — no `+` needed.

---

## Decorators as HTML Wrappers

A decorator wraps a function's return value. These three wrap output in HTML tags:

```python
def make_bold(function):
    def bold_wrapper():
        return f"<b>{function()}</b>"
    return bold_wrapper


def make_emphasis(function):
    def emphasis_wrapper():
        return f"<em>{function()}</em>"
    return emphasis_wrapper


def make_underlined(function):
    def underlined_wrapper():
        return f"<u>{function()}</u>"
    return underlined_wrapper
```

---

## Stacking Decorators

Decorators are applied **bottom-up** — the decorator closest to the function runs first (innermost result), the topmost decorator runs last (outermost wrapper).

```python
@app.route("/bye")
@make_bold        # applied third → outermost: <b>...</b>
@make_emphasis    # applied second → middle:   <em>...</em>
@make_underlined  # applied first  → innermost: <u>Bye</u>
def bye():
    return "Bye"

# Result: <b><em><u>Bye</u></em></b>
```

Note: `@app.route` must always be outermost since it registers the function with Flask.

---

## Advanced Decorators — args and kwargs

Use `*args` and `**kwargs` to forward all arguments through the wrapper unchanged:

```python
class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False


def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        user = args[0]  # first positional arg is the User object
        if user.is_logged_in:
            return function(*args, **kwargs)
        else:
            print("User is not authenticated. Access denied.")
    return wrapper


@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")


new_user = User("angela")
new_user.is_logged_in = True
create_blog_post(new_user)   # → "This is angela's new blog post."
```

Without `*args`/`**kwargs`, the wrapper would not accept the `user` argument and would raise a `TypeError`.

---

## Parameterised Decorators

A decorator factory is a function that takes parameters and returns a decorator.  
This adds one extra layer of nesting:

```python
def color(col):
    """Wraps the function's return value in a coloured <h1>."""
    def decorator(function):
        def color_wrapper(*args, **kwargs):
            content = function(*args, **kwargs)
            return f'<h1 style="color:{col}; text-align:center">{content}</h1>'
        color_wrapper.__name__ = f"color_{function.__name__}"
        return color_wrapper
    return decorator


def html_tag(tag):
    """Wraps the function's return value in any HTML tag."""
    def decorator(function):
        def html_tag_wrapper(*args, **kwargs):
            content = function(*args, **kwargs)
            return f"<{tag}>{content}</{tag}>"
        html_tag_wrapper.__name__ = f"{tag}_{function.__name__}"
        return html_tag_wrapper
    return decorator
```

Usage:

```python
@color("blue")
def heading():
    return "Hello"

# heading() → '<h1 style="color:blue; text-align:center">Hello</h1>'
```

> Setting `wrapper.__name__` manually is important when stacking with Flask routes — Flask uses the function name as the endpoint name and will raise an `AssertionError` if two routes share the same endpoint name.

---

## Logging Decorator Exercise

Write a decorator that logs every call: prints the function name, its arguments, and the return value.

```python
def logging_decorator(function):
    def wrapper(*args):
        print(f"You called {function.__name__}{args}")
        result = function(*args)
        print(f"It returned: {result}")
        return result
    return wrapper


@logging_decorator
def a_function(*args):
    return sum(args)


a_function(1, 2, 3)
# You called a_function(1, 2, 3)
# It returned: 6
```

---

## Final Project — Higher/Lower URL Game

Build a Flask app where the player guesses a secret number by typing it into the URL bar.

**Requirements:**
- Pick a random secret (0–9) once at server start
- Home page (`/`) — instructions + GIF
- Route `/<int:guess>` — compare guess, return colour-coded result + GIF

```python
from flask import Flask
import random

app = Flask(__name__)

SECRET_NUMBER = random.randint(0, 9)

@app.route("/")
def home():
    return (
        '<h1 style="text-align: center;">Guess a number between 0 and 9</h1>'
        '<p style="text-align: center;">Type a number after the slash, e.g. /3</p>'
        '<div style="text-align: center;">'
        '<img src="https://i.giphy.com/3o7aCSPqXE5C6T8tBC.webp" width="300">'
        '</div>'
    )

@app.route("/<int:guess>")
def check_number(guess):
    if guess < SECRET_NUMBER:
        return '<h1 style="color: red; text-align: center;">Too low, try again!</h1>'
    elif guess > SECRET_NUMBER:
        return '<h1 style="color: purple; text-align: center;">Too high, try again!</h1>'
    else:
        return '<h1 style="color: green; text-align: center;">You found me!</h1>'

if __name__ == "__main__":
    app.run(debug=True)
```

**Key insight:** The URL path variable `<int:guess>` is the entire input mechanism — no HTML form, no JavaScript, no button. The URL *is* the interface.

---

## Extra — Decorator Showcase on the Game

The extra version adds three custom decorators to demonstrate their power on a live Flask app.

**`log_route`** — logs every route call and a preview of the response to the console:

```python
def log_route(function):
    def log_route_wrapper(*args, **kwargs):
        print(f"[LOG] Called {function.__name__} with {args} {kwargs}")
        result = function(*args, **kwargs)
        print(f"[LOG] Returned: {str(result)[:60]}...")
        return result
    log_route_wrapper.__name__ = f"log_{function.__name__}"
    return log_route_wrapper
```

**`color(col)`** — wraps output in a coloured `<h1>` (parameterised decorator):

```python
def color(col):
    def decorator(function):
        def color_wrapper(*args, **kwargs):
            content = function(*args, **kwargs)
            return f'<h1 style="color:{col}; text-align:center">{content}</h1>'
        color_wrapper.__name__ = f"color_{function.__name__}"
        return color_wrapper
    return decorator
```

**`html_tag(tag)`** — wraps output in any HTML tag (parameterised decorator):

```python
def html_tag(tag):
    def decorator(function):
        def html_tag_wrapper(*args, **kwargs):
            content = function(*args, **kwargs)
            return f"<{tag}>{content}</{tag}>"
        html_tag_wrapper.__name__ = f"{tag}_{function.__name__}"
        return html_tag_wrapper
    return decorator
```

**Stacking all three on one route:**

```python
@app.route("/bye")
@log_route              # logs the call (outermost — runs last)
@html_tag("u")          # wraps in <u>
@html_tag("em")         # wraps in <em>
@html_tag("b")          # wraps in <b>
@color("blue")          # wraps in coloured <h1> (innermost — runs first)
def bye():
    return "Goodbye, friend!"

# Result: logged, then:
# <u><em><b><h1 style="color:blue; text-align:center">Goodbye, friend!</h1></b></em></u>
```
