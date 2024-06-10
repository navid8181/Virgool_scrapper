# get library

import requests
import json
from fake_http_header import FakeHttpHeader
from Constatnt import BASE_URL, UserType

import sys
import os
from user import User


def getUrl(baseUrl, userID, userType: UserType, numberPage):
    url = f'{baseUrl}/{userID}/{userType.name}?page={numberPage}'
    return url


def ScrapeData(userID, userType: UserType):


    # create fake header for bypassing captcha
    fake_header = FakeHttpHeader()



    header = fake_header.as_header_dict()


    # set cookie for verify captcha
    cookie = {

        '__arcsrc': ''
    }
    
    if os.path.exists('cookie.json') :
        myCookieFile = open('cookie.json')
        dataCookie  = myCookieFile.read()
        dataCookie = json.loads(dataCookie)
  
        if dataCookie['__arcsrc']  != "" :
            cookie['__arcsrc'] = dataCookie['__arcsrc']
        myCookieFile.close()
     
    # userID = "hassan.sheikh7"
    currentIndexPage = 1
    # userType = UserType.following
    # data that must be save to file
    allData = []
    url = ''
    while True:

        try:

            # create URL
            header = fake_header.as_header_dict()
            url = getUrl(BASE_URL, userID, userType, currentIndexPage)
            r = requests.get(url, headers=header, cookies=cookie)
            #check not error has been rise
            jsonData = r.json()
        
 
            if 'error' in jsonData :
                raise Exception(jsonData['error'])
            # get json Data
            data = jsonData['data']

            for d in data:
                newUser = None
                if userType == UserType.following:
                    newUser = User(userID, d['username'])
                else:
                    newUser = User(d['username'], userID)
                allData.append(newUser)

            # get last page
            lastPage = jsonData['pagination']['lastPage']
            lastPage = int(lastPage)

            print(
                f'Work- {(1.0*currentIndexPage/lastPage)* 100.0}% is complete')

            if currentIndexPage > lastPage:
                break

            currentIndexPage += 1
        except Exception as e:
            #enter captcha to scrape more data!
            print(e)
            if str(e) == 'not_found':
                raise Exception("user not found")
            print(url)
            print(
                "please enter new [__arcsrc] cookie from link above after complete captcha :")
            cookie['__arcsrc'] = input("enter __arcsrc : ")
            
            cookieFile = open('cookie.json','w')
            cookieFile.write(json.dumps(cookie))
            cookieFile.close()
            
            

    jsonString = json.dumps([ob.__dict__ for ob in allData])

    f = open(f'{userID}-{userType.name}.json', 'w')
    f.write(jsonString)
    f.close()



scrapeMode = sys.argv[1]

if scrapeMode == "user" :
    userID = sys.argv[2]
    userTypeIO = sys.argv[3]
    userType  = None
    
    if userTypeIO == "following":
        userType = UserType.following
    elif userTypeIO == "followers" :
        userType = UserType.followers
    else :
        raise Exception("user Type must be [following] | [followers] ")

    
    ScrapeData(userID,userType)   

elif  scrapeMode == 'file' :
    #must enter file of followings json to collect data
    jsonFileName  = sys.argv[2]
    
    jsonData = open(jsonFileName)
    data = json.load(jsonData)
    
    count = 0
    for user in data :
     
        userId = user['toUserID']
        count +=1
        print("***************")
        print(count)
        if os.path.exists(f'{userId}-following.json'):
            continue
        
        ScrapeData(userId,UserType.following)
        ScrapeData(userId,UserType.followers)
        
        

    