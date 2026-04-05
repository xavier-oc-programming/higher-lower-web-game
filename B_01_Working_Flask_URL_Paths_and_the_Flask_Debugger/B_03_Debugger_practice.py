from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Homepage 3</h1>"

@app.route("/user/<username>/<int:number>")
def show_user_profile(username, number):
    return f"User {username}, you are {number} years old."

@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post {post_id} (integer)"

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Subpath: {subpath}"


if __name__ == "__main__":
    # Simple Flask dev server with auto-reload
    print("[Flask] Running in SOLO mode (Flask reloader ON)")
    app.run(
        port=5001,
        debug=True,        # enables reloader + debugger toolbar
        use_reloader=True  # explicit for clarity
    )
