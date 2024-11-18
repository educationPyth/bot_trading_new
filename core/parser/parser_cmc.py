import re
import json
import requests
import database.requests as rq


async def parse_transactions(user_id, chat_id):
    data_db = await rq.get_data(user_id)
    bot_data = await rq.bot_id(chat_id)
    bot_id = bot_data.id
    bots = data_db.get('bots')[bot_id-1]
    # print(f'modul - parser_cmc.py, str - 12\n'
    #       f'{bots}')
    token = bots['contract']
    transactions_time = bots['transactions_time']
    chat = bots['chat']
    # data_last_time = get_last_time_transaction(from_user_id=user_id, from_chat_id=chat_id)
    if transactions_time is not None:
        last_time = transactions_time
        # print(f'last_time before - {last_time}')
        # general_info
        data = parse_general_information(token)
        if data.get('data') is None:
            return False
        platform_id = data['data']['platform']['id']
        pool_id = data['data']['poolId']
        name_coin = data['data']['baseToken']['symbol']
        base_token = data['data']['baseToken']['address']
        volume24 = data['data']['volume24h']
        contract = data['data']['address']
        liquidity = data['data']['poolInfoD']['liquidity']
        # transaction_info
        url_transactions = f'https://api.coinmarketcap.com/kline/v3/k-line/transactions/{platform_id}/{pool_id}?reverse-order=true'
        data_transactions = requests.get(url=url_transactions)
        # print(transactions_time)
        # print(data_transactions)
        if data_transactions.status_code == 200:
            data = data_transactions.json()
            # print(data)

            first_transaction = data['data']['transactions'][0]
            time_first_transaction = int(first_transaction['time'])
            # print(first_transaction)
            # print(f'current_time before = {current_time}')
            if time_first_transaction != last_time:
                data['name_coin'] = name_coin
                data['volume24'] = volume24
                data['contract'] = contract
                data['base_token'] = base_token
                data['liquidity'] = liquidity
                # print('Должна пройти')
                update_last_time_transaction = time_first_transaction
                await rq.set_last_time_transaction(last_time_transactions=update_last_time_transaction, chat_id=chat)
                # print(f'last_time after - {update_last_time_transaction}')
                return data
            else:
                return 'equally'
        else:
            return False

    #         else:
    #             # print('транзакция была')
    #             return 'False'
    # else:
    #     return 'False'


def parse_general_information(token):
    pattern = r'(.|\n)*'
    pattern_ignore_case = re.compile(pattern, re.IGNORECASE)
    if pattern_ignore_case.match(token):
        url = f'https://api.coinmarketcap.com/dexer/v3/dexer/pair-info?dexer-platform-name=ton&address={token}'
        general_info = requests.get(url=url)
        if general_info.status_code == 200:
            data = general_info.json()
            # print(json.dumps(data, indent=4))
            return data

    return None
