import re

def toDate(str):
    list = str.split('/')
    try:
        return list[1]+"-"+list[0]+"-"+list[2]
    except:
        return ''

def toBit(str):
    if (str == 'yes'):
        return '1'
    elif (str == 'no'):
        return '0'
    else:
        return 'null'

file = open("data.txt", "r", encoding = "ISO-8859-1")

data = re.split("\n", file.read())

file.close()

file = open('query-0.txt', "w")
file.write('insert into newServiceRollOutAddresses (uprn, Address1, Address2, Street, Locality, Town, PostCode, Ward, USRN, New_Rec_Round, New_Day, New_Recycling_Week, Assisted, Start_Date, End_Date, First_new_service_collection_date , Exception_Property, Proposed_Service, Service_Literature, Communal_No_of_bins_needed) values\n')

for i in range(1, len(data)):
    if (i % 1000 == 0):
        if (i % 10000 == 0):
            file.close()
            file = open('query-' + str(i//10000) + '.txt', "w")
        file.write('insert into newServiceRollOutAddresses (uprn, Address1, Address2, Street, Locality, Town, PostCode, Ward, USRN, New_Rec_Round, New_Day, New_Recycling_Week, Assisted, Start_Date, End_Date, First_new_service_collection_date , Exception_Property, Proposed_Service, Service_Literature, Communal_No_of_bins_needed) values\n')
        
    row = re.split(r'\t', data[i])

    string = '('

    for a in range(0, len(row)):
        row[a] = row[a].replace("\'", "\'\'").replace(u'\u201c', '\'\'').replace(u'\u201d', '\'\'').replace(u'\u2018', '\'\'').replace(u'\u2019', '\'\'')

        if (a >= 13 and a <= 15):
            row[a] = toDate(row[a])
        elif (a == 16):
            row[a] = toBit(row[a])

        if (a == 16):
            string += row[a]
        else:
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