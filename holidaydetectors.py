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
    print("checking between " + str(start.isoformat())+" and "+str(end.isoformat()))
    span = int((end-start).days)
    yearsflag=False
    if span <365:
        temps=gettemp(start,end)
    else: #only one year of data per query so dice it up
        yearsflag=True
        years = int(span/365)
        temps={}
        temps[0]=gettemp(start,start+datetime.timedelta(days=365))
        nxtyear=start+datetime.timedelta(days=366)
        for n in range(1,years):
            temps[n] = gettemp(nxtyear,nxtyear+datetime.timedelta(days=364))
            nxtyear=nxtyear+datetime.timedelta(days=365)
            print(len(temps[n]['results']))
        temps[years]=gettemp(nxtyear,end)      
    for n in range(0,int((end-start).days)):
        today = start + datetime.timedelta(days=n)
        if today.weekday() == 6: #Sundays
            span = span-1
        else:
            spanold = span
            match today.month:
                case 1: #NYD/MLK
                    if today.day == 1 or (today.day == 2 and today.weekday() == 0) or xthydayofmonth(today,0,3):
                        span = span-1
                case 2: #President's
                    if xthydayofmonth(today,0,3):
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
                    if today.day == 11 or (today.day == 12 and today.weekday() == 0):
                        span = span-1
                    elif xthydayofmonth(today,3,3):
                        span = span-1
                case 12: #Christmas
                    if today.day == 25 or (today.day == 26 and today.weekday() == 0):
                        span = span-1
                    elif today.day == 31 and today.weekday() == 4:
                        span = span-1
            if spanold == span: #if it's not sunday or a holiday, check the weather
                print("checking temp on "+str(today))
                if yearsflag:
                    yearindex=int(n/365)
                    todaystemp=temps[yearindex]['results'][n%365]['value']
                else:
                    todaystemp=temps['results'][n]['value']
                print("it was "+str(todaystemp)+" deg")
                if todaystemp<32 or todaystemp >95 :#32F is too cold, 95F is too hot
                    span = span-1
    return span


def gettemp(start,end): #Gets the measured temp from NOAA's station in Provo, from date start to date endget
    #start=datetime.datetime(start.year,start.month,start.day)
    #end=datetime.datetime(end.year,end.month,end.day)
    url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TOBS&stationid=GHCND:USC00427064&units=standard'
    token = {'token': 'wFsLkUJAIGqtIxSftgJdTgVGgONIhmlp'}
    daterange = {'startdate':start.isoformat(),'enddate':end.isoformat()}
    print(daterange)
    r = requests.get(url,headers=token,params=daterange)
    out = r.json()
    z = json.dumps(out)
    results = json.loads(z)
    return results


start = datetime.datetime(2019,6,13)    
end = datetime.datetime(2022,6,28)
blackoutdates(start,end)




            
