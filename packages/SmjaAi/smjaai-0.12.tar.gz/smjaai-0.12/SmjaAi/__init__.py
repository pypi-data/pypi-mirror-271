import requests , random,os
f =open('proxy.txt','a+').write(requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text)
proxy_list =  open('proxy.txt','r').read().splitlines()
prox = random.choice(proxy_list)
os.remove('proxy.txt')
proxy = {"https://" : prox, "http://" : prox}
def ChatGPT(Text:str):
        while True:
            rq = '123'
            d = random.choice(rq)
            e = random.choice(rq)
            c = random.choice(rq)
            b = random.choice(rq)
            j = d + e
            url = 'https://backend.aichattings.com/api/v2/chatgpt/talk'
            data = {'ep_user_id': j+'62','locale':' en','model':' gpt3','msg':Text}
            req = requests.post(url,data=data,proxies=proxy).text
            da = {'text':req,
            'status':'successfully'}

            return da

def Check_Emails(Email:str):
 req = requests.get(f'https://api.skrapp.io/v3/open/verify?email={Email}',proxies=proxy).json()
 if req["email_status"]=='invalid':
  em = req['email']
  domain = req['domain']
  va = 'available'
  dmj = {'Email':em,
  'Domain':domain,
  'Status':va
  }
  return dmj
 else:
  unva = 'unavailable'
  dmmj = {'Email':req['email'],
  'Domain':req['domain'],
  'Status':unva
  }
  
  return dmmj
