import threading
import random
import time
import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3

vk_session1 = vk_api.VkApi(token='836b224a9cb082af2bf804c598fc7e8b45274bfa5e533a45dfec4797b58139c59204cd0f53fe11be183aa')
acc = vk_session1.get_api()
longpoll = VkLongPoll(vk_session1)

vk_session = vk_api.VkApi(token='6a22339594750300f27b35460ff7658133f780405aea001db0b67bbdb2b84a91db2f112371d789028c255')
vk = vk_session.get_api()
a1 = False
a2 = False

def main():
    print('Dep thread started')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.peer_id == -166948584 and not event.from_me:
                if event.message.find('ты получил') != -1:
                    text = event.message.split()
                    amount = text[3].replace('$', '')
                    amount = amount.replace('.','')
                    id = text[6].replace('[id', '')
                    id = id[0:9]
                    conn = sqlite3.connect("bot.db")
                    cursor = conn.cursor()
                    sql = f"SELECT * FROM acc WHERE `id` = {id}"
                    cursor.execute(sql)
                    user_data = cursor.fetchone()
                    if user_data != None:
                        sql = f"UPDATE acc SET `money` = {user_data[1] + int(amount)} WHERE `id` = {id}"
                        cursor.execute(sql)
                        conn.commit()
                        vk.messages.send(user_id=id, random_id=get_random_id(), message=f"твой счет был пополнен на ${formatnum(amount)}. баланс - ${formatnum(user_data[1]+int(amount))}")

def posting():
    print('Post thread started')
    global a1, a2
    while True:
        if time.strftime('%H:%M') == '18:32' and a1 == False:
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"SELECT * FROM acc WHERE `id` = 0"
            cursor.execute(sql)
            temp = cursor.fetchone()
            acc.wall.delete(owner_id=-198251975, post_id=temp[3])
            tmp = acc.wall.post(owner_id=-198251975, from_group=1, message='покупка лотерей закрывается так как через 5 минут будет выбран счастливый билет!', close_comments=1)
            sql = f"UPDATE acc SET `state` = 'close', `dop` = '{tmp['post_id']}' WHERE `id` = 0"
            cursor.execute(sql)
            conn.commit()
            a1 = True
        elif time.strftime('%H:%M') == '18:36' and a2 == False:
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"SELECT * FROM tickets"
            cursor.execute(sql)
            members = cursor.fetchall()
            conn.commit()
            if len(members) == 0:
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                sql = "SELECT * FROM acc WHERE `id` = 0"
                cursor.execute(sql)
                temp = cursor.fetchone()
                conn.commit()
                acc.wall.delete(owner_id=-198251975, post_id=temp[3])
                temp = acc.wall.post(owner_id=-198251975, from_group=1, message='розыгрыша нет, так как никто не купил билетики(', close_comments=1)
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                sql = f"UPDATE acc SET `state` = 'open', `dop` = '{temp['post_id']}' WHERE `id` = 0"
                cursor.execute(sql)
            else:
                win_id = random.randint(1, len(members)) - 1
                winner = members[win_id]

                prize = len(members) * 1000
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                sql = f"SELECT * FROM acc WHERE `id` = {winner[1]}"
                cursor.execute(sql)
                user_data = cursor.fetchone()
                sql = f"UDPATE acc SET `money` = {user_data[1] + prize} WHERE `id` = {user_data[0]}"
                cursor.execute(sql)
                conn.commit()

                vk.messages.send(user_id=user_data[0], random_id=get_random_id(), message=f"поздравляем! ты выиграл в лотерее ${formatnum(prize)}<br><br>баланс - ${formatnum(user_data[1] + prize)}")

                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                sql = "DELETE FROM tickets"
                cursor.execute(sql)
                sql = "SELECT * FROM acc WHERE `id` = 0"
                cursor.execute(sql)
                temp = cursor.fetchone()
                winner_info = acc.users.get(user_ids=winner[1], name_case='acc')
                acc.wall.delete(owner_id=-198251975, post_id=temp[3])
                tmp = acc.wall.post(owner_id=-198251975, from_group=1, message=f"поздравляем пользователя [id{winner[1]}|{winner_info[0]['first_name']} {winner_info[0]['last_name']}] с выигрышем ${formatnum(prize)}!", close_comments=1)
                sql = f"UPDATE acc SET `state` = 'open', `dop` = '{tmp['post_id']}' WHERE `id` = 0"
                cursor.execute(sql)
                conn.commit()
            a2 = True
        elif time.strftime('%H:%M') == '18:40':
            a1 = False
            a2 = False


def formatnum(number):
    b = ''
    j = 0
    c = ''
    for i in reversed(str(number)):
        if j == 3:
            b = b + '.'
            j = 0
        b = b + i
        j = j + 1
    for i in reversed(b):
        c = c + i
    return c

dep = threading.Thread(target=main)
post = threading.Thread(target=posting)
dep.start()
post.start()