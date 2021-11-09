import pandas as pd
import numpy as np
import requests
from lxml import html


pageContent1 = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29')
tree1 = html.fromstring(pageContent1.content)

countriesGDP = tree1.xpath('//div[1]/table[2]/tbody/tr/td[1]/a/text()')
for index, str in enumerate(countriesGDP):
    countriesGDP[index] = str[:-2]
estGDP = tree1.xpath('//div[1]/table[2]/tbody/tr/td[5]/text()')

# print(countriesGDP)
# print(estGDP)

pageContent2 = requests.get('https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population')
tree2 = html.fromstring(pageContent2.content)

countriesPop = tree2.xpath('//div[1]/table/tbody/tr/td[1]/a/text()')
population = tree2.xpath('//div[1]/table/tbody/tr/td[3]/text()')

# print(countriesPop)
# print(population)

gdpFrame = pd.DataFrame({'country': countriesGDP, 'estGDP': estGDP})
popFrame = pd.DataFrame({'country': countriesPop, 'population': population})

gdpFrame['estGDP'] = gdpFrame['estGDP'].apply(lambda s : int(s.replace(',','')))
popFrame['population'] = popFrame['population'].apply(lambda s : int(s.replace(',','')))

joined = pd.merge(gdpFrame, popFrame, on='country', how='inner')

print(joined['estGDP'].corr(joined['population']))

# print(joined)
