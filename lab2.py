from numpy.core.numeric import NaN
import pandas as pd

class lab2():
    def __init__(self):
        self.athleteEvents = pd.read_csv("athlete_events.csv")
        # self.nocRegions = pd.read_csv("noc_regions.csv")
        # self.nocRegions = dict(self.nocRegions[["NOC", "region"]].values)

        # self.tester()
        print("\n==============Q2================")
        self.q2()
        print("\n==============Q3================")
        self.q3()
        print("\n==============Q4================")
        self.q4()
        print("\n==============Q5================")
        self.q5()
        print("\n==============Q6================")
        self.q6()


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
        print(merged["MedalCount"].corr(merged["Height"]))


    def q5(self):
        athleteEvents = pd.read_csv("athlete_events.csv").fillna(0)[["NOC", "Year", "Medal"]]
        athleteEvents = athleteEvents[athleteEvents["Medal"] != 0]
        athleteEvents = athleteEvents[athleteEvents["Year"] >= 1960]
        nocGroup = athleteEvents.groupby("NOC")
        yearCounts = nocGroup['Year'].value_counts()
        yearCounts.name = "yearCount"
        yearCounts = yearCounts.reset_index()

        years = yearCounts["Year"].drop_duplicates()

        popSize = pd.read_csv("population_size.csv").drop(columns=["Country Name","Indicator Name","Indicator Code"]).set_index("Country Code")
        popSize.dropna(how='all', axis='columns',inplace=True)
        popSize.columns = popSize.columns.map(lambda str: int(str))
        popSize = popSize.stack().reset_index()
        popSize.columns = ["NOC", "Year", "Population"]
        popSize.name = "popSize"

        merged = yearCounts.merge(popSize, left_on = ["Year", "NOC"], right_on = ["Year", "NOC"])

        tmp = merged["Year"]
        merged["Year"] = merged["NOC"]
        merged["NOC"] = tmp
        merged.columns = ["Year", "NOC", "YearCount", "Population"] 

        merged.set_index(["Year", "NOC"], inplace = True)
        
        output = pd.DataFrame()
        output["Year"] = years
        output["Correlation"] = output["Year"].map(lambda year: merged.loc[year][:]["YearCount"].corr(merged.loc[year][:]["Population"]))
        print(output.sort_values(by = "Year"))


    def q6(self):
        athleteEvents = pd.read_csv("athlete_events.csv").fillna(0)[["NOC", "Medal"]]
        athleteEvents = athleteEvents[athleteEvents["Medal"] != 0]
        medals = athleteEvents.groupby("NOC").count()
        # print(medals.head(10))
        gdp = pd.read_csv("gdp.csv").drop(columns="Country Name")
        gdp.columns = ["NOC","Year", "Value"]
        avgGDP = gdp.groupby("NOC")["Value"].mean()
        # print(avgGDP.head(10))
        merged = pd.merge(medals, avgGDP, how = "inner", on = "NOC")
        print(merged["Medal"].corr(merged["Value"]))


lab2instance = lab2()