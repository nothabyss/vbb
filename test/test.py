import threading


class MyClass:
    def __init__(self):
        self.value = 0

    def do_something(self):
        self.value += 1
        print(f"Value is now {self.value}")


def worker(obj):
    obj.do_something()


# 创建对象
my_obj = MyClass()

# 创建子线程，将对象作为参数传递
t = threading.Thread(target=worker, args=(my_obj,))
t.start()