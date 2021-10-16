import pandas as pd
import numpy as np

"""
athleteEvents = pd.read_csv("athlete_events_test.csv").fillna(0)[["NOC", "Year", "Medal"]]
athleteEvents = athleteEvents[athleteEvents["Medal"] != 0]
athleteEvents = athleteEvents[athleteEvents["Year"] >= 1960]
nocGroup = athleteEvents.groupby("NOC")
yearCounts = nocGroup['Year'].value_counts()
yearCounts.name = "yearCount"
yearCounts = yearCounts.reset_index()

# nocRegions = pd.read_csv("noc_regions_test.csv")
popSize = pd.read_csv("population_size_test.csv")[["Country Code", "1960", "1964"]].set_index("Country Code")
popSize.columns = popSize.columns.map(lambda str: int(str))
popSize = popSize.stack().reset_index()
popSize.columns = ["NOC", "Year", "Population"]
popSize.name = "popSize"


print(yearCounts)
# print(nocRegions)
print(popSize)


# merged = yearCounts.merge(popSize, left_index = True, left_on = ["NOC"], right_on = ["Year"])
merged = yearCounts.merge(popSize, left_on = ["NOC", "Year"], right_on = ["NOC", "Year"])
# merged = yearCounts.join(popSize, on = ["NOC", "Year"])

print(merged)
# print(yearCounts["CHN"][1960])

"""

# athleteEventsTest = pd.read_csv("athlete_events_test.csv").fillna(0)
# athleteEventsTest = athleteEventsTest[athleteEventsTest["Medal"] != 0][["NOC", "Medal"]]
# nocRegionsTest = pd.read_csv("noc_regions_test.csv")[["NOC", "region"]]
# merged = pd.merge(nocRegionsTest, athleteEventsTest)
# print(merged)

# athleteEventsTest = pd.read_csv("athlete_events_test.csv").fillna(0)
# athleteEventsTest = athleteEventsTest[athleteEventsTest["Medal"] != 0][["ID", "Name", "Medal"]]
# medalCountsPerAthlete = athleteEventsTest["ID"].value_counts().to_frame()
# medalCountsPerAthlete["MedalCount"] = medalCountsPerAthlete["ID"]
# medalCountsPerAthlete["ID"] = medalCountsPerAthlete.index
# print(medalCountsPerAthlete)
# athleteEventsTest = athleteEventsTest.set_index("ID").drop_duplicates().reset_index()
# print(athleteEventsTest)
# merged = pd.merge(athleteEventsTest, medalCountsPerAthlete)
# print(merged)

# athleteEventsTest = pd.read_csv("athlete_events_test.csv").fillna(0)[["NOC", "Year", "Medal"]]
# athleteEventsTest = athleteEventsTest[athleteEventsTest["Medal"] != 0]
# athleteEventsTest = athleteEventsTest[athleteEventsTest["Year"] >= 1960]
# nocGroup = athleteEventsTest.groupby("NOC")
# yearCounts = nocGroup['Year'].value_counts().unstack()
# print(yearCounts)
# popSizeTest = pd.read_csv("population_size_test.csv")[["Country Code", "1992", "2012"]]
# print(popSizeTest)