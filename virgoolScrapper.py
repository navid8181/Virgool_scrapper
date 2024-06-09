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

        '__arcsjs': 'c2c5893857a5f46c508f8b14bf7a6c6a',
        '_ga': 'GA1.1.562552015.1717925749',
        '_ga_V1LLR5NWKW': 'GS1.1.1717932661.2.0.1717932661.0.0.0',
    }

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

            # get json Data
            jsonData = r.json()
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
                f'Work-{(1.0*currentIndexPage/lastPage)* 100.0}% is complete')

            if currentIndexPage > lastPage:
                break

            currentIndexPage += 1
        except Exception as e:
            #enter captcha to scrape more data!
            
            print(url)
            print(
                "please enter new __arcsrc cookie from link above after complete captcha :")
            cookie['__arcsjs'] = input("enter __arcsjs : ")

    jsonString = json.dumps([ob.__dict__ for ob in allData])

    f = open(f'{userID}-{userType.name}.json', 'a')
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
        
        

    