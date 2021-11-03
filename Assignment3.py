import pandas as pd
import numpy as np
import yfinance as yf

''' QUESTION 1 '''
dates1 = pd.date_range(np.datetime64("2017-06-05"), periods = 5, freq = "D")
dates2 = dates1.append(dates1)
dates3 = dates2.append(dates1)

rawData = {
'Date': dates3,
'Company': ['Facebook']*5 + ['Google']*5 + ['Microsoft']*5,
'Price': [155,150,153,155,156,955,987,963,1000,1012,66,69,62,61,66],
'Price to earnings ratio (P/E)': [37.10, 36.98, 36.78,36.11,37.07,
                                  32.0, 31.3 ,31.7,31.2,30.0,
                                  30.31,30.56,30.46,30.11,31.00]
}

q1_1 = pd.DataFrame(rawData)
q1_2 = q1_1.pivot(index = "Date", columns = "Company")

''' QUESTION 2 '''
q2_1 = q1_1.sort_values(by="Date").set_index(['Date', 'Company'])
print(q2_1)


''' QUESTION 3 '''
q3_1 = q1_1.pivot_table(index = "Company",  aggfunc="mean")
print(q3_1)


''' QUESTION 4 '''
student = pd.DataFrame({'student name':['John', 'Bob', 'Suzan'], 'age':[20, 30, 22]})
course = pd.DataFrame({'department':['CS', 'CS', 'ENGL'], 
'course number': [233, 455, 433], 
'description':['databases', 'operating systems', 'poetry']})
takes = pd.DataFrame(
    {'student name':['John', 'John', 'Suzan'], 
    'department name': ['CS', 'CS', 'ENGL'], 
    'course number': [233, 455, 433], 
    'grade': ['C', 'B', 'A']})


''' QUESTION 5 '''
takes['grade'] = takes['grade'].apply(lambda letterGrade: 69-ord(letterGrade))
gpas = takes.groupby('student name').mean().reset_index()
gpas = pd.merge(student, gpas, how='outer', on='student name').drop(columns=['age', 'course number']).fillna(0)


''' QUESTION 6 '''
print(gpas[gpas['grade'] == 0].drop(columns = 'grade'))


''' QUESTION 7 '''
businessDays = pd.bdate_range("2018-01-01", "2018-12-31", normalize=True)
values = range(0, 261)

q7_1 = pd.Series(values, index=businessDays)
print(q7_1)


''' QUESTION 8 '''
days2018 = pd.date_range("2018-01-01", "2018-12-31").map(lambda date: date.strftime('%A'))  # used to be date.day_of_week
daysCount = pd.Series(days2018).value_counts()
daysCount.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
print(daysCount)



''' QUESTION 9 '''
googleStock = yf.Ticker("GOOG")
googleHistory = googleStock.history(start = "2017-01-01", end = "2017-12-31")[['Open', 'Close']]
googleHistory["Profit"] = googleHistory["Close"] - googleHistory["Open"]
googleHistory = googleHistory.drop(columns=['Open','Close'])
dailyAvg = googleHistory.groupby(googleHistory.index.dayofweek).sum()
dailyAvg.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
dailyAvg = dailyAvg.sort_values(by='Profit', ascending=False)
print(dailyAvg)