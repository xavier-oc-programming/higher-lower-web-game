# TODO: Create the logging_decorator() function 👇
def logging_decorator(function):
    def wrapper(*args):
        # 1) Print the function name and its arguments
        print(f"You called {function.__name__}{args}")
        # 2) Call the original function and save the result
        result = function(*args)
        # 3) Print the returned value
        print(f"It returned: {result}")
        # 4) Return the result so the function still works normally
        return result
    return wrapper


# TODO: Use the decorator 👇
@logging_decorator
def a_function(*args):
    return sum(args)


a_function(1, 2, 3)
