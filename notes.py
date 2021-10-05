import numpy as np

arr = np.array([[1,2],[3,4]])

arr2 = arr * 2

print(arr2)

print(arr2 + arr2)

arr3 = np.arange(0,3,.5)
print(np.resize(arr3, (2,3)))

# print(arr3 + arr2)        # arrays arent same size so they dont work

def customFunc(x):
    if x > 3:
        return 2
    return 1

def customFunc2(x):
    if len(x) > 1:
        return 2
    return 1

result = np.vectorize(customFunc)(arr)

result2 = np.vectorize(customFunc2)(arr)    # default output type is same as first argument; must specify if need other type

print(result)

print(result2)
