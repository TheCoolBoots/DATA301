import json

file = open('recipes1.txt')
data = json.load(file)

"""
recipes:
    name
    ingredients
        quantity
        name
        type
    steps
    timers
    imageurl
    originalurl
"""

print(data['name'])