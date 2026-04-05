# Day 55 — Course Notes

**Course:** 100 Days of Code: The Complete Python Pro Bootcamp  
**Instructor:** Dr. Angela Yu  
**Topic:** HTML & URL Parsing in Flask + Higher/Lower Final Project

---

## What the Day Covered

### Flask URL Routing

Flask maps URL paths to Python functions using the `@app.route()` decorator.
Path segments can carry typed variables:

```python
@app.route("/user/<username>/<int:number>")
def show_user(username, number):
    return f"User {username}, age {number}"
```

Supported converters: `string` (default), `int`, `float`, `path`, `uuid`.

### The Flask Debugger

Running with `debug=True` activates:
- Auto-reload on file save
- Interactive in-browser traceback with a PIN-protected console

```python
app.run(debug=True)
```

### Returning HTML from Routes

Route functions can return raw HTML strings. Flask sets the response
`Content-Type` to `text/html` automatically.

```python
@app.route("/")
def home():
    return "<h1>Hello</h1><p>This is HTML.</p>"
```

### Python Decorators as HTML Wrappers

A decorator wraps a function's return value. Stacking decorators
applies them bottom-up (innermost first):

```python
def make_bold(fn):
    def wrapper():
        return f"<b>{fn()}</b>"
    return wrapper

@make_bold        # applied second → outermost <b>
@make_emphasis    # applied first  → innermost <em>
def message():
    return "Hello"

# Result: <b><em>Hello</em></b>
```

### Advanced Decorators — `*args` and `**kwargs`

To forward all arguments through a wrapper:

```python
def decorator(fn):
    def wrapper(*args, **kwargs):
        # pre-logic
        result = fn(*args, **kwargs)
        # post-logic
        return result
    return wrapper
```

### Parameterised Decorators

A decorator factory takes parameters and returns a decorator:

```python
def color(col):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            content = fn(*args, **kwargs)
            return f'<h1 style="color:{col}">{content}</h1>'
        return wrapper
    return decorator

@color("blue")
def heading():
    return "Hello"
```

---

## Final Project — Higher/Lower URL Game

The exercise: build a Flask app where the user guesses a number by
typing it directly into the URL bar.

**Requirements:**
- Pick a random secret number (0–9) when the server starts
- Home page (`/`) shows instructions and a GIF
- Route `/<int:guess>` checks the guess and returns:
  - Too low → red heading + GIF
  - Too high → purple heading + GIF
  - Correct → green heading + GIF

**Key learning:** URL path variables as game input — no forms, no
JavaScript, no buttons. The URL *is* the interface.

---

## Files from This Day

| File | Purpose |
|---|---|
| `B_01_Working_Flask_URL_Paths_and_the_Flask_Debugger.py` | URL variable types demo |
| `B_03_Debugger_practice.py` | Debugger + URL routing exercises |
| `C_02_Rendering_HTML_Elements_with_Flask.py` | HTML from routes + decorator wrappers |
| `D_03_Challenge_Use_Python_Decorators_to_Style_HTML_Tags.py` | Stacked decorator challenge |
| `E_04_Advanced_Decorators_with_args_and_kwargs.py` | Auth-gate decorator with `*args`/`**kwargs` |
| `F_05_Coding_Exercise_23_Advanced_Decorators.py` | Logging decorator exercise |
| `G_06_Final_Project_Higher_or_Lower_URLs.py` | Final project — clean version |
| `G_07_EXTRA_Final_Project_Higher_or_Lower_URLs.py` | Final project + extra decorators (`log_route`, `color`, `html_tag`) |
