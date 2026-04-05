# Higher / Lower Web Game

A number-guessing game played entirely through the browser URL bar.  
Type `/3` to guess 3. The server tells you if you're too low, too high, or spot on.

Two builds are included: a verbatim course version and a modular rebuild that fixes a real concurrency bug in the original.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Builds Comparison](#builds-comparison)
- [How to Play](#how-to-play)
- [Gameplay Rules](#gameplay-rules)
- [Features](#features)
- [Navigation Flow](#navigation-flow)
- [Architecture](#architecture)
- [Module Reference](#module-reference)
- [Configuration Reference](#configuration-reference)
- [Display Layout](#display-layout)
- [Design Decisions](#design-decisions)
- [Course Context](#course-context)
- [Dependencies](#dependencies)

---

## Quick Start

```bash
# Install Flask
pip install flask

# Launch the terminal menu
python menu.py
```

Pick **[1]** or **[2]**, then open your browser at `http://localhost:5000`.

**Run a build directly (no menu):**

```bash
cd original && python main.py
# or
cd advanced && python main.py
```

> Stop the server with `Ctrl+C`. The terminal menu reappears automatically.

---

## Builds Comparison

| Feature | Original | Advanced |
| :--- | :--- | :--- |
| Secret number scope | Server-wide global — shared by all tabs/users | Per-session — each browser tab has its own secret |
| Config constants | Hardcoded inline (`0`, `9`) | All in `config.py` |
| HTML | Inline strings in route functions | Jinja2 templates in `templates/` |
| Pure logic layer | No | `game.py` — zero Flask imports |
| Type hints | No | Throughout |
| GIF URLs | Hardcoded in routes | Constants in `config.py` |
| Guard on direct URL access | No — crashes on missing secret | Redirects `/<N>` to `/` if no session |

---

## How to Play

1. Run the server via `python menu.py` or directly.
2. Open `http://localhost:5000` — a secret number is chosen.
3. Type your guess into the URL bar: `http://localhost:5000/5`
4. Read the feedback: **Too low**, **Too high**, or **You found me!**
5. Click **Play again** on the result page to reset and start over.

---

## Gameplay Rules

- Secret number is drawn from **0 to 9** inclusive.
- Each guess is one HTTP GET request — the number goes directly in the URL path.
- A correct guess clears the session. Visiting `/` always starts a fresh game.
- No guess counter or limit — guess as many times as you like.

---

## Features

### Both Builds

**URL-based input** — no forms, no buttons. The URL path *is* the input. Visiting `/4` submits the guess 4.

**GIF feedback** — each outcome (too low, too high, correct) shows a different animated GIF alongside the heading.

**Colour-coded headings** — red for too low, purple for too high, green for correct.

**Play again link** — the result page always includes a link back to `/` to reset.

### Advanced Only

**Per-session secret number** — Flask's signed cookie session gives each browser tab its own independent secret. Two players on the same server get different numbers. This fixes a real bug in the original where all users share one global that never changes until the server restarts.

**Pure logic layer** — `game.py` contains `pick_secret()` and `check_guess()` with zero Flask imports. Logic can be unit-tested or reused without starting a server.

**Jinja2 templates** — HTML lives in `.html` files, not Python strings. `result.html` uses an `{% if %}/{% elif %}/{% else %}` block on the `outcome` variable — no HTML is constructed in Python.

**Config module** — every constant (`GUESS_MIN`, `GUESS_MAX`, `PORT`, all GIF URLs) lives in `config.py`. Changing the number range or swapping a GIF means editing one line in one file.

**Session guard** — visiting `/<N>` directly with no session (bookmarked link, page refresh after expiry) redirects to `/` instead of crashing.

---

## Navigation Flow

### Terminal Menu

```
python menu.py
│
├── [1] ──► original/main.py    Flask on port 5000
├── [2] ──► advanced/main.py    Flask on port 5000
└── [q] ──► exit
```

The menu clears the console and reappears automatically each time the server stops.

### Browser Flow

```
                      GET /
             ┌─────────────────────┐
             │     Home page       │
             │  "Guess 0 – 9"      │
             │  Secret → session   │
             └──────────┬──────────┘
                        │  GET /<number>
                        ▼
             ┌─────────────────────┐
             │    Result page      │
             │                     │
             │  "low"    → red     │
             │  "high"   → purple  │
             │  "correct"→ green   │
             │                     │
             │  [ Play again ]     │
             └──────────┬──────────┘
                        │  GET /
                        └──► Home page (new game)

GET /<number>  with no session  ──►  redirect to GET /
```

---

## Architecture

```
higher-lower-web-game/
│
├── menu.py                  # Terminal launcher — subprocess.run per build
├── art.py                   # ASCII LOGO printed by menu.py
├── requirements.txt         # Flask; Python 3.10+
├── .gitignore
├── README.md
│
├── docs/
│   └── COURSE_NOTES.md      # All Day 55 topics with annotated code examples
│
├── original/
│   └── main.py              # Verbatim course file — single-file Flask app
│
└── advanced/
    ├── config.py            # All constants — zero magic numbers elsewhere
    ├── game.py              # Pure logic — pick_secret(), check_guess()
    ├── main.py              # Flask app — routes only, calls game.py
    └── templates/
        ├── index.html       # Home page
        └── result.html      # Result page (if/elif/else on outcome)
```

---

## Module Reference

### `advanced/game.py`

| Function | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `pick_secret` | `(low: int, high: int) -> int` | `int` | Random integer in `[low, high]` inclusive |
| `check_guess` | `(secret: int, guess: int) -> str` | `"low"` \| `"high"` \| `"correct"` | Compares guess to secret |

### `advanced/main.py` — Routes

| Route | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | Picks a new secret, stores in session, renders `index.html` |
| `/<int:guess>` | GET | Calls `check_guess`, renders `result.html`; redirects to `/` if no session |

---

## Configuration Reference

All constants live in `advanced/config.py`. No magic numbers appear anywhere else.

| Constant | Default | Description |
| :--- | :--- | :--- |
| `GUESS_MIN` | `0` | Lower bound of the secret number range (inclusive) |
| `GUESS_MAX` | `9` | Upper bound of the secret number range (inclusive) |
| `PORT` | `5000` | Flask development server port |
| `DEBUG` | `True` | Flask debug mode — enables auto-reload and detailed error pages |
| `GIF_HOME` | *(URL)* | GIF shown on the home / start page |
| `GIF_LOW` | *(URL)* | GIF shown when the guess is too low |
| `GIF_HIGH` | *(URL)* | GIF shown when the guess is too high |
| `GIF_CORRECT` | *(URL)* | GIF shown when the guess is correct |

To change the number range to 1–100, edit two lines in `config.py` — nothing else needs to change.

---

## Display Layout

```
index.html
┌──────────────────────────────────────────────────┐
│                                                  │
│       Guess a number between 0 and 9             │  ← <h1>
│                                                  │
│    Type a number after the slash in the URL      │  ← <p>
│    e.g.  http://localhost:5000/3                 │
│                                                  │
│                    [GIF]                         │  ← centered img
│                                                  │
└──────────────────────────────────────────────────┘

result.html — outcome: "low"
┌──────────────────────────────────────────────────┐
│                                                  │
│           Too low, try again!                    │  ← <h1> red
│           Your guess: 2 — go higher.             │  ← <p>
│                                                  │
│                    [GIF]                         │
│                                                  │
│               [ Play again ]                     │  ← <a href="/">
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Design Decisions

**Flask session vs module-level global**

The original stores `SECRET_NUMBER = random.randint(0, 9)` at module level. It is picked once when the server starts and never changes. Every user sharing the same server shares the same secret — if one player finds it, the game is effectively over for everyone until the server restarts. The advanced build stores the secret in `session`, a signed cookie. Each browser tab gets its own number, reset every time `/` is visited. This is the correct behaviour for a per-player guessing game.

**Pure `game.py` layer with no Flask imports**

Route functions in `main.py` are deliberately thin: read the request → call `game.py` → pass the result to a template. No logic lives in the routes. This means `pick_secret()` and `check_guess()` can be unit-tested without spinning up a Flask app, and the game rules can be read without understanding Flask routing.

**Jinja2 templates vs inline HTML strings**

The original returns multi-line Python strings containing raw HTML. This works but mixes two languages in one file, breaks syntax highlighting, and buries display decisions inside route logic. Templates keep HTML in `.html` files where editors understand it, and leave routes focused on logic only.

**`config.py` for GIF URLs**

GIF URLs are long, opaque strings that have nothing to do with game logic. Putting them in `config.py` means routes and templates never mention specific URLs — they reference named constants. Swapping a GIF or changing the number range means editing one file, one line.

**Redirect on missing session**

If a user visits `/5` with no active session (bookmarked link, direct share, result-page refresh after a long gap), `session.get("secret")` returns `None`. The original would crash comparing `None` to an integer. The advanced build detects the missing session and redirects to `/`, starting a clean game.

**`subprocess.run` with `cwd=path.parent` in `menu.py`**

Each build is launched as a separate subprocess rather than imported. This keeps the menu process alive — when the server stops (Ctrl+C), the menu loop continues and redraws the prompt. The `cwd=str(path.parent)` argument is critical: it ensures that relative imports inside each build (`from config import ...`) resolve correctly regardless of where `menu.py` is invoked from.

---

## Course Context

Built during **Day 55** of [100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu.

**Topics covered on Day 55:** Flask URL routing, typed path variable converters (`<int:>`, `<path:>`), returning HTML strings from routes, Python decorators, stacking and parameterising decorators, the Flask debugger.

The Higher/Lower game is the day's final project — demonstrating URL path variables as the sole input mechanism for a game.

---

## Dependencies

| Module | Used for |
| :--- | :--- |
| `flask` | Web server, routing, session management, Jinja2 template rendering |
| `random` | Generating the secret number (`random.randint`) |
| `os` | Console clear (`os.system`) in `menu.py` |
| `sys` | `sys.executable` — ensures the subprocess uses the same Python interpreter |
| `subprocess` | Launching each build from `menu.py` without blocking the menu loop |
| `pathlib.Path` | Resolving file paths relative to each script — no hardcoded paths |
