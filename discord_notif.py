from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
import json

def notif(token, influencer_name, token_name, others_bought, is_new=False):
    #color is dark green
    web_hook = DiscordWebhook(url='ENTER_DISCORD_WEBHOOK_HERE')
    embed = DiscordEmbed(title = f'{influencer_name} has made a new transaction!', color='2263842')
    embed.add_embed_field(name = "Token Name", value=f"{token['tokenName']}")
    embed.add_embed_field(name = "Contract ID", value=f"https://etherscan.io/token/{token['contractAddress']}")
    embed.add_embed_field(name = "TX ID", value=f"https://etherscan.io/tx/{token['hash']}")
    embed.add_embed_field(name = "Uniswap", value=f"https://uniswap.info/token/{token['contractAddress']}")
    embed.add_embed_field(name = "Timestamp", value = str(datetime.datetime.now().time()))
    if is_new is False:
        embed.add_embed_field(name = 'New/old', value= "**OLD**")
        embed.add_embed_field(name = 'OTHERS BOUGHT?', value = str(others_bought))
    else:
        embed.add_embed_field(name = 'New/old', value="**NEW**")
    web_hook.add_embed(embed)
    web_hook.execute()

def update_json(influencer_name, token_name, influencer_dict, shared_dict):
    with open(f'./jsons/{influencer_name}.json', mode='w') as influencer_json:
        json.dump(influencer_dict, influencer_json)
    with open('./jsons/shared_coins.json', mode='w') as shared_json:
        json.dump(shared_dict, shared_json)
