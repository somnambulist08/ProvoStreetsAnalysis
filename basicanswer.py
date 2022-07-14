import datetime 
import csv

file = csv.reader(open(r"C:\Users\somnambulist\Desktop\testerino\StreetProvo.csv",newline=''), delimiter=',')

#so for "just the facts maam" we need start, end, and distance.
#distance is field 115 in yards
#start is field 84 (Date Updated), end is field 112 (field verified)

#skip the first line, full of labels 
f = next(file)

timeformat = '%m/%d/%Y %I:%M:%S %p'

rate=0
for row in file:
    if row[112] != '':
        distance = float(row[115]) * (3.0/5280.0) #miles completed
        start = datetime.datetime.strptime(row[84],timeformat)
        end = datetime.datetime.strptime(row[112],timeformat)
        rate = rate + distance/(end.date()-start.date()).days

print(str(rate) + " miles per day")
        
    
    

