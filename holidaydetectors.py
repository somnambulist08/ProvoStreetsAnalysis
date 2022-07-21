import datetime
import json
import requests

def xthydayofmonth(today,day,number): #takes Date, day(0 = Mon, 6 = Sun), number in month 1-5
    if day > 6 or day < 0 or number > 5: #out of range
        return False
    else:
        if (today.day - (7 * (number-1))) > 0 and (today.day - (7 * (number-1))) < 8:
            return True
        else:
            return False

def blackoutdates(start,end):
    span = int((end-start).days)
    for n in range(0,int((end-start).days)):
        today = start.day + n
        if today.weekday() == 6: #Sundays
            span = span-1
        else:
            spanold = span
            match today.month:
                case 1: #NYD/MLK
                    if today.day == 1 or (today.day == 2 and today.weekday() == 0):
                        span = span-1
                    else:
                        if xthydayofmonth(today,0,3):
                            span = span-1        
                case 2: #President's
                    if xthdayofmonth(today,0,3):
                        span = span-1
                case 5: #Memorial
                    if today.weekday() == 0 and today.day >=25:
                        span = span-1
                case 6: #Juneteenth
                    if today.day == 19 or (today.day == 20 and today.weekday() == 0):
                        span = span-1
                case 7: #Independance/Pioneer
                    if today.day == 4 or (today.day == 5 and today.weekday() == 0):
                        span = span-1
                    elif today.day == 24 or (today.day == 25 and today.weekday() == 0):
                        span = span-1
                case 9: #Labor
                    if xthydayofmonth(today,0,1):
                        span = span-1
                case 10: #Columbus
                    if xthydayofmonth(today,0,2):
                        span = span-1
                case 11: #Veterans/Thanksgiving
                    if xthydayofmonth(today,3,3):
                        span = span-1
                    elif today.day == 11 or (today.day == 12 and today.weekday() == 0):
                        span = span-1
                case 12: #Christmas
                    if today.day == 25 or (today.day == 26 and today.weekday() == 0):
                        span = span-1
                    elif today.day == 31 and today.weekday() == 4:
                        span = span-1
            if spanold == span: #check for weather
                temp = gettemp(today)
                if temp<32 or temp >95 :#32F is too cold, 95F is too hot
                    span = span-1
    return span


def gettemp(day): #Gets the measured temp from NOAA's provo station on given day
    url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TOBS&stationid=GHCND:USC00427064&units=standard'
    token = {'token': 'GThBfAlDCLbufAjUwCwChyWGIKKwGltF'}
    daterange = {'startdate':day.isoformat(),'enddate':day.isoformat()}
    r = requests.get(url,headers=token,params=daterange)
    out = r.json()['results'][-1]
    return out['value']
    
    




            
