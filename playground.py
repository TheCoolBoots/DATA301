import pandas as pd
import numpy as np

customerData = {'ID': [0,1,2],
                'Name': ['Bob', 'John', 'Susan']}

vendorData = {'ID':[10,3,37],
                'Name':['Amazonian Books', 'The 13 Dwarves', 'Morningstar Bucks']}

purchaseData = {'cid': [0,0,2],
                'vid': [3,37,10],
                'cost': [1.0, 69.42, 9001.1]}

cData = pd.DataFrame(customerData)
vData = pd.DataFrame(vendorData)
pData = pd.DataFrame(purchaseData)

totals = pData.groupby('cid')['cost'].sum()
bigBuys = totals[totals == totals.max()]
bigBuyers = pd.merge(cData, bigBuys, left_on='ID', right_on='cid', how='right')[['ID', 'Name']]

print(totals.reset_index())