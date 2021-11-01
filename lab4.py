import pandas as pd
import numpy as np
import requests
from lxml import html


pageContent1 = requests.get('https://en.wikipedia.org/wiki/List_of_sovereign_states')
tree1 = html.fromstring(pageContent1.content)
# commonAndFormalNames = tree1.xpath('//table[1]/tbody/tr[3]/td[0]/b[1]/a[1]/text()')
afganistan = tree1.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[4]/td[1]/b/a/text()')

print(afganistan)

# pageContent=requests.get('https://en.wikipedia.org/wiki/List_of_Olympic_medalists_in_judo')
# tree = html.fromstring(pageContent.content)
# gold=tree.xpath('//table[1]/tbody/tr[@valign="top"]/td[2]/a[1]/text()')
# silver=tree.xpath('//table[1]/tbody/tr[@valign="top"]/td[3]/a[1]/text()')
# bronze1=tree.xpath('//table[1]/tbody/tr[@valign="top"]/td[4]/a[1]/text()')
# bronze2=tree.xpath('//table[1]/tbody/tr[not(@valign="top")]/td[1]/a[1]/text()')
# games=tree.xpath('//table[1]/tbody/tr[@valign="top"]/td[1]/a[1]/text()')
# df=pd.DataFrame({'games':games,'gold':gold,'silver':silver,'bronze1':bronze1,'bronze2':bronze2})
# df=df.set_index('games')
# print(df)
