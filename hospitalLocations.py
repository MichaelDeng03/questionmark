import pandas as pd
import geopandas as gpd
import googlemaps
from datetime import datetime
from census import Census
from us import states
gmaps = googlemaps.Client(key='AIzaSyCejRRc9OZq1slvtfsjZsbV69O3NXlD06A')

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

hospitals = pd.read_csv('allHospitals.csv')
citiesPop = pd.read_csv('allCityPopulations.csv')
citiesPop = citiesPop[['City', 'State', 'Population','lats2', 'long2']]

def get_data(state):
    # change below according to user input
    # state = "California" 
    hospitals_state = hospitals[hospitals["State"] == us_state_to_abbrev[state]] 
    
    citiesPop_state = citiesPop[citiesPop["State"] == state]
    # end of changes bc user endpoint

    citiesPop_state['City'] = [" ".join(val[::-1].split(' ',1)[1:])[::-1] for val in citiesPop_state['City'].values]
    hospitals_state['City'] = [val.lower().capitalize() for val in hospitals_state['City'].values]
    noaccess = []
    for ind in citiesPop_state.index:
        city = citiesPop_state['City'][ind]
        df1 = hospitals_state[hospitals_state['City']==city]
        s=df1['numPeople'].sum()
        noaccess.append(citiesPop_state['Population'][ind]-s)
    result = citiesPop_state.merge(hospitals_state,left_on = ['City'], right_on = ['City'], how='left')

    result = result[["City", "lats2", "long2", "Population"]]
    result = result.drop_duplicates()
    result['NoAccess'] = noaccess
    return result

