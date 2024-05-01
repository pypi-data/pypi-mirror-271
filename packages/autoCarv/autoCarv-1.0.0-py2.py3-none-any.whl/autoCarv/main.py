import time

from web3 import Web3,HTTPProvider
from eth_account.messages import encode_defunct
import requests
import base64


wallet=''
key=''

getMsgUrl="https://interface.carv.io/protocol/wallet/get_signature_text"
loginUrl ="https://interface.carv.io/protocol/login"
getSoulUrl='https://interface.carv.io/airdrop/mint/carv_soul'
getBalenceUrl="https://interface.carv.io/airdrop/soul/balance"


header = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Origin":"https://protocol.carv.io",
        "Referer":"https://protocol.carv.io/",
        "X-App-Id":"carv"
    }
url='https://interface.carv.io/protocol/login'
opBnbRpc='https://opbnb-rpc.publicnode.com'
Sync='https://mainnet.era.zksync.io'
linea='https://linea.decubate.com'
web3 = Web3(HTTPProvider(opBnbRpc))

def signMessage(pk, web3,msg):
    #msg='AI + DYOR = Ultimate Answer to Unlock Web3 Universe'
    private_key = pk
    message = encode_defunct(text=msg)
    #res=web3.eth.sign(walletAddess,text=msg)
    signed_message = web3.eth.account.sign_message(signable_message=message,private_key=pk)
    #print(web3.eth.account.recover_message(message, signature='0xcb4e97b94da909502dafc55eee9a235e88d1cf67f61742e2eb501a73f18edf582ce27e1ce4ea8d301409839ef0cb3206264e225ba125f7d08bc72cdf364ec3681b'))
    print("签名成功")
    return web3.toHex(signed_message.signature)


msg=""
while True:
    rsp=requests.get(getMsgUrl,headers=header)
    if str(rsp.status_code) != "200":
        time.sleep(5)
    else:
        msg=rsp.json().get("data").get("text")
        break


def login(signNature,wallet,msg):
    jsonData = {
        "wallet_addr":wallet,
        "signature":signNature,
        "text":msg
    }
    rsp=requests.post(url=loginUrl,headers=header,json=jsonData)
    if str(rsp.status_code) != "200":
        time.sleep(5)
    else:
        token=rsp.json().get("data").get("token")
        print("登录成功")
        return token





def getRoainSoul():
    while True:
        tryCnt=0
        rsp=requests.post(url=getSoulUrl,data=roainData,headers=headeWithToken)
        if str(rsp.status_code) != "200":
            print("获取ronin SOUL失败，5S后重试")
            tryCnt+=1
            if tryCnt > 5:
                break
            time.sleep(5)
        else:
            print("获取ronin SOUL成功！")
            break


def getOpbnbSoul(wallet,pk):
    opbnbData = {
        "chain_id": 204
    }
    tryCnt = 0
    while True:
        if tryCnt > 5:
            break
        try:
            rsp=requests.post(url=getSoulUrl,data=opbnbData,headers=headeWithToken)
            hello=rsp.json()
            if str(rsp.status_code) != "200":
                print("获取ronin SOUL失败，5S后重试")
                time.sleep(5)
            else:
                account=rsp.json().get("data").get("permit").get("account")
                amount = rsp.json().get("data").get("permit").get("amount")
                ymd = rsp.json().get("data").get("permit").get("ymd")
                signature = rsp.json().get("data").get("signature")
                contract = rsp.json().get("data").get("contract")
                account64=str.rjust(account[2:],64,"0")
                amounthex = Web3.toHex(amount)
                amount64 = str.rjust(amounthex[2:], 64, "0")
                ymd = Web3.toHex(ymd)
                ymd64 = str.rjust(ymd[2:], 64, "0")
                dataFmt = "0xa2a9539c%s%s%s00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000041%s00000000000000000000000000000000000000000000000000000000000000"
                data = dataFmt % (account64, amount64, ymd64, signature[2:])
                break
        except Exception as e:
            print(e.args[0].get('message'))
            raise e
        tryCnt += 1
    gasPrice = web3.eth.gas_price
    wallet=web3.toChecksumAddress(wallet)
    nonce = web3.eth.get_transaction_count(wallet)
    params = {
        "from": wallet,
        "gasPrice": gasPrice,
        "gas": 200000,
        "nonce": nonce,
        "data": data,
        "chainId": 204,
        "to": contract
    }
    signTx = web3.eth.account.sign_transaction(params, pk)
    tx_hash = web3.eth.send_raw_transaction(signTx.rawTransaction)

    print('交易哈希值为：' + Web3.toHex(tx_hash))
    result = web3.eth.wait_for_transaction_receipt(Web3.toHex(tx_hash))
    ststus = result.get('status')
    if '1' == str(ststus):
        print('成功mint SOUL金额：' + str(amount))
    else:
        print('mint失败')

def getBalence():
    rsp = requests.get(getBalenceUrl,headers=headeWithToken)
    if str(rsp.status_code) != "200":
        print("获取余额失败，5S后重试")
        time.sleep(5)
    else:
        print("mint后余额为："+str(rsp.json().get("data").get("balence")))


signMsg=signMessage(key,web3,msg)

token = login(signMsg,wallet,msg)
tokenEoa="eoa:"+str(token)
token64 = base64.b64encode(bytes(tokenEoa.encode("utf-8")))

headeWithToken={
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Authorization": 'bearer '+ str(token64, "utf-8"),
    "Origin": "https://protocol.carv.io",
    "Referer": "https://protocol.carv.io/",
    "X-App-Id": "carv"
}

roainData={
    "chain_id":2020
}
getRoainSoul()
getOpbnbSoul(wallet, key)
time.sleep(2)
getBalence()


