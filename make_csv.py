import random
import utm

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Stuff for Josie to change ###########################################################################################

GRANITE_NAME = "Granite X"
NUMBER_OF_COORDINATES = 20

# End of stuff for Josie to change ####################################################################################

output_filename = GRANITE_NAME + " quadrats.csv"

print("Trying to open '" + GRANITE_NAME + ".kml'...")
try:
    with open(GRANITE_NAME + ".kml", "r") as f:
        kml = f.read()
except Exception as e:
    print("ERROR: Check the 'GRANITE_NAME'")
    print(e)
print("Opened '" + GRANITE_NAME + ".kml' successfully")

if "<coordinates>" not in kml:
    print("ERROR: '" + GRANITE_NAME + ".kml' doesn't contain any coordinates")
    exit(1)
polygon_verticies_text = kml.split("<coordinates>")[1].split("</coordinates>")[0].strip()
polygon_verticies = polygon_verticies_text.split(" ")
print("'" + GRANITE_NAME + ".kml' was parsed successfully")

# Find the boundary
min_n = 99999999999999
max_n = 0
min_e = 99999999999999
max_e = 0

# Get the bounding polygon
formatted_verticies = []
for vertex in polygon_verticies:
    data = vertex.split(",")
    longitude = float(data[0])
    latitude = float(data[1])
    utm_e, utm_n, _, _ = utm.from_latlon(latitude, longitude)
    formatted_vertex = [utm_e, utm_n]
    formatted_verticies.append(formatted_vertex)

    # Check for new bounds
    if utm_n < min_n:
        min_n = utm_n
    if utm_n > max_n:
        max_n = utm_n
    if utm_e < min_e:
        min_e = utm_e
    if utm_e > max_e:
        max_e = utm_e

print("Found the bounding polygon for point validity checking")
print("Found the boundary for point generation:", min_n, max_n, min_e, max_e)

polygon = Polygon(formatted_verticies)

home_utm_e = round(min_e)
home_utm_n = round(min_n)

height = round(max_n - min_n)
width = round(max_e - min_e)

points = []
number_of_valid_coordinates = 0
while number_of_valid_coordinates < NUMBER_OF_COORDINATES:
    utm_e = home_utm_e + random.randint(0, width)
    utm_n = home_utm_n + random.randint(0, height)

    point = Point(utm_e, utm_n)
    if not polygon.contains(point):
        continue

    latitude, longitude = utm.to_latlon(utm_e, utm_n, 50, "H")

    points.append([str(latitude), str(longitude), str(int(utm_e)), str(int(utm_n))])
    number_of_valid_coordinates += 1

print("Successfully generated", NUMBER_OF_COORDINATES, "coordinates inside the bounding polygon defined by '" + GRANITE_NAME + ".kml'")

with open(output_filename, "w+") as f:
    f.write("Name,Latitude,Longitude,Northing,Easting\n")
    for i, point in enumerate(points):
        f.write(str(i+1) + "," + ",".join(point) + "\n")

print("Wrote output to '" + output_filename + "'")
print("Complete")