import os
try:
 import cloudscraper
except:
 os.system('pip install cloudscraper')

whisper = cloudscraper.create_scraper( 
    browser={ 
        'browser': 'chrome', 
        'platform': 'windows', 
        'desktop': True 
    } 
)

def Search_Tellonym(Query:str):
 response=whisper.get(f'https://api.tellonym.me/search/users?searchString={Query}&term={Query}&limit=25').json()
 return response


def Check_Tellonym_User(User:str):
 res = whisper.get(f'https://api.tellonym.me/accounts/check?username={User}&limit=25').json()
 return res
 

def Check_Tellonym_Email(email:str):
 e1 = email.split('@')[0]
 e2 = email.split('@')[1]
 whis = cloudscraper.create_scraper(browser={ 'browser': 'chrome', 'platform': 'windows', 'desktop': True })
 res = whis.get(f'https://api.tellonym.me/accounts/check?email={e1}%40{e2}&limit=13').json()
 return res 
 

def Info_Account(User:str):
 r = whisper.get(f'https://api.tellonym.me/profiles/name/{User}?limit=13').json()
 return r