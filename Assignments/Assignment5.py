import pandas as pd

ageData = ['Young','Old','Young','Middle Age','Young','Old','Middle Age','Young','Old','Old']
incomeData = ['Middle class','High','Low','High','High','Middle class','Low','Low','Middle class','High']
carData = ['Yes','Yes','No','Yes','No','No','Yes','Yes','No','Yes']

dataset = pd.DataFrame({'Age': ageData, 'Income':incomeData,'Owns Car': carData})

dataset['AgeCat'] = pd.Categorical(dataset['Age'])

print(dataset)