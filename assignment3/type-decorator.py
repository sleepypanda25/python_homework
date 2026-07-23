# --- Task 2: A Decorator that Takes an Argument ---
def type_converter(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return type_of_output(func(*args, **kwargs))
        return wrapper
    return decorator

@type_converter(str)
def return_int():
    return 5

@type_converter(int)
def return_string():
    return "not a number"

print("--- Task 2 ---")
y = return_int()
print(type(y).__name__) # This should print "str"
try:
   y = return_string()
   print("shouldn't get here!")
except ValueError:
   print("can't convert that string to an integer!") # This is what should happen