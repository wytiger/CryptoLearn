import requests

def __init__():
    headers = {
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


def balances(wallet_address):
    url = f"https://waitlist-api.prod.blast.io/v1/user/public/l2-balances"
    params = {'walletAddress': wallet_address}
    response = requests.options(url, params=params)

    if response.status_code == 200:        
        return response.json()  # Assuming the response is in JSON format
    else:
        return {"error": f"Request failed with status code {response.status_code}"}


def check_wallet_account(wallet_address):
    url = f"https://waitlist-api.prod.blast.io/v1/auth/wallet/has-account"
    params = {'walletAddress': wallet_address}
    response = requests.get(url, params=params)
    print(response.request.url)

    if response.status_code == 200:
        f = open('hasAccount.txt','a')
        hasAccount = response.json().get('hasAccount')
        text = str(hasAccount)+', '+wallet_address
        print(text)
        print(text,file=f)
        return response.json()  # Assuming the response is in JSON format
    else:
        return {"error": f"Request failed with status code {response.status_code}"}


def main():
    f = open('account.txt', 'r', encoding='utf-8')
    accounts = f.readlines()
    f.close()
    
    for idx, account in enumerate(accounts):     
        print(account)
        address = account.strip()
        '''result = balances(address)
        print(result) '''  
        result2 = check_wallet_account(address)
        print(result2)
        print("---------------------")


main()