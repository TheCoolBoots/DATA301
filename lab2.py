from numpy.core.numeric import NaN
import pandas as pd

class lab2():
    def __init__(self):
        self.athleteEvents = pd.read_csv("athlete_events.csv")
        self.nocRegions = pd.read_csv("noc_regions.csv")
        self.nocRegionsDict = dict(self.nocRegions[["NOC", "region"]].values)

        self.q2()
        # self.q3()
        # self.q4()
        # self.q5()

    def q2(self):
        golds = self.athleteEvents[self.athleteEvents["Medal"] == "Gold"][["NOC", "Medal"]]
        # golds["NOC"] = golds["NOC"].map(lambda noc: self.nocRegions[noc])
        golds = golds["NOC"].value_counts()
        print(golds)

    def q3(self):
        golds = self.athleteEvents[self.athleteEvents["Medal"] == "Gold"][["ID", "Name", "Medal"]]
        idCounts = golds["ID"].value_counts(sort = False)
        golds = golds.drop_duplicates()
        golds["Medal"] = golds["ID"].map(lambda id : idCounts.loc[id])
        print(golds.sort_values(by = "Medal", ascending = False))

    def q4(self):

        # fill all na's with 0's
        medals = self.athleteEvents.fillna(0)

        # remove all entries that didnt result in a medal won
        medals = medals[medals["Medal"] != 0]
        # print(medals[["ID", "Height", "Medal"]])

        # remove all entries that have 0 height
        medals = medals[medals["Height"] > 0][["ID", "Height"]]
        # print(medals)

        # count the number of medals each athlete has won
        medalCount = medals["ID"].value_counts()

        # change dataframe to have only one entry per athlete
        medals = medals.set_index("ID").drop_duplicates()

        # map the medal count to each athlete ID
        medals["MedalCount"] = medals.index.map(lambda id : medalCount.loc[id])
        
        # print(medals)
        print(medals["MedalCount"].corr(medals["Height"]))

    def q5(self):


        # import population_size.csv
        yearlyPopulation = pd.read_csv("population_size.csv").drop(columns=["Country Name","Indicator Name","Indicator Code"]).fillna(0)
        yearlyPopulation.set_index("Country Code", inplace = True)
        print(yearlyPopulation)


        # strip out all non-medal entries, isolate year and NOC columns
        medalsPerYearPerCountry = self.athleteEvents.fillna(0)[self.athleteEvents["Medal"] != 0][["NOC", "Year"]]

        # count the number of medals won by each country each year
            # create dataframe with indexes and column labels same as yearly population
            # fill all data with 0's
            # for each element in medalsPerYearPerCountry
            # increment [NOC, Year] by 1

        # get list of all NOC's

        # for each column of yearly population and medals won per year, get correlation


    def getYearlyCalculation(self, country, yearlyPop, medalsPerCountry):
        pass


    

lab2instance = lab2()