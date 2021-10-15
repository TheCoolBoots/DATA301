from numpy.core.numeric import NaN
import pandas as pd

class lab2():
    def __init__(self):
        self.athleteEvents = pd.read_csv("athlete_events.csv")
        # self.nocRegions = pd.read_csv("noc_regions.csv")
        # self.nocRegions = dict(self.nocRegions[["NOC", "region"]].values)

        # self.tester()
        # self.q2()
        # self.q3()
        # self.q4()
        self.q5()

    def tester(self):
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

        pass

    # def q2(self):
    #     golds = self.athleteEvents[self.athleteEvents["Medal"] == "Gold"][["NOC", "Medal"]]
    #     golds["NOC"] = golds["NOC"].map(lambda noc: self.nocRegions[noc])
    #     golds = golds["NOC"].value_counts()
    #     print(golds)

    def q2(self):
        golds = self.athleteEvents[self.athleteEvents["Medal"] == "Gold"][["NOC", "Medal"]]
        nocRegions = pd.read_csv("noc_regions.csv")[["NOC", "region"]]
        merged = pd.merge(golds, nocRegions)
        print(merged["region"].value_counts())


    def q3(self):
        golds = self.athleteEvents[self.athleteEvents["Medal"] == "Gold"][["ID", "Name"]]
        medalCountsPerAthlete = golds["ID"].value_counts().to_frame()
        medalCountsPerAthlete["MedalCount"] = medalCountsPerAthlete["ID"]
        medalCountsPerAthlete["ID"] = medalCountsPerAthlete.index
        golds = golds.set_index("ID").drop_duplicates().reset_index()
        merged = pd.merge(golds, medalCountsPerAthlete)
        print(merged.sort_values(by = "MedalCount", ascending = False))


    def q4(self):
        medals = self.athleteEvents.fillna(0)
        medals = medals[medals["Medal"] != 0]
        medals = medals[medals["Height"] > 0][["ID", "Name", "Height"]]
        medalCountsPerAthlete = medals["ID"].value_counts().to_frame()
        medalCountsPerAthlete["MedalCount"] = medalCountsPerAthlete["ID"]
        medalCountsPerAthlete["ID"] = medalCountsPerAthlete.index
        medals = medals.set_index("ID").drop_duplicates().reset_index()
        merged = pd.merge(medals, medalCountsPerAthlete)

        # print(merged)
        print(merged["MedalCount"].corr(merged["Height"]))


    def q5(self):
        athleteEvents = pd.read_csv("athlete_events.csv").fillna(0)[["NOC", "Year", "Medal"]]
        athleteEvents = athleteEvents[athleteEvents["Medal"] != 0]
        athleteEvents = athleteEvents[athleteEvents["Year"] >= 1960]
        print(athleteEvents.head(20))
        nocGroup = athleteEvents.groupby("NOC")
        yearCounts = nocGroup['Year'].value_counts().fillna(0)
        yearCounts.columns = ['MedalCount']
        yearCounts.name = "MedalCount"
        yearCounts = yearCounts.reset_index()


        # print(yearCounts)
        popSize = pd.read_csv("population_size.csv").drop(columns=["Country Name","Indicator Name","Indicator Code"])
        popSize = popSize.rename(columns = {"Country Code": "NOC"}).set_index("NOC").stack()
        popSize.name = "popSize"
        popSize = popSize.reset_index()
        # print(popSize)

        print(yearCounts.head(30))
        # print('\n')
        print(popSize.head(30))

        #print(yearCounts[["NOC", 1960]].set_index("NOC")[1960])
        #print(popSize[["NOC", "1960"]].set_index("NOC")["1960"])


        

        

    def getYearlyCalculation(self, country, yearlyPop, medalsPerCountry):
        pass


    

lab2instance = lab2()