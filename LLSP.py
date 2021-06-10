import json,requests,re,threading,time,os,ujson,os.path
from playsound import playsound
from datetime import date
from datetime import datetime, timedelta


if os.path.isfile("settings.json"):
    with open("settings.json", "r") as settings:
        settings = ujson.load(settings)
        api_key = settings['api-key']
        logPath = settings['logPath']
        soundPath = settings['soundPath']
        tTime = settings['Time']

else:
    settings = {}
    settings["api-key"] = "RGAPI-8f1c21de-617a-4a3d-b1db-b70a3162f825"
    settings["logPath"] = "C:\\Riot Games\\League of Legends\\Logs\\GameLogs"
    settings["soundPath"] = "Alarm.mp3"
    settings["Time"] = 50
    tTime = 50
    api_key = "RGAPI-8f1c21de-617a-4a3d-b1db-b70a3162f825"
    logPath = "C:\Riot Games\League of Legends\Logs\GameLogs"
    soundPath = "Alarm.mp3"
    with open("settings.json", "w") as outfile:
        defaultDump = ujson.dump(settings,outfile,indent=4)

    
    

        

        
    


while True:
    dt = datetime.today()
    def Alert(aTime, gT):
            print("Alert")
            while True:
                dt = datetime.today()
                dt = dt - timedelta(seconds=20)
                print("Time Diff=",dt - gT,"|",dt, gT)
                if dt >= aTime:
                    print('Play Sound')
                    global soundPath
                    playsound(soundPath)
                    time.sleep(35)
                    break
                else:
                    time.sleep(1)

                
                


    def Request(pIGN, region):
        print("Request")
        eSID = requests.get("https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(region,pIGN,api_key),  timeout=10).json()
        print(eSID)
        iD = eSID["id"]
        gT = 0
        a = 0
        while gT <= 0:
            a+=1
            print(a,'gT Attempts')
            gT = requests.get("https://{}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{}?api_key={}".format(region,iD,api_key),  timeout=10).json()
            gT = gT["gameStartTime"]
            print(gT)
            time.sleep(1)
        gT = int(gT) / 1000
        gT = datetime.fromtimestamp(gT).strftime('%Y-%m-%d %H:%M:%S.%f')
        gT = datetime.strptime(gT,'%Y-%m-%d %H:%M:%S.%f')
        global tTime
        aTime = gT + timedelta(seconds=tTime)
        Alert(aTime, gT)
        
    def SearchLog(logPathDirect, item, api_key):
        print("SearchLog")
        a = 0
        while True:
            a+=1
            print(a, 'SearchLog Attempts')
            f = open("{}\{}_r3dlog.txt".format(logPathDirect,item))
            f = f.read()
            if "**LOCAL**" in f:
                region = re.findall("-PlatformID=....", f)
                region = str(region)
                region = region.replace("-PlatformID=", "")
                region = region.replace('"', "")
                region = region.strip("]['")
                #region = region.strip('"')
                print(region)
                pIGN = re.findall('...................LOCAL..', f)
                pIGN = str(pIGN)
                pIGN = re.split("\s", pIGN)
                if pIGN:
                    pIGN = pIGN[2]
                    Request(pIGN, region)
                    break
            time.sleep(1)
            
        



        


    def GetRecent(dt, time, logPath):
        print("GetRecent")
        fileTime = str(time.ctime(os.path.getmtime(logPath)))
        d = datetime.strptime(fileTime,"%a %b  %d %H:%M:%S %Y")
        delta = timedelta(minutes=1)
        time = dt - d
        if dt < d + delta:
            print("new file")
            dirs = os.listdir(logPath)
            if len(dirs) > 1:
                for item in dirs:
                    tem = str(item)
                    date = item[0:10]
                    time = item[11:19]
                    d = datetime.strptime(item,"%Y-%m-%dT%H-%M-%S")
                    delta = timedelta(minutes=1)
                    if dt < d + delta:
                        logPathDirect = "{}\{}".format(logPath, item)
                        SearchLog(logPathDirect, item, api_key)
        else:
            print("too old of file")
    time.sleep(1)
    GetRecent(dt, time, logPath)



