class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False


def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        # args[0] will be the `user` object passed to the decorated function
        user = args[0]

        if user.is_logged_in:
            # Forward all arguments correctly
            return function(*args, **kwargs)
        else:
            print("User is not authenticated. Access denied.")
    return wrapper


@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")


# ---- RUN TEST ----
print("\n\n----------The code starts here----------\n\n")
new_user = User("angela")
new_user.is_logged_in = True   # Change to False to test failure
create_blog_post(new_user)

print("\n\n----------The code ends here----------\n\n")
