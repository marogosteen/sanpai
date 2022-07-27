import folium

data = []
with open("result/result.csv") as f:
    for line in f.readlines():
        line = line.split(",")
        data.append([line[0], float(line[1]), float(line[2])])

lats = [line[1] for line in data]
longs = [line[2] for line in data]
min_lat = min(lats)
min_long = min(longs)
max_lat = max(lats)
max_long = max(longs)
locs = [[line[1], line[2]] for line in data]

m = folium.Map(tiles='OpenStreetMap')
folium.PolyLine(
    locs, color="blue"
).add_to(m)

m.fit_bounds([[min_lat, min_long], [max_lat, max_long]])
m.save("map.html")
