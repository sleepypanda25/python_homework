import logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))

# --- Task 1: Writing and Testing a Decorator ---
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        logger.log(logging.INFO, "function: " + func.__name__)
        logger.log(logging.INFO, "positional parameters: " + args)
        logger.log(logging.INFO, "keyword parameters:" + kwargs)
        logger.log(logging.INFO, "return: " + result)

        return result
    return wrapper
    
@logger_decorator
def hello_world():
    print("Hello World!")

@logger_decorator
def true_func(*args):
    print("True dat")
    return True

def logger_return(**kwargs):
    print("Roger that")
    return logger_decorator

print("--- Task 1 ---")
hello_world()
true_func()
logger_return()