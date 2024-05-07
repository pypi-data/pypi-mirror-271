import os
try:
 import cloudscraper,random,requests
 
except:
 os.system('pip install cloudscraper')
f =open('proxy.txt','a+').write(requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text)
proxy_list =  open('proxy.txt','r').read().splitlines()
prox = random.choice(proxy_list)
os.remove('proxy.txt')
proxy = {"https://" : prox, "http://" : prox}

whisper = cloudscraper.create_scraper( 
    browser={ 
        'browser': 'chrome', 
        'platform': 'windows', 
        'desktop': True 
    } 
)

def Search_Tellonym(Query:str):
 response=whisper.get(f'https://api.tellonym.me/search/users?searchString={Query}&term={Query}&limit=25',proxies=proxy).json()
 return response


def Check_Tellonym_User(User:str):
 res = whisper.get(f'https://api.tellonym.me/accounts/check?username={User}&limit=25',proxies=proxy).json()
 #print(res)
#Check_Tellonym_User(User='0nz7')
 return res
 

def Check_Tellonym_Email(email:str):
 e1 = email.split('@')[0]
 e2 = email.split('@')[1]
 whis = cloudscraper.create_scraper(browser={ 'browser': 'chrome', 'platform': 'windows', 'desktop': True })
 res = whis.get(f'https://api.tellonym.me/accounts/check?email={e1}%40{e2}&limit=13',proxies=proxy).json()
 return res 
 

def Info_Account(User:str):
 r = whisper.get(f'https://api.tellonym.me/profiles/name/{User}?limit=13',proxies=proxy).json()
 return r