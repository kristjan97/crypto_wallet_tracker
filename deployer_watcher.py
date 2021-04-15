from etherscan.accounts import Account
import time

def deployer_watcher(address, key):
    acc = Account(address=address, api_key=key)
    transactions = acc.get_transaction_page(page=1, offset=10000, sort='des', erc20=True)
    for transaction in transactions:
        if transaction['from'] == 'ADDRESS_HERE':
            print(transaction)


deployer_watcher('ADDRESS_HERE', 'KEY_HERE')