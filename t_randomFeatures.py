import numpy as np
import pandas as pd

"""queryNum docNum relevance empty
1 1 2
1 2 1
1 3 2
1 4 4
1 5 -1"""

queryNums = np.arange(start=1, stop=21)
queryNums = np.append(queryNums, queryNums)
queryNums = np.append(queryNums, queryNums)
queryNums = np.sort(queryNums)

docNums = np.random.randint(1, 101, 80)

relevance = np.random.randint(-1, 4, 80)

dataFrame = pd.DataFrame({'queryNum':queryNums,'docNum':docNums,'relevance':relevance,'empty':[None]*80})
# dataFrame.set_index('queryNum', inplace=True)

print(dataFrame)

dataFrame.to_csv('humanJudgementTest',sep=' ', index=None,mode='a')
# np.savetxt('humanJudgementTest', dataFrame.values)
# with open('humanJudgements', 'w+') as file:
