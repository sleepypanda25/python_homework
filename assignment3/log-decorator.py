import logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))

# --- Task 1: Writing and Testing a Decorator ---
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        logger.log(logging.INFO, f"function: {func.__name__}")
        if len(args) != 0:
            logger.log(logging.INFO, f"positional parameters: {list(args)}")
        else:
            logger.log(logging.INFO, "positional parameters: none")
        if len(kwargs) != 0:
            logger.log(logging.INFO, f"keyword parameters: {dict(kwargs)}")
        else:
            logger.log(logging.INFO, "keyword parameters: none")
        logger.log(logging.INFO, f"return: {result}")

        return result
    return wrapper
    
@logger_decorator
def hello_world():
    print("Hello World!")

@logger_decorator
def true_func(*args):
    print("True dat")
    return True

@logger_decorator
def logger_return(**kwargs):
    print("Roger that")
    return logger_decorator

print("--- Task 1 ---")
hello_world()
true_func()
logger_return()