

class logger():
    def __init__(self, func):
        self.calls= 0
        self.func = func

    def __call__(self, *args):
        self.calls += 1
        print("call %d to %s" % (self.calls, self.func.__name__))
        self.func(*args)

@logger
def add(a,b):
    print("a + b = ",(a+b))


add(1,2)
add(3,4)
add(3,4)
