import time

def timer(n):
    def wrap1(func):
        def wrap2(*args,**kwargs):
            t0 = time.time()
            for i in range(n):
                result = func(*args,**kwargs)
            t1 = time.time()
            print(t1 - t0)
            return result
        return wrap2
    return wrap1

@timer(1000000)
def foo(x,y):
    return x ** y

print(foo(100,4))

'''
装饰器可以带参数,无非就是在定义函数时在加一层
def deco(n)                               # 代表的是添加的参数
    def wrap1(func)                       # func代表的是views中的函数
        def wrap2(*agrs,**kwagrs)         # *agrs,**kwagrs是func函数的参数
            response = func(*agrs,**kwagrs) #每一层定义的函数都要有返回值
            return response
        return wrap2
    return wrap1
    
@deco(10)
def foo(x,y)
    return x ** y
    
foo(10,3)   #调用函数

'''
