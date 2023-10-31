from datetime import datetime, timedelta
from time import sleep
from os import system, name, path
from requests import api, get
import json


def writeData(fileName):
    with open(fileName, 'w') as f:
        data = str(getData(get_location_info()))
        data = data.replace('\'', '\"')
        f.write(data)


def getData(locationInfo):
    data = api.get(f'http://api.aladhan.com/v1/timingsByCity?city={locationInfo[0]}&country={locationInfo[1]}&method=4').json()

    filterTimes = ['Sunset', 'Imsak', 'Midnight', 'Firstthird', 'Lastthird']
    prayTimes = data['data']['timings']
    filteredPrayTimes = {}
    # filteredPrayTimes = {            
    #             "Fajr": ["03:57", 25],
    #             "Sunrise": ["05:46", 0],
    #             "Dhuhr": ["12:59", 20], 
    #             "Asr": ["16:55", 20],
    #             "Maghrib": ["20:12", 10],
    #             "Isha": ["22:02", 20],
    #             }

    for i, v in prayTimes.items():
        if i not in filterTimes:
            filteredPrayTimes[i] = [v]

    # adding igamh time
    filteredPrayTimes['Fajr'].append(25)
    filteredPrayTimes['Sunrise'].append(0)              
    filteredPrayTimes['Dhuhr'].append(20)   
    filteredPrayTimes['Asr'].append(20)        
    filteredPrayTimes['Maghrib'].append(10)        
    filteredPrayTimes['Isha'].append(20)

    return filteredPrayTimes


def findDelta(pray_igamh_times, currentTime):
    prayTime = datetime.strptime(pray_igamh_times[0] + ':00', '%H:%M:%S')

    prayTime = timedelta(hours=prayTime.hour,
                    minutes=prayTime.minute,
                    seconds=prayTime.second)

    currentTime = timedelta(hours=currentTime.hour,
                    minutes=currentTime.minute,
                    seconds=currentTime.second)
    
    timeRemain = prayTime - currentTime

    if currentTime >= prayTime:
        timePassed = currentTime - prayTime
        igamh = timedelta(minutes=pray_igamh_times[1])

        if currentTime >= prayTime + igamh:
            return f'{timePassed} - passed'
        
        return f'{timePassed} - Igamh time is - {prayTime + igamh - currentTime}'
    
    return timeRemain


def displayTimes(data):
    location = get_location_info()
    system('cls' if name=='nt' else 'clear')
    while 1:
        currentTime = datetime.now().time()
        print(location)

        for prayName, pray_igamh_times in data.items():
            print(f'{prayName}\t{findDelta(pray_igamh_times, currentTime)}')

        sleep(1)
        system('cls' if name=='nt' else 'clear')  


def get_location_info():
    try:
        response = get("https://ipinfo.io")
        data = response.json()

        city = data.get("city", "Unknown")
        country = data.get("country", "Unknown")

        return city, country

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def check_date():
    isOld = False
    with open('currentDate.txt', 'r') as f:
        date = str(datetime.now().date())
        cur = f.read()
        if cur != date:
            isOld = True
        
    return isOld

if not path.isfile('currentDate.txt'):
    open('currentDate.txt', 'x').close()

if not path.isfile('prayTimes.txt'):
    open('prayTimes.txt', 'x').close()


if check_date():
    with open('currentDate.txt', 'w') as f:
        date = str(datetime.now().date())
        f.write(date)
        writeData('prayTimes.txt')


prayTimes = None

with open('prayTimes.txt', 'r') as f:
    prayTimes = json.loads(f.readline())


displayTimes(prayTimes)

