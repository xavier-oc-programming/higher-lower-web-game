from flask import Flask
app = Flask(__name__)

def make_bold(function):
    def bold_wrapper():
        return f"<b> {function()} </b>"
    return bold_wrapper


def make_emphasis(function):
    def emphasis_wrapper():
        return f'<em>{function()}</em>'
    return emphasis_wrapper



def make_underlined(function):
    def underlined_wrapper():
        return f'<u>{function()}</u>'
    return underlined_wrapper


@app.route("/")
def home():
    return '<h1 style="text-align: center">Homepage 3</h1>' \
    '<p>This is a paragraph, cool, right?</p>' \
    '<img src= "https://d2zp5xs5cp8zlg.cloudfront.net/image-86754-800.jpg" width=200>' \
    '<img src= "https://media1.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZW8wOW1vdHZlYjQ4aWF5b2Jva2Ezd2owZ3d0OTUwaXlqMHJnMW40ZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/hPyONzUYJhLZS/giphy.webp">'

@app.route("/user/<username>/<int:number>")
def show_user_profile(username, number):
    return f"User {username}, you are {number} years old."

@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post {post_id} (integer)"

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "Bye"

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


