import folium                                                                                                           # import folium: for anaconda: conda config --add channels conda-forge --> conda install folium

map_osm = folium.Map(location=[51.5073, -0.1277])                                                                       # create a map object centered on london
map_osm.create_map(path='london_map.html')                                                                              # create a .html file for the map

