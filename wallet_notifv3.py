import asyncio
import aiohttp
import json
from etherscan.accounts import Account
import time
import discord_notif


class WalletNotif():
    def __init__(self):
        self.address_book = {}
        self.key = ''
        self.influencer_dicts = {}
        self.shared_coins = {}
        self.data = {}
        self.setup()
        self.watch()

    def setup(self):
        with open('./jsons/influencers.json') as influencers_json:
            self.address_book = json.loads(influencers_json.read())
        for influencer in self.address_book.keys():
            path = f'./jsons/{influencer}.json'
            try:
                with open(path) as influencer_dict:
                    self.influencer_dicts[influencer] = json.loads(influencer_dict.read())
            except:
                with open(f'./jsons/{influencer}.json', mode='w') as influencer_dict:
                    new_dict = {}
                    new_dict['coins_bought'] = {}
                    json.dump(new_dict, influencer_dict)
                    self.influencer_dicts[influencer] = {}
        with open(f'./jsons/shared_coins.json') as shared_coins:
            self.shared_coins = json.loads(shared_coins.read())
        with open('./jsons/api_key.json') as api_key:
            self.key = json.loads(api_key.read())['key']


    def watch(self):
        count = 0
        while True:
            for name, address in self.address_book.items():
                print(f"{count} looking through {name}'s address")
                acc = Account(address=address, api_key=self.key)
                transactions = acc.get_transaction_page(page=0, sort ='desc', erc20=True)
                if len(transactions) < 50:
                    upper_range = len(transactions)
                else:
                    upper_range = 50
                for i in range(0,upper_range):
                    curr_tx = transactions[i]
                    token_name = curr_tx['tokenName']
                    if token_name not in self.influencer_dicts[name]:
                        print(f"New token {token_name} found by {name}")
                        if token_name not in self.shared_coins:
                            self.shared_coins[token_name] = 0
                            discord_notif.notif(curr_tx, name, token_name, self.shared_coins[token_name], True)
                        else:
                            self.shared_coins[token_name] += 1
                            discord_notif.notif(curr_tx, name, token_name, self.shared_coins[token_name])
                        self.influencer_dicts[name][token_name] = True
                        discord_notif.update_json(name, token_name, self.influencer_dicts[name], self.shared_coins)
            count += 1
            print('waiting')
            time.sleep(10)
            
            



notif = WalletNotif()






