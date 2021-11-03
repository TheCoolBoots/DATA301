import pandas as pd
import numpy as np

""" QUESTION 1 """

a1 = 2 * np.ones((10,10))

a2 = np.arange(1,101).reshape(10,10)

a3 = a2[-2:]

# a4 = a2.resize((5,20))

a5 = np.hstack([a1,a2])

a5_5 = np.vstack([a1,a2])

a6 = a2.sum(axis = 1)
print(a6)

a7 = a2.diagonal().mean()

data = {
    'id':[1,3,6],
    'name':['Bob','John','Suzan'],
    'age':[22,25,33],
    'salary':[20000,50000,100000],
    'department':['UI', 'UI','Testing']
}

q8 = pd.DataFrame(data)

data2 = {
    'department name':['UI', 'Testing'],
    'budget':[2000000, 4000000]
}

q9 = pd.DataFrame(data2)

q10 = q8.groupby('department')['salary'].mean()

q11 = q8[q8['salary'] == q8['salary'].max()]

# print(q11)

q12 = q8['age'].corr(q8['salary'])

tmp = pd.merge(q10, q9, left_on = 'department', right_on = 'department name')

q13 = tmp['salary'].corr(tmp['budget'])

data3 = {
    'Monday':[2,2,3],
    'Tuesday':[1,4,3],
    'Wednesday':[2,2,0],
    'Thursday':[2,5,1]
}

q14 = pd.DataFrame(data3, index=["Camry", "Prius", "Prime"]).stack()
print(q14.loc['Prius']['Thursday'])