import json
import pandas as pd

file = open('labs/recipes.txt', encoding='utf8')
data = json.load(file)

recipeNames = []
recipeIngredients = []

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

for recipe in data:
    recipeNames.append(recipe['name'])
    ingredientList = []
    for ingredient in recipe['ingredients']:
        ingredientList.append(ingredient['name'])
    recipeIngredients.append(ingredientList)

dataframe = pd.DataFrame({'recipeNames':recipeNames,
                            'ingredientList':recipeIngredients}).set_index('recipeNames')

print(dataframe)

allIngredients = set()

for ingredientList in dataframe['ingredientList']:
    allIngredients.update(ingredientList)

inverseData = {}

for ingredient in allIngredients:
    inverseData[ingredient] = set()

for recipeName in dataframe.index:
    ingredients = dataframe.loc[recipeName]
    for ingredient in ingredients:
        for i in ingredient:    # for some reason the data is double wrapped in a list
            inverseData[i].add(recipeName)

inverseDF = pd.DataFrame(index=inverseData.keys(),data={'recipes': inverseData.values()})

print(inverseDF)


# print(dataframe)