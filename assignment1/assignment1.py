# --- Task 1: Hello ---
def hello():
    return "Hello!"

print("--- Task 1 ---")
print(hello())

# --- Task 2: Greet with a Formatted String ---
def greet(name):
    return f"Hello, {name}!"

print("\n--- Task 2 ---")
print(greet("Amanda"))

# --- Task 3: Calculator ---
def calc(num1, num2, operation="multiply"):
    try:
        if operation == "add":
            return num1 + num2
        elif operation == "subtract":
            return num1 - num2
        elif operation == "divide":
            return float(num1) / float(num2)
        elif operation == "modulo":
            return num1 % num2
        elif operation == "int_divide":
            return num1 / num2
        elif operation == "power":
            return num1 ** num2
        else:
            return num1 * num2
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
    except Exception as e:
        return e

print("\n--- Task 3 ---")
print(calc(1, 2, "add"))
print(calc(4, 2, "subtract"))
print(calc(1, 2))
print(calc(4, 2, "divide"))
print(calc(1, 2, "modulo"))
print(calc(4, 2, "int_divide"))
print(calc(2, 3, "power"))
print(calc(10, 0, "divide"))
print(calc("1", "2"))

# --- Task 4: Data Type Conversion ---
def data_type_conversion(value, type):
    try:
        if type == "int":
            return int(value)
        if type == "float":
            return float(value)
        if type == "str":
            return str(value)
    except ValueError:
        return f"You can't convert {value} into a {type}."

print("\n--- Task 4 ---")
print(data_type_conversion(5, "float"))
print(data_type_conversion(5, "str"))
print(data_type_conversion("hello", "float"))

# --- Task 5: Grading System, Using *args ---
def grade(*args):
    try:
        average = sum(args) / len(args)

        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except:
        return "Invalid data was provided."

print("\n--- Task 5 ---")
print(grade(90, 95, 96, 92, 99, 92, 91, 100))
print(grade(90, 95, 96, 92, 99, "92", 91, 100))

# --- Task 6: Use a For Loop with a Range ---
def repeat(string, count):
    new_string = ""

    for i in range(count):
        new_string += string
    
    return new_string

print("\n--- Task 6 ---")
print(repeat("hello", 5))

# --- Task 7: Student Scores, Using **kwargs ---
def student_scores(request, **kwargs):
    if request == "best":
        best = None

        for key, value in kwargs.items():
            if best==None or value > kwargs.get(best):
                best = key
        
        return best
    elif request == "mean":
        return sum(kwargs.values()) / len(kwargs.values())

print("\n--- Task 7 ---")
print(student_scores("best", John=85, Sara=90, Alex=97))
print(student_scores("mean", John=85, Sara=90, Alex=97))

# --- Task 8: Titleize, with String and List Operations ---
def titleize(title):
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    words = title.split()

    for i in range(len(words)):
        word = words[i]
        if word not in little_words or i == 0 or i == len(words) - 1:
            words[i] = word.capitalize()
    return " ".join(words)

print("\n--- Task 8 ---")
print(titleize("harry potter"))

# --- Task 9: Hangman, with more String Operations ---
def hangman(secret, guess):
    letters = list(secret)

    for i in range(len(letters)):
        letter = letters[i]

        if letter not in guess:
            letters[i] = "_"
    
    return "".join(letters)

print("\n--- Task 9 ---")
print(hangman("chicken", "ck"))

# --- Task 10: Pig Latin, Another String Manipulation Exercise ---
def pig_latin(string):
    vowels = ["a", "e", "i", "o", "u"]
    words = string.split()

    for i in range(len(words)):
        word = words[i]
        start = word[0]

        if start in vowels:
            words[i] = word + "ay"
        else:
            j = 1

            while j < len(word) and word[j] not in vowels:
                start += word[j]
                if word[j] == "q":
                    start += word[j + 1]
                    j += 1
                j += 1
            
            word = word[j:] + start + "ay"
            words[i] = word
        
    return " ".join(words)


print("\n--- Task 10 ---")
print(pig_latin("my name is amanda"))