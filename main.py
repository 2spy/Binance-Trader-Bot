# Copyright 2022
# By 2$py#5340
# Version 0.0.1
# from github.com/2spy

import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import threading
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

def main(url):
    with open('config.json', 'r') as f:
        config = json.load(f)
    webhookurl = config['webhook']
    Uid = url.split('=')[-1]
    s = requests.Session()
    data2 = {
        "encryptedUid": Uid
    }

    r = s.post('https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo',
               json=data2)
    dats2 = json.loads(r.text)
    last_trade = {}
    while True:
        try:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

            user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
            useragent = user_agent_rotator.get_random_user_agent()
            headers = {
                'User-Agent': useragent,
                #'cookie': "cid=U4Wyp49n; bnc-uuid=374b0592-9f57-4752-ab39-26e1acd84e50; monitor-uuid=015583d9-cdd4-4050-a210-a3f3a4955a8c; _gcl_au=1.1.1655517786.1666871959; userPreferredCurrency=USD_USD; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22184194fa111434-0114ffee05327f6-26021f51-2073600-184194fa112ee7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg0MTk0ZmExMTE0MzQtMDExNGZmZWUwNTMyN2Y2LTI2MDIxZjUxLTIwNzM2MDAtMTg0MTk0ZmExMTJlZTcifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22184194fa111434-0114ffee05327f6-26021f51-2073600-184194fa112ee7%22%7D; BNC_FV_KEY=3381e2673043a2aea3adcdfddf996ff40e60248b; BNC_FV_KEY_EXPIRE=1666893561355; OptanonAlertBoxClosed=2022-10-27T11:59:22.543Z; _gid=GA1.2.619676464.1666871963; lang=en; theme=dark; _ga_3WP50LGEEC=GS1.1.1666871959.1.1.1666872325.59.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Oct+27+2022+14%3A05%3A26+GMT%2B0200+(heure+d%E2%80%99%C3%A9t%C3%A9+d%E2%80%99Europe+centrale)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3fa8b2a3-33f9-4e9a-8bfb-c4a3d4b4ff8d&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&geolocation=FR%3BPAC&AwaitingReconsent=false; _ga=GA1.2.1395835907.1666871960; _gat_UA-162512367-1=1",
                #'crsftoken': '41d8cd98f00b204e9800998ecf8427e',
                "Accept-Encoding": "*",
                "Connection": "keep-alive"
            }

            data = {
                "encryptedUid": Uid,
                "tradeType": "PERPETUAL"
            }
            r = requests.post("https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition",
                              json=data, headers=headers)
            dats = json.loads(r.text)
            alltradeactive = []
            for trade in dats['data']['otherPositionRetList']:
                alltradeactive.append(str(trade['updateTimeStamp']))
                if str(trade['updateTimeStamp']) not in last_trade.keys():
                    currency = trade['symbol']
                    user = dats2['data']['nickName']
                    img = dats2['data']['userPhotoUrl']
                    marketprice = trade['markPrice']
                    if '-' in str(trade['amount']):
                        longorshot = "Vente 🔴"
                    else:
                        longorshot = "Achat 🟢"
                    levier = trade['leverage']
                    taille = str(trade['amount'])
                    entry = "$" + str(trade['entryPrice'])
                    times = time.time()
                    embed = DiscordEmbed(title="📊 Nouvelle position ouverte sur $" + currency, color=0x32CD32)
                    embed.description = "***Version: *** ``0.0.1``\n\n"
                    embed.set_thumbnail(url="https://logodownload.org/wp-content/uploads/2021/03/binance-logo-0-2048x2048.png")
                    embed.set_author(name=user, icon_url=img)
                    embed.add_embed_field(name="Prix d'entrée:", value=f"> {entry}", inline=False)
                    embed.add_embed_field(name="Prix du marché:", value="> $" + str(marketprice), inline=False)
                    embed.add_embed_field(name="Long ou Short:", value="> " + longorshot, inline=False)
                    embed.add_embed_field(name="Taille:", value="> " + str(taille), inline=False)
                    embed.add_embed_field(name="Levier", value="> x" + str(levier), inline=False)
                    embed.set_footer(text="Binance Futures by 2$py#5340", icon_url="https://logodownload.org/wp-content/uploads/2021/03/binance-logo-0-2048x2048.png")
                    embed.set_timestamp()


                    webhook = DiscordWebhook(url=webhookurl, username="Binance Tracker", avatar_url=img, rate_limit_retry=True)
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    end = time.time() - times


                    last_trade[str(trade['updateTimeStamp'])] = {'user': user, 'currency': currency, 'img': img, 'longorshot': longorshot,'amount': trade["amount"], 'entry': entry, 'levier': levier, 'marketprice': marketprice}
                    print("New trade detected + Time to send: " + str(round(end*1000)) + "ms")

            listtradetodelete = []
            for traded in last_trade.keys():
                if traded not in alltradeactive:
                    data = last_trade[traded]
                    listtradetodelete.append(traded)

                    embeds = DiscordEmbed(title='Trade Closed', description="Trade closed", color=0xFF0000)
                    embeds.set_footer(text='Binance Account Tracker', icon_url=data['img'])
                    embeds.set_thumbnail(url=data['img'])
                    message = ""
                    message += "> ***User: ***" + data['user'] + "\n\n"
                    message += "> ***Currency: ***" + data['currency'] + "\n\n"
                    message += "> ***Long/Short: ***" + data['longorshot'] + "\n\n"
                    message += "> ***Market Price: ***" + "$" + str(data['marketprice']) + "\n\n"
                    message += "> ***Taille: ***" + str(data['amount']) + "\n\n"
                    message += "> ***Leverage: ***" + str(data['levier']) + "\n\n"
                    embeds.set_timestamp()
                    embeds.description = message
                    webhooks = DiscordWebhook(url=webhookurl, username="Binance Tracker", avatar_url=data['img'], rate_limit_retry=True)
                    webhooks.add_embed(embeds)
                    response = webhooks.execute()
                    print("Trade closed")
            for i in listtradetodelete:
                del last_trade[i]

            time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(3)
            pass



if __name__ == "__main__":
    alluid = open('profileuid.txt', 'r').read().splitlines()
    for uid in alluid:
        print(uid)
        threading.Thread(target=main, args=(uid,)).start()
