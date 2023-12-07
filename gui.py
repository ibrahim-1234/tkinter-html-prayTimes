from datetime import datetime, timedelta
from requests import api, get
import customtkinter as tk


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


data = getData(get_location_info())


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


def displayTimes():
    currentTime = datetime.now().time()
    text = ''
    for prayName, pray_igamh_times in data.items():
        text += f'{prayName}\t{findDelta(pray_igamh_times, currentTime)}\n'

    prayTimes.configure(text=text)
    app.after(1000, displayTimes)
    

app = tk.CTk()

prayTimes = tk.CTkLabel(app, font=('consolas', 26))
prayTimes.pack()

displayTimes()
app.mainloop()
