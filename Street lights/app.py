import re
from convertbng.util import convert_lonlat

file = open("data.txt", "r")

data = re.split("\n", file.read())

file.close()


eastings = []
northings = []

for i in range(1, len(data)):
    row = re.split(r'\t', data[i])

    eastings.append(float(row[4]))
    northings.append(float(row[5]))

coordinates = convert_lonlat(eastings, northings)


file = open('query-0.txt', "w")
file.write('insert into newstreetlights (assetid, sitename, plotno, featureid, location, type, primmeasure, centroide, centroidn, sitecode, featuregp, latitude, longitude, GeoLoc) values\n')

for i in range(1, len(data)):
    if (i % 1000 == 0):
        if (i % 10000 == 0):
            file.close()
            file = open('query-' + str(i//10000) + '.txt', "w")
        file.write('insert into newstreetlights (assetid, sitename, plotno, featureid, location, type, primmeasure, centroide, centroidn, sitecode, featuregp, latitude, longitude, GeoLoc) values\n')
        
    row = re.split(r'\t', data[i])

    row[1] = row[1].replace("\'", "\'\'").replace(u'\u201c', '\'\'').replace(u'\u201d', '\'\'').replace(u'\u2018', '\'\'').replace(u'\u2019', '\'\'')
    row[3] = row[3].replace("\'", "\'\'").replace(u'\u201c', '\'\'').replace(u'\u201d', '\'\'').replace(u'\u2018', '\'\'').replace(u'\u2019', '\'\'')

    geography = 'point(' + str(coordinates[0][i - 1]) +  ' ' + str(coordinates[1][i - 1]) + ')'
    
    if (row[4] == '0' or row[5] == '0'):
        coordinates[0][i - 1] = 0
        coordinates[1][i - 1] = 0
        geography = 'null'

    file.write('(\'' + row[11] + '\', \'' + row[1] + '\', \'' + row[6] + '\', \'' + row[2] + '\', \'' + row[3] + '\', \'' + row[7] + '\', 0, \'' + row[4] + '\', \'' + row[5] + '\', \'' + row[0] + '\', \'' + row[8] + '\', \'' + str(coordinates[1][i - 1]) + '\', \'' + str(coordinates[0][i - 1]) + '\', \'' + geography + '\')')
    if ((i + 1) % 1000 != 0):
        file.write(',')
    file.write('\n')

file.close()