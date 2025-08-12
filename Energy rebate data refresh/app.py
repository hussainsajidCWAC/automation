import re

file = open("data.txt", "r")

data = re.split("\n", file.read())

file.close()

file = open('query-0.txt', "w")
file.write('insert into energyrebate3 (ACCOUNT_REF, PROPERTY_REF, PROP_POSTCODE) values\n')

for i in range(1, len(data)):
    if (i % 1000 == 0):
        if (i % 10000 == 0):
            file.close()
            file = open('query-' + str(i//10000) + '.txt', "w")
        file.write('insert into energyrebate3 (ACCOUNT_REF, PROPERTY_REF, PROP_POSTCODE) values\n')
        
    row = re.split(r'\t', data[i])

    string = '('

    for a in range(0, len(row)):
        if (a == 0 or a == 3 or a == 8):
            row[a] = row[a].replace("\'", "\'\'").replace(u'\u201c', '\'\'').replace(u'\u201d', '\'\'').replace(u'\u2018', '\'\'').replace(u'\u2019', '\'\'')
            string += '\'' + row[a] + '\''

            if (a != len(row) - 1):
                string += ','
    
    string += ')'

    if ((i + 1) % 1000 != 0):
        string += ','
    
    string += '\n'

    if (len(string) >= 10):
        file.write(string)

file.close()