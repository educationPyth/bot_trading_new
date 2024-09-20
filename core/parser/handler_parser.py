from aiogram import Bot
from aiogram.types import Message
from core.parser.parser_cmc import parse_transactions
# from db import get_token, set_group_id, set_photo, get_user_links, get_choose_transaction
import datetime
import database.requests as rq


async def check_transactions(user_id, chat_id):
    # const
    data_db = await rq.get_data(user_id)
    bot_data = await rq.bot_id(chat_id)
    if bot_data:
        bot_id = bot_data.id
        bots = data_db.get('bots')[bot_id-1]
        # data bd
        chat = bots['chat']
        output_id = chat
        contract = bots['contract']
        photo = bots['photo']

        domain = ['hhtp', 'https', 'www']
        links_user_str = bots['links']
        links = {}
        if len(links_user_str) == 0:
            links_user = None
        elif len(links_user_str) > 0:
            links_user = links_user_str.split(';')
            for item in links_user:
                if item != '':
                    name = item.split(' ')[0]
                    link = item.split(' ')[1]
                    if not any(link.startswith(prefix) for prefix in domain):
                        address = 'www.' + link
                    else:
                        address = link
                    links[name] = address

        # data parser
        data_transaction = await parse_transactions(user_id=user_id, chat_id=chat)
        # print(data_transaction)
        if data_transaction is None:
            return None
        elif data_transaction == 'equally':
            return 'equally'
        else:
            if not data_transaction:
                # await bot.send_message(user_id, 'Упс..Что-то пошло не так!\n'
                #                                 'Попробуйте ввести другой контракт (Pairs contract)')
                print('Упс..Что-то пошло не так!\n'
                      'Попробуйте ввести другой контракт (Pairs contract)')
            else:
                time_transactions = data_transaction['data']['transactions'][0]['time']

                unix_timestamp = int(time_transactions)
                transaction_time = datetime.datetime.fromtimestamp(unix_timestamp)

                formatted_time = transaction_time.strftime("%H:%M:%S %d.%m.%Y")

                type_transactions = data_transaction['data']['transactions'][0]['type']
                price_usdt = data_transaction['data']['transactions'][0]['priceUsd']
                amount = data_transaction['data']['transactions'][0]['amount']
                total_usdt = data_transaction['data']['transactions'][0]['totalUsd'][:5]
                total_quote = data_transaction['data']['transactions'][0]['totalQuote']
                volume24 = data_transaction['volume24']
                name_coin = data_transaction['name_coin']
                contract = data_transaction['contract']
                base_token = data_transaction['base_token']
                liquidity = data_transaction['liquidity']

                # Обрезание строки после .
                price_usdt_container = price_usdt.split('.')
                num_cut = int(len(price_usdt_container[1]) / 2)
                if len(price_usdt_container[1]) > 8:
                    price_usdt = price_usdt[:num_cut]

                if len(volume24) > 2:
                    volume24_man_part = volume24.split('.')
                    volume24_container_decimal = volume24_man_part[1]
                    volume24 = volume24_man_part[0] + '.' + volume24_container_decimal[:2]

                liquidity_list = liquidity.split('.')
                liquidity = liquidity_list[0]

                # Если выбор только ПОКУПКИ
                # select = get_choose_transaction(from_user_id=user_id, from_chat_id=chat)
                select = 'buy'
                if select == 'buy' and type_transactions == 'buy':
                    text = f"""<b>🆕✅✅ {name_coin} new Buy ✅✅🆕</b>
    
⏳ <b>Time: {formatted_time}</b>

💰 <b>Spent: {total_quote} TON (${total_usdt})</b>

🧳 <b>Bought: {amount} {name_coin}</b>

💲 <b>Price: ${price_usdt}</b>

📈 <b><a href='https://coinmarketcap.com/dexscan/ru/ton/{contract}/'>Chart coinmarketcap</a> | <a href='https://dedust.io/swap/{base_token}/TON'>buy</a></b>

🏦 <b>Liquidity: ${liquidity}</b>

💰 <b>Volume(24): ${volume24}</b>

👨‍🦰 <b><a href='https://tonviewer.com/{base_token}?section=holders'>Holders</a></b>
"""
                    data_parser = {
                        'html': text,
                        'photo': photo,
                        'links': links
                    }
                    return data_parser
                    # await send_photo(output_id, photo=photo, caption=text, reply_markup=await user_links(links),
                    #                     parse_mode='HTML')
    else:
        return None


    #             # Если выбор только ПРОДАЖИ
    #             elif select == 'sell':
    #                 if type_transactions == 'sell':
    #                     text = f"""<b>🆕❌❌ {name_coin} new Sell ❌❌🆕</b>
    #
    # ⏳ <b>Time: {formatted_time}</b>
    #
    # 💰 <b>Spent: {total_quote} TON (${total_usdt})</b>
    #
    # 🧳 <b>Bought: {amount} {name_coin}</b>
    #
    # 💲 <b>Price: ${price_usdt}</b>
    #
    # 📈 <b><a href='https://coinmarketcap.com/dexscan/ru/ton/{contract}/'>Chart coinmarketcap</a> | <a href='https://dedust.io/swap/{base_token}/TON'>buy</a></b>
    #
    # 🏦 <b>Liquidity: ${liquidity}</b>
    #
    # 💰 <b>Volume(24): ${volume24}</b>
    #
    # 👨‍🦰 <b><a href='https://tonviewer.com/{base_token}?section=holders'>Holders</a></b>
    # """
    #                     await bot.send_photo(output_id, photo=photo, caption=text, reply_markup=kb_inline_user_links(links),
    #                                          parse_mode='HTML')
    #             # Если выбор ВСЕ транзакции
    #             elif select == 'both':
    #                 if type_transactions == 'sell':
    #                     text_header = f"<b>🆕❌❌ {name_coin} new Sell ❌❌🆕</b>"
    #                 else:
    #                     text_header = f"<b>🆕✅✅ {name_coin} new Buy ✅✅🆕</b>"
    #                 text = f"""{text_header}
    #
    # ⏳ <b>Time: {formatted_time}</b>
    #
    # 💰 <b>Spent: {total_quote} TON (${total_usdt})</b>
    #
    # 🧳 <b>Bought: {amount} {name_coin}</b>
    #
    # 💲 <b>Price: ${price_usdt}</b>
    #
    # 📈 <b><a href='https://coinmarketcap.com/dexscan/ru/ton/{contract}/'>Chart coinmarketcap</a> | <a href='https://dedust.io/swap/{base_token}/TON'>buy</a></b>
    #
    # 🏦 <b>Liquidity: ${liquidity}</b>
    #
    # 💰 <b>Volume(24): ${volume24}</b>
    #
    # 👨‍🦰 <b><a href='https://tonviewer.com/{base_token}?section=holders'>Holders</a></b>
    # """
    #                 await bot.send_photo(output_id, photo=photo, caption=text, reply_markup=kb_inline_user_links(links),
    #                                      parse_mode='HTML')

