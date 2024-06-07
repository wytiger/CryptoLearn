import requests
from web3 import Web3
from eth_account.messages import encode_defunct
import json

class Blast:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "If-None-Match": 'W/"22-B2qIJ359b+laS9nBTB/cr49Jplo"',
            "Origin": "https://blast.io",
            "Priority": "u=1, i",
            "Referer": "https://blast.io/",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        self.cookies = None
        

    def challenge(self,wallet_address):
        print(wallet_address) 
        url = f"https://waitlist-api.prod.blast.io/v1/auth/wallet/challenge"
        params = {'walletAddress': wallet_address}
        # 创建一个会话对象
        session = requests.Session()
        # 第一次请求，获取响应头中的Cookie并保存到会话中
        response = requests.post(url, headers=self.headers,json=params)
        self.cookies = response.cookies
        
        print('challenge:\n',response.json()) 
        print('*********************') 
        if response.status_code == 201:        
            return response.json()  # Assuming the response is in JSON format
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
        


    def login(self,challenge,web3,private_key):
        message = challenge.get("message")
        #先对数据进行编码再签名
        message_encoded = encode_defunct(text=message)
        sign_message = web3.eth.account.sign_message(message_encoded, private_key)
        signature = sign_message.signature.hex()

        print("walletAddress:\n",challenge.get("walletAddress"))
        print("message:\n",message)
        print("signature:\n",signature)

        url = f"https://waitlist-api.prod.blast.io/v1/auth/wallet/login"
        params = {
                  'walletAddress':challenge.get("walletAddress"),
                  'expiresOn':challenge.get("expiresOn"),
                  'hmac':challenge.get("hmac"),
                  'message':message,
                  'signature':signature
                  }
        response = requests.Session().post(url, headers=self.headers, cookies=self.cookies,json=params)
        self.cookies.update(response.cookies)
        print(response.text) 
        print('*********************') 
        if response.status_code == 201 | response.status_code == 200:        
            return response.json()  # Assuming the response is in JSON format
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
        

    def me(self,wallet_address):
        url = f"https://waitlist-api.prod.blast.io/v1/auth/me"
        params = {'walletAddress': wallet_address}
        response =  requests.Session().get(url, headers=self.headers, cookies=self.cookies)
        print(response.text) 
        print('#######################') 
        if response.status_code == 200:     
            f = open('blastStatic.txt','a')
            # 将JSON字符串加载为Python字典
            data = json.loads(response.text)           
            season2 = data['user']['season2']
            multiplier = season2['multiplier'] 
            boostedSelfPoints = season2['boostedSelfPoints']
            boostedReferralPoints = season2['boostedReferralPoints'] 
            totalPoints = boostedSelfPoints+boostedReferralPoints           
            gold = season2['unboostedDeveloperSelfPoints']
            #打印到屏幕与文件
            print(wallet_address)            
            print(multiplier) 
            print(totalPoints)
            print(gold)
            print(wallet_address,file=f)            
            print(multiplier,file=f)     
            print(totalPoints,file=f)
            print(gold,file=f)
            print('-------------------------------------------------',file=f)
            return response.json()  # Assuming the response is in JSON format
        else:
            return {"error": f"Request failed with status code {response.status_code}"}



    def balances(self,wallet_address):
        url = f"https://waitlist-api.prod.blast.io/v1/user/public/l2-balances"
        params = {'walletAddress': wallet_address}
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        print(response) 
        if response.status_code == 200:        
            return response.json()  # Assuming the response is in JSON format
        else:
            return {"error": f"Request failed with status code {response.status_code}"}


    def has_account(self,wallet_address):
        url = f"https://waitlist-api.prod.blast.io/v1/auth/wallet/has-account"
        params = {'walletAddress': wallet_address}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            f = open('hasAccount.txt','a')
            hasAccount = response.json().get('hasAccount')             
            text = str(hasAccount)
            print(wallet_address)
            print(text)
            print('*********************')            
            #print(wallet_address,file=f)
            print(text,wallet_address,file=f)
            return response.json()  # Assuming the response is in JSON format
        else:
            return {"error": f"Request failed with status code {response.status_code}"}


def main():
        f = open('privateKey.txt', 'r', encoding='utf-8')
        private_key_list = f.readlines()
        f.close()
        
        rpc="https://rpc.blast.io"
        web3 = Web3(Web3.HTTPProvider(rpc))
    
        for idx, private_key in enumerate(private_key_list):     
            account = web3.eth.account.from_key(private_key.strip()) 
            privateKey = private_key.strip()
            address = account.address.strip()

            blast = Blast()
            blast.has_account(address)            
            challenge= blast.challenge(address)            
            # 要检查的键名（注意这里是字符串，而不是变量）
            key_to_check = 'challenge'
            if key_to_check in challenge:                
                challengeData = challenge.get("challenge")
                blast.login(challengeData,web3,privateKey)
                blast.me(address)
            
            print("---------------------")


main()
