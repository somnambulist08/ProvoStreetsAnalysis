import datetime 
import csv
from holidaydetectors import blackoutdates

file = csv.reader(open('StreetProvo.csv',newline=''), delimiter=',')

#so for "just the facts maam" we need start, end, and distance.
#distance is field 115 in yards
#start is field 84 (Date Updated), end is field 112 (field verified)

inprogress = csv.writer(open('StreetsInProgress.csv','w'), delimiter=',')
complete = csv.writer(open('StreetsComplete.csv','w'), delimiter=',')

#write headers to both
f = next(file)

headers = f
headers.append('Rate of Completion')

complete.writerow(headers)
f.append('Estimated Percent Complete')
f.append('Estimated Date of Completion')
inprogress.writerow(f)


timeformat = '%m/%d/%Y %I:%M:%S %p'

globalrate=0
for row in file:
    if row[112] != '':
        distance = float(row[115]) * (3.0/5280.0) #miles completed
        start = datetime.datetime.strptime(row[84],timeformat)
        end = datetime.datetime.strptime(row[112],timeformat)
        #real workdays elapsed
        daysworked = blackoutdates(start.date(),end.date())
        row[116] = distance/daysworked
        globalrate = globalrate + distance/daysworked
        print(row[0])
        complete.writerow(row)
    else:
        row[116]=0
        row[117]=datetime.datetime(2000,1,1) #placeholders
        inprogress.writerow(row)

print(str(globalrate) + " miles per day")
        


