from flask import Flask, request, jsonify
from html_js_generator import *
import numpy as np
from kmeans import kmeans
import pandas as pd
from hospitalLocations import get_data
import googlemaps

app = Flask(__name__)
apikey = 'AIzaSyCejRRc9OZq1slvtfsjZsbV69O3NXlD06A'
center_lat = 39
center_lng = -96 
zoom = 5


@app.route('/')
def home():
    gmap = init_map(center_lat, center_lng, zoom, apikey, title = 'Hospital/City Locations')

    gmap.draw("index.html")
    add_input_fields()

    with open("index.html") as f:
        html = f.read()

    return html


@app.route('/input', methods=["GET", "POST"])
def test():
    if request.method == "POST":
        # temporary cast to tuple for testing
        num_hospitals = int(request.form["num_hospitals"])
        state = request.form["state"]

        df = get_data(state)
        df =df.rename(columns = {'lats2' : 'latitude', 'long2' : 'longitude', 'NoAccess' : 'population'})
        hospital, coords = kmeans.run_kmeans(num_hospitals, df)
        lngs, lats, h_lngs, h_lats = [], [], [], []
        for coord in coords:
            lngs.append(coord[0])
            lats.append(coord[1])
        lngs, lats = tuple(lngs), tuple(lats)
        for hospital_coord in hospital:
            h_lngs.append(hospital_coord[0])
            h_lats.append(hospital_coord[1])
        h_lngs, h_lats = tuple(h_lngs), tuple(h_lats)
        
        gmaps = googlemaps.Client(apikey)
        geocode_result = gmaps.geocode(state)
        lat = geocode_result[0]['geometry']['location']['lat']
        long = geocode_result[0]['geometry']['location']['lng']

        gmap = init_map(lat, long, zoom=8.8, title ='Hospital/City Locations')
        draw_points(gmap, lats, lngs,
                color='red', size=1000, opacity=0.8)
        draw_points(gmap, h_lats, h_lngs, color = 'blue', size = 5000, opacity = 0.8)
        gmap.draw('index.html')

        with open("index.html") as f:
            html = f.read()
        return html


if __name__ == '__main__':
    # don't change this line!
    app.run(host="0.0.0.0", debug=True, threaded=False)

