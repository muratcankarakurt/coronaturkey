#!/usr/bin/python

import requests
from flask import Flask, request, render_template

url = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&\
where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&\
orderByFields=Country_Region%20asc%2CProvince_State%20asc&outSR=102100&resultOffset=0&\
resultRecordCount=250&cacheHint=true"


def get_country_list():

    try:
        r = requests.get(url=url)
        result = r.json()["features"]
        return_list = {}
        for i in range(0,len(result)):
            if result[i]['attributes']['Province_State'] is None:
                return_list[str(result[i]['attributes']['Country_Region'])] = result[i]['attributes']
            else:
                return_list[str(result[i]['attributes']['Country_Region'] + "/" + result[i]['attributes']['Province_State'])] = result[i]['attributes']
    except Exception as e:
        print("Please enter a valid country name. Exception detail: " + e.message)

    return return_list


def get_turkey_only():

    try:
        r = requests.get(url=url)
        result = r.json()["features"]
        countrydata = {}
        for i in range(0, len(result)):
            if str(result[i]['attributes']['Country_Region']) == "Turkey":
                countrydata["TR"] = result[i]['attributes']
    except Exception as e:
        print(e)

    return countrydata


def get_details_by_country(country, region):

    try:
        r = requests.get(url=url)
        result = r.json()["features"]
        print(result)
        for i in range(0,len(result)):
            if str(result[i]['attributes']['Province_State']) == "" & str(result[i]['attributes']['Country_Region']) == str(country):
                return result[i]['attributes']
            elif str(result[i]['attributes']['Province_State']) == region:
                return result[i]['attributes']
    except Exception as e:
        print("Please enter a valid country or province name. Exception detail: " + str(e))


app = Flask(__name__)


@app.route("/")
def turkey():
    #return get_turkey_only()

    turkeydata = dict(get_turkey_only())
    vaka = str(turkeydata["TR"]["Confirmed"])
    olum = str(turkeydata["TR"]["Deaths"])
    iyi = str(turkeydata["TR"]["Recovered"])

    return render_template('index.html', vaka=vaka, olum=olum, iyi=iyi)


@app.route("/json")
def turkeyjson():
    return get_turkey_only()

'''
@app.route("/countryDetails")
def home():
    args = request.args
    countryName = str(args["country"])
    provinceName = str(args["province"])
    return get_details_by_country(str(countryName), str(provinceName))


@app.route("/countries")
def countrypage():
    return get_country_list()
'''

if __name__ == "__main__":
    app.run()
