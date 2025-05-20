from datetime import datetime
import time


class Dec:

    global tt

    def simple_decorator(func):
        tt = "teste"
        def wrapper(name):
            print("Before the function call")
            time_start = datetime.now()
            # Call the original function and store the result
            say = func(name)

            time_stop = datetime.now()
            time_delta = (time_stop - time_start).microseconds      

            print(f"After the function call. time:{time_delta}")
            print(f"tt-> {tt}")
            # Return the result
            return say
        return wrapper
    
    
    simple_decorator = staticmethod( simple_decorator )

dec = Dec()

@dec.simple_decorator
def say_hello(name):
    time.sleep(0.5)
    print("Function being excuted")
    print(f"Hello {name}!")


say_hello('Rohit')