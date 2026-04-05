# Higher / Lower Web Game

A number-guessing game played entirely through the browser URL bar. Type `/3` to guess 3. The server tells you if you're too low, too high, or spot on.

Two builds included: a verbatim course version and a modular rebuild that fixes a real concurrency bug in the original.

---

## 1. Quick Start

```bash
# Install Flask
pip install flask

# Launch the terminal menu
python menu.py
```

Then pick **[1]** or **[2]**, open your browser, and visit `http://localhost:5000`.

To run a build directly without the menu:

```bash
cd original && python main.py
cd advanced && python main.py
```

---

## 2. Builds Comparison

| Feature | Original | Advanced |
|---|---|---|
| Secret number scope | Server-wide global — shared by all tabs/users | Per-session — each browser tab has its own secret |
| Config constants | Hardcoded inline (`0`, `9`) | All in `config.py` |
| HTML | Inline strings in route functions | Jinja2 templates in `templates/` |
| Pure logic layer | No | `game.py` — zero Flask imports |
| Type hints | No | Throughout |
| GIF URLs | Hardcoded in routes | Constants in `config.py` |
| Guard on direct URL access | No | Redirects `/N` to `/` if no session exists |

---

## 3. How to Play

1. Run the server (via menu or directly).
2. Open `http://localhost:5000` in your browser.
3. A secret number between 0 and 9 is chosen.
4. Type a guess directly into the URL bar: `http://localhost:5000/5`
5. The page tells you: **Too low**, **Too high**, or **You found me!**
6. Click the link on the result page to reset and play again.

---

## 4. Gameplay Rules

- Secret number is chosen from **0 to 9** inclusive.
- Each guess is a single HTTP request — type a number after the slash.
- A correct guess clears the session. Visiting `/` starts a new game.
- There is no guess counter or limit — guess as many times as you like.

---

## 5. Features

### Both Builds

**URL-based input** — no forms, no buttons. The URL path *is* the input. Visiting `/4` submits the guess 4.

**GIF feedback** — each outcome (too low, too high, correct) shows a different animated GIF alongside the heading.

**Colour-coded headings** — red for too low, purple for too high, green for correct.

**Play again link** — the result page always includes a link back to `/` to reset.

### Advanced Only

**Per-session secret number** — Flask's signed cookie session gives each browser tab its own independent secret. Two players on the same server get different numbers. This fixes a real bug in the original where all users share one global.

**Pure logic layer** — `game.py` contains `pick_secret()` and `check_guess()` with zero Flask imports. Logic can be tested or reused without starting a server.

**Jinja2 templates** — HTML lives in `.html` files, not Python strings. The `result.html` template uses an `if/elif/else` block on the `outcome` variable — no HTML is constructed in Python.

**Config module** — every constant (`GUESS_MIN`, `GUESS_MAX`, `PORT`, GIF URLs) lives in `config.py`. Changing the number range or swapping a GIF requires editing one file.

**Session guard** — visiting `/5` directly without ever hitting `/` (no session) redirects to the home page instead of crashing.

---

## 6. Navigation Flow

### Terminal Menu

```
python menu.py
│
├── [1] → original/main.py   (Flask on port 5000)
├── [2] → advanced/main.py   (Flask on port 5000)
└── [q] → exit
```

Menu reappears automatically when the Flask server is stopped (Ctrl+C).

### Browser Flow

```
GET /
┌─────────────────────────┐
│  Home page              │
│  "Guess between 0–9"    │
│  Secret stored in session│
└────────────┬────────────┘
             │  visit /<number>
             ▼
┌─────────────────────────┐
│  Result page            │
│                         │
│  outcome == "low"    → "Too low!"    (red)    + GIF
│  outcome == "high"   → "Too high!"  (purple)  + GIF
│  outcome == "correct"→ "You found!" (green)   + GIF
│                         │
│  [Play again] → GET /   │
└─────────────────────────┘

GET /<number>  with no session → redirect to GET /
```

---

## 7. Architecture

```
higher-lower-web-game/
│
├── menu.py                  # Terminal launcher — subprocess.run per build
├── art.py                   # LOGO printed by menu.py
├── requirements.txt         # Flask; Python 3.10+
├── .gitignore
├── README.md
│
├── docs/
│   └── COURSE_NOTES.md      # Original course exercise description
│
├── original/
│   └── main.py              # Verbatim course file — single-file Flask app
│
└── advanced/
    ├── config.py            # All constants — zero magic numbers elsewhere
    ├── game.py              # Pure logic — pick_secret(), check_guess()
    ├── main.py              # Flask app — routes only, calls game.py
    └── templates/
        ├── index.html       # Home page template
        └── result.html      # Result page template (if/elif/else on outcome)
```

---

## 8. Module Reference

### `game.py`

| Function | Signature | Description |
|---|---|---|
| `pick_secret` | `(low: int, high: int) -> int` | Returns a random integer in `[low, high]` inclusive |
| `check_guess` | `(secret: int, guess: int) -> str` | Returns `"low"`, `"high"`, or `"correct"` |

### `advanced/main.py` — Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Picks a new secret, stores in session, renders `index.html` |
| `/<int:guess>` | GET | Calls `check_guess`, renders `result.html`; redirects home if no session |

---

## 9. Configuration Reference

All constants live in `advanced/config.py`.

| Constant | Default | Description |
|---|---|---|
| `GUESS_MIN` | `0` | Lower bound of the secret number range (inclusive) |
| `GUESS_MAX` | `9` | Upper bound of the secret number range (inclusive) |
| `PORT` | `5000` | Flask development server port |
| `DEBUG` | `True` | Flask debug mode — enables auto-reload and error pages |
| `GIF_LOW` | *(URL)* | GIF shown when guess is too low |
| `GIF_HIGH` | *(URL)* | GIF shown when guess is too high |
| `GIF_CORRECT` | *(URL)* | GIF shown when guess is correct |

---

## 10. Display Layout

```
Browser window — index.html

┌──────────────────────────────────────────────┐
│                                              │
│      Guess a number between 0 and 9          │  ← <h1>
│                                              │
│   Type a number after the slash in the URL   │  ← <p>
│   e.g. http://localhost:5000/3               │
│                                              │
│                  [GIF]                       │  ← centered image
│                                              │
└──────────────────────────────────────────────┘

Browser window — result.html (outcome: "low")

┌──────────────────────────────────────────────┐
│                                              │
│           Too low, try again!                │  ← <h1> red
│                                              │
│                  [GIF]                       │
│                                              │
│              [ Play again ]                  │  ← link to /
│                                              │
└──────────────────────────────────────────────┘
```

---

## 11. Design Decisions

**Flask session vs module-level global for the secret number**

The original stores `SECRET_NUMBER = random.randint(0, 9)` at module level. This is picked once when the server starts and never changes. Every user hitting the same server shares the same secret — if one player finds it, the number is "used up" for everyone until the server restarts. The advanced build stores the secret in `session`, which is a signed cookie. Each browser tab gets its own number, reset every time `/` is visited. This is the correct behaviour for a guessing game.

**Pure `game.py` layer with no Flask imports**

Route functions in `main.py` are thin: they read the request, call `game.py`, and pass the result to a template. No logic lives in the routes. This means `pick_secret()` and `check_guess()` can be unit-tested without spinning up a Flask app, and the game rules can be read without understanding Flask routing.

**Jinja2 templates vs inline HTML strings**

The original returns multi-line Python strings containing raw HTML. This works but mixes two languages in one file, makes syntax highlighting useless, and puts all display decisions inside the route. Templates keep HTML in `.html` files where editors understand it, and let the route stay focused on logic.

**`config.py` for GIF URLs**

GIF URLs are long, opaque strings that have nothing to do with game logic. Putting them in `config.py` means the routes and templates never mention specific URLs — they just reference named constants. Swapping a GIF means editing one line in one file.

**Redirect on missing session**

If a user visits `/5` directly (bookmarked link, shared URL, refreshed result page after a long gap), there is no session secret. The original would crash trying to compare `None` to an integer. The advanced build detects a missing session with `session.get("secret")` and redirects to `/`, which starts a clean game.

---

## 12. Course Context

Built during **Day 55** of [100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu.

Day 55 topics: Flask URL routing, URL path variable types (`<int:>`, `<path:>`), returning HTML from routes, Python decorators, stacking decorators, the Flask debugger.

The Higher/Lower game is the day's final project — demonstrating URL variables as game input.

---

## 13. Dependencies

| Module | Used for |
|---|---|
| `flask` | Web server, routing, session management, template rendering |
| `random` | Generating the secret number |
| `os` | Console clear in `menu.py` |
| `sys` | `sys.executable` for subprocess launch in `menu.py` |
| `subprocess` | Launching builds from `menu.py` |
| `pathlib.Path` | Resolving file paths relative to each script |
