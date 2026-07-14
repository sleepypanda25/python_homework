import traceback

# --- Task 1: Diary ---
with open ('diary.txt', 'a') as file:
    try:
        command = input("What happened today?\n")
        file.write(command + "\n")

        while command != "done for now":
            command = input("What else?\n")
            file.write(command + "\n")
    except Exception as e:
        #print("An exception occurred." + type(e).__name__)
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")