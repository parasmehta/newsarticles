import folium                                                                                                           # import folium: for anaconda: conda config --add channels conda-forge --> conda install folium
import csv

list = []

print("\nCorrecting format of geometry (lat <--> lon)...")

input = open('london_articles_tagged.txt', 'rb')
for row in csv.reader(input):

    coords = str(row[3]).replace('LINESTRING(','').replace(')','')                                                      # switch langitude - longitude
    coords = coords.split(",")                                                                                          # |
    coordinates = []                                                                                                    # |
    for coord in coords:                                                                                                # |
        coord = coord.split(" ")                                                                                        # |
        coord = [float(coord[1]), float(coord[0])]                                                                      # |
        coordinates.append(coord)                                                                                       # |
    list.append(coordinates)                                                                                            # save all coordinates in a list

input.close()

print("...done.\n")

listlength = len(list)
print("Number of entries: " + str(listlength))

importance = []
for i in range(0,listlength,1):
    if not (list[i] in (x[1] for x in importance)):
        importance.append([list.count(list[i]),list[i]])

print("Number of distinct entries: " + str(len(importance)))

importance.sort()
print (importance[0][0],importance[len(importance)-1][0])


map_osm = folium.Map(location=[51.5073, -0.1277])                                                                       # create a map object centered on london
for line in importance:
    if line[0] <= 100:
        pl = folium.PolyLine(locations=line[1],weight=10, color='yellow')                                               # 60% red
    elif line[0] <= 500:
        pl = folium.PolyLine(locations=line[1], weight=10, color='orange')                                              # 40% red
    else:
        pl = folium.PolyLine(locations=line[1], weight=10, color='red')                                                 # 20% red
    map_osm.add_children(pl)
map_osm.save('london_map.html')                                                                                         # create a .html file for the map

print("Map generated. See london_map.html")
