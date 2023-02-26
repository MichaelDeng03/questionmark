import gmplot
import bs4

apikey = 'AIzaSyCejRRc9OZq1slvtfsjZsbV69O3NXlD06A'
center_lat = 37.766956
center_lng = -122.448481
zoom = 14


def init_map(center_lat=center_lat, center_lng=center_lng, zoom=zoom, apikey=apikey, title = 'Hospital/City Locations'):
    '''
    Input: Takes in a tuple of lats/longs, zoom level, and apikey
    Output: Returns a GoogleMapPlotter object
    '''
    return gmplot.GoogleMapPlotter(center_lat, center_lng, zoom, apikey=apikey, title = title)


def draw_points(g_map:gmplot.GoogleMapPlotter, lats, longs, color='red', size=40, opacity=0.8):
    '''
    Input: Takes input of a tuple of lats/longs
    Output: Draws a scatter plot of points
    '''
    g_map.scatter(lats, longs, color=color, size=size,
                 marker=False, alpha=opacity)


def add_input_fields():
    '''
    Input: None
    Output: Adds input fields to the map. Do this after drawing the initial map
    '''
    with open('index.html') as f:
        html_txt = f.read()
        soup = bs4.BeautifulSoup(html_txt, features='lxml')
        soup.find("div", {"id": "map_canvas"})[
            'style'] = "width: 80%; height: 92%;"

    # save the file again
    with open("index.html", "w") as outf:
        outf.write(str(soup))

    # idk how bs4 works: i add input form here
    lines = []
    with open('index.html', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if '<div id="map_canvas" style="width: ' in line:
                lines.insert(i + 1, '<form action="input" method="POST">\n')
                lines.insert(i + 2, '<div id = submit_body>\n ')
                lines.insert(
                    i + 3, '  <label for="num_hospitals">Number of Hospitals:</label>\n')
                lines.insert(
                    i + 4, '  <input type="text" id="num_hospitals" name="num_hospitals"<br>\n')
                lines.insert(
                    i + 5, '  <label for="state">State:</label>\n')
                lines.insert(
                    i + 6, '  <input type="text" id="state" name="state"><br>\n')
                lines.insert(
                    i + 7, '  <input type="submit" value="Submit">\n')
                lines.insert(
                    i + 8, '</div>\n'
                )
                lines.insert(
                    i + 9, '</form>\n')
                break

    with open('index.html', 'w') as f:
        f.write(' '.join(lines))


# attractions_lats, attractions_lngs = zip(*[
#     (37.769901, -122.498331),
#     (37.768645, -122.475328),
#     (37.771478, -122.468677),
#     (37.769867, -122.466102),
#     (37.767187, -122.467496),
#     (37.770104, -122.470436)
# ])

# attractions_lats2, attractions_lngs2 = zip(*[
#     (37.759901, -122.498331),
#     (37.758645, -122.475328),
#     (37.761478, -122.468677),
#     (37.759867, -122.466102),
#     (37.757187, -122.467496),
#     (37.760104, -122.470436)
# ])


gmap = init_map()
# draw_points(attractions_lats, attractions_lngs,
#             color='red', size=40, opacity=0.8)
# draw_points(attractions_lats2, attractions_lngs2,
#             color='blue', size=40, opacity=0.8)
# gmap.draw("index.html")

# add_input_fields()

