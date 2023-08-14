import requests
import telebot


token = '6352398845:AAGPJChFGJCDuLYPnv4-ppJrm6_tCxu-bYM'
bot = telebot.TeleBot(token)
r = requests.get("https://api.opendota.com/api/heroes")
heroes = r.json()
heroes_id = dict()
for i in heroes:
    heroes_id[i['id']] = i['localized_name']
abbreviations = {'am': 1, 'bs': 4, 'cm': 5, 'drow': 6, 'shaker': 7, 'jug': 8, 'morph': 10, 'sf': 11, 'pl': 12, 'sk': 16,
                 'storm': 17, 'vs': 20, 'wr': 21, 'shaman': 27, 'tide': 29, 'wd': 30, 'necr': 36, 'beast': 38,
                 'qop': 39, 'venom': 40, 'void': 41, 'wk': 42, 'dp': 43, 'pa': 44, 'ta': 46, 'dk': 49, 'clock': 51,
                 'furion': 53, 'ls': 54, 'ds': 55, 'omni': 57, 'koza': 58, 'ns': 60, 'brood': 61, 'bh': 62, 'bat': 65,
                 'aa': 68, 'bara': 71, 'gyro': 72, 'od': 76, 'pivo': 78, 'sd': 79, 'ld': 80, 'ck': 81, 'treant': 83,
                 'ogre': 84, 'zombi': 85, 'nyx': 88, 'naga': 89, 'kotl': 90, 'wisp': 91, 'dusa': 94, 'trol': 95,
                 'cent': 96, 'timber': 98, 'ej': 99, 'sky': 101, 'elder': 103, 'lc': 104, 'miner': 105, 'ember': 106,
                 'zemla': 107, 'pit': 108, 'tb': 109, 'bird': 110, 'wyvern': 112, 'arc': 113, 'mk': 114, 'dw': 119,
                 'pango': 120, 'grim': 121, 'belka': 123, 'vs': 126, 'babka': 128, 'db': 135, 'pb': 137}


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Вводи героев через пробел.')


@bot.message_handler(commands=['help'])
def help(m):
    str = ''
    for i in abbreviations:
        str += f'{heroes_id[abbreviations[i]]}: *{i}*\n'
    bot.send_message(m.chat.id, 'Вместо полных названий героев можно использовать следующие сокращения:\n' + str,
                     parse_mode='Markdown')


@bot.message_handler(content_types=["text"])
def get_hero(m):
    hero = m.text.lower().split()
    ids = []
    for i in hero:
        r = abbreviations.get(i)
        id = 0
        if r is None:
            for j in heroes:
                if j['localized_name'].lower() == i:
                    id = j['id']
            if id == 0:
                bot.send_message(m.chat.id, 'Не найден герой ' + i)
                return
        else:
            id = r
        ids.append(id)
    print(ids)
    for i in ids:
        for j in heroes:
            if j['id'] == i:
                print(j['localized_name'], end=' ')
    n = len(ids)
    winrate = [dict()] * n
    for id in range(n):
        r = requests.get(f"https://api.opendota.com/api/heroes/{ids[id]}/matchups").json()
        for i in r:
            if i['games_played'] > 10:
                winrate[id][i['hero_id']] = i['wins'] / i['games_played'] * 100
            else:
                winrate[id][i['hero_id']] = 50
    cwinrate = []
    for id in winrate[0]:
        s = 0
        for i in winrate:
            s += i[id]
        cwinrate.append((s / n, id))
    cwinrate.sort(reverse=True)
    print(cwinrate)
    ans = ''
    for i in cwinrate:
        ans += f'*{heroes_id[i[1]]}*: {round(i[0], 2)}%\n'
    bot.send_message(m.chat.id, ans, parse_mode='Markdown')


bot.polling(none_stop=True, interval=0)
