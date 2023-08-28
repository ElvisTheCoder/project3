from flask import Flask, render_template, jsonify

#Load From the Database file that I created. It is in this same directory
from database import LoadHousingData
from database import LoadInterestData

App = Flask(__name__)

#Route to produce your main home page. 
#Feel free to add additional HTML routes to add additional pages


#This is the main data route, it will produce JSON for your javascript to use
#You will wind up calling into it using d3.json("/LoadData/1") to get period 1
@App.route("/LoadHousingData")

def LoadData(): 
    returneddata = LoadHousingData()

    #Produce a JSON object (aka a list of python dictionaries
    HomePriceList = []
    for index,row in returneddata.iterrows(): 
            HomePriceList.append({
            "id" : row['id'], 
            "city" : row['city'],
            "Year": row['Year'],
            "Value": row['Value'],
            "% Change": row['percentagechange']})
    #Return the JSON that you created
    return jsonify(HomePriceList)

@App.route("/LoadInterestRates")

def LoadData2(): 

    returneddata = LoadInterestData()

    #Produce a JSON object (aka a list of python dictionaries
    InterestList = []
    for index,interest_row in returneddata.iterrows(): 
            InterestList.append({
            "id": interest_row['id'],
            "year": interest_row['year'],
            "Interest_Rates": interest_row['Interest_Rates']})
    #Return the JSON that you created
    return jsonify(InterestList)


if __name__ == "__main__":
     App.run(debug=True)