import requests

file = requests.get("https://api.covidactnow.org/v2/counties.csv?apiKey=54fe6177c1854be7bee1b354304b2109")
ecd = file.encoding

with open('301finaldata', 'w+',encoding=ecd) as storeData:
    storeData.write(file.text)