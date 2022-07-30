import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import sqlite3
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import time
import threading

adminkey = VkKeyboard(False)
adminkey.add_button('посмотреть заявки на вывод', VkKeyboardColor.PRIMARY, '{"admin_menu":"withdraws"}')
adminkey.add_line()
adminkey.add_button('выбрать рандома', VkKeyboardColor.PRIMARY, '{"admin_menu":"random"}')
adminkey.add_line()
adminkey.add_button('выход', VkKeyboardColor.SECONDARY, '{"admin_menu":"exit"}')

lotterykey = VkKeyboard(False)
lotterykey.add_button('купить билет "мини босс"', VkKeyboardColor.PRIMARY, '{"lottery_menu":"buy1"}')
lotterykey.add_button('купить билет "босс"', VkKeyboardColor.PRIMARY, '{"lottery_menu":"buy2"}')
lotterykey.add_line()
lotterykey.add_button('выход', VkKeyboardColor.SECONDARY, '{"lottery_menu":"exit"}')

admmainkey = VkKeyboard(False)
admmainkey.add_button('распродажа', VkKeyboardColor.PRIMARY, '{"main_menu":"sale"}')
admmainkey.add_button('лотерея', VkKeyboardColor.PRIMARY, '{"main_menu":"lottery"}')
admmainkey.add_button('ломбард', VkKeyboardColor.PRIMARY, '{"main_menu":"pawnshop"}')
admmainkey.add_line()
admmainkey.add_button('пополнить', VkKeyboardColor.SECONDARY, '{"main_menu":"deposit"}')
admmainkey.add_button('помощь', VkKeyboardColor.SECONDARY, '{"main_menu":"help"}')
admmainkey.add_button('вывод', VkKeyboardColor.SECONDARY, '{"main_menu":"withdraw"}')
admmainkey.add_line()
admmainkey.add_button('админка', VkKeyboardColor.SECONDARY, '{"main_menu":"admin_menu"}')

mainkey = VkKeyboard(False)
mainkey.add_button('распродажа', VkKeyboardColor.PRIMARY, '{"main_menu":"sale"}')
mainkey.add_button('лотерея', VkKeyboardColor.PRIMARY, '{"main_menu":"lottery"}')
mainkey.add_button('ломбард', VkKeyboardColor.PRIMARY, '{"main_menu":"pawnshop"}')
mainkey.add_line()
mainkey.add_button('пополнить', VkKeyboardColor.SECONDARY, '{"main_menu":"deposit"}')
mainkey.add_button('помощь', VkKeyboardColor.SECONDARY, '{"main_menu":"help"}')
mainkey.add_button('вывод', VkKeyboardColor.SECONDARY, '{"main_menu":"withdraw"}')

vk_session1 = vk_api.VkApi(token='836b224a9cb082af2bf804c598fc7e8b45274bfa5e533a45dfec4797b58139c59204cd0f53fe11be183aa')
acc = vk_session1.get_api()
longpoll1 = VkLongPoll(vk_session1)

vk_session = vk_api.VkApi(token='6a22339594750300f27b35460ff7658133f780405aea001db0b67bbdb2b84a91db2f112371d789028c255')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 198251975)

a1 = False
a2 = False

def lottery_buy1(user_id, user_data, object):
    global amount, err
    err = False
    if 'payload' in object.message:
        if object.message['payload'] == '{"lottery_buy":"exit"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"UPDATE acc SET `state` = 'lottery_menu' WHERE `id` = {user_id}"
            cursor.execute(sql)
            sql = f"SELECT * FROM tickets1 WHERE `id` = {user_id}"
            cursor.execute(sql)
            tickets1 = len(cursor.fetchall())
            sql = f"SELECT * FROM tickets2 WHERE `id` = {user_id}"
            cursor.execute(sql)
            tickets2 = len(cursor.fetchall())
            conn.commit()
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'ты в меню лотереи!<br>твой баланс - ${formatnum(user_data[1])}<br>кол-во твоих билетов "мини босс" - {formatnum(tickets1)}<br>кол-во твоих билетов "босс" - {formatnum(tickets2)}', keyboard=lotterykey.get_keyboard())
    else:
        amount = ''
        for i in object.message['text'].lower():
            if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '0':
                amount = amount + i
            elif i == 'к' or i == 'k':
                amount = int(amount) * 1000
            else:
                err = True
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! не указанно количество билетов')
                break
        if not err:
            total = int(amount) * 1000
            if user_data[1] >= int(total):
                query = ''
                for i in range(int(amount)):
                    query = query + f"INSERT INTO tickets1(`user_id`) VALUES ({user_id});"
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                cursor.executescript(query)
                sql = f"UPDATE acc SET `money` = {user_data[1] - total}, `state` = 'main_menu' WHERE `id` = {user_id}"
                cursor.execute(sql)
                conn.commit()
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'ты успешно купил {formatnum(amount)} билетов "мини босс" за ${formatnum(total)}! розыгрыш билетов происходит каждый день в 10:00 по МСК<br><br>баланс - ${formatnum(user_data[1] - total)}', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
            else:
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! недостаточно денег')
        err = False

def lottery_buy2(user_id, user_data, object):
    global amount, err
    err = False
    if 'payload' in object.message:
        if object.message['payload'] == '{"lottery_buy":"exit"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"UPDATE acc SET `state` = 'lottery_menu' WHERE `id` = {user_id}"
            cursor.execute(sql)
            sql = f"SELECT * FROM tickets1 WHERE `id` = {user_id}"
            cursor.execute(sql)
            tickets1 = len(cursor.fetchall())
            sql = f"SELECT * FROM tickets2 WHERE `id` = {user_id}"
            cursor.execute(sql)
            tickets2 = len(cursor.fetchall())
            conn.commit()
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'ты в меню лотереи!<br>твой баланс - ${formatnum(user_data[1])}<br>кол-во твоих билетов "мини босс" - {formatnum(tickets1)}<br>кол-во твоих билетов "босс" - {formatnum(tickets2)}', keyboard=lotterykey.get_keyboard())
    else:
        amount = ''
        for i in object.message['text'].lower():
            if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '0':
                amount = amount + i
            elif i == 'к' or i == 'k':
                amount = int(amount) * 1000
            else:
                err = True
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! не указанно количество билетов')
                break
        if not err:
            total = int(amount) * 1000
            if user_data[1] >= int(total):
                query = ''
                for i in range(int(amount)):
                    query = query + f"INSERT INTO tickets2(`user_id`) VALUES ({user_id});"
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                cursor.executescript(query)
                sql = f"UPDATE acc SET `money` = {user_data[1] - total}, `state` = 'main_menu' WHERE `id` = {user_id}"
                cursor.execute(sql)
                conn.commit()
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'ты успешно купил {formatnum(amount)} билетов "босс" за ${formatnum(total)}! розыгрыш билетов происходит каждый день в 10:00 по МСК<br><br>баланс - ${formatnum(user_data[1] - total)}', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
            else:
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! недостаточно денег')
        err = False

def lottery_menu(user_id, user_data, object):
    if 'payload' in object.message:
        if object.message['payload'] == '{"lottery_menu":"buy2"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = "SELECT * FROM acc WHERE `id` = 0"
            cursor.execute(sql)
            res = cursor.fetchone()
            conn.commit()
            if res[2] == 'open':
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                sql = f"UPDATE acc SET `state` = 'lottery_buy2' WHERE `id` = {user_id}"
                cursor.execute(sql)
                conn.commit()
                key = VkKeyboard(False)
                key.add_button('выход', VkKeyboardColor.SECONDARY, '{"lottery_buy":"exit"}')
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'стоймость одного билета - $1.000, напиши, сколько билетов ты хочешь купить<br><br>баланс - ${formatnum(user_data[1])}', keyboard=key.get_keyboard())
        elif object.message['payload'] == '{"lottery_menu":"buy1"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = "SELECT * FROM acc WHERE `id` = 0"
            cursor.execute(sql)
            res = cursor.fetchone()
            conn.commit()
            if res[2] == 'open':
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                sql = f"UPDATE acc SET `state` = 'lottery_buy1' WHERE `id` = {user_id}"
                cursor.execute(sql)
                conn.commit()
                key = VkKeyboard(False)
                key.add_button('выход', VkKeyboardColor.SECONDARY, '{"lottery_buy":"exit"}')
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'стоймость одного билета - $1.000, напиши, сколько билетов ты хочешь купить<br><br>баланс - ${formatnum(user_data[1])}', keyboard=key.get_keyboard())
            else:
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='покупка билетов закрыта, так как скоро будет выбран счастливый билет')
        elif object.message['payload'] == '{"lottery_menu":"exit"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"UPDATE acc SET `state` = 'main_menu' WHERE `id` = {user_id}"
            cursor.execute(sql)
            conn.commit()
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'ты в главном меню!<br>твой баланс - ${formatnum(user_data[1])}', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())

    else:
        vk.messages.send(user_id=user_id, random_id=get_random_id(), message='используй кнопки!', keyboard=lotterykey.get_keyboard())

def withdraw_menu(user_id, user_data, object):
    err = False
    if 'payload' in object.message:
        if object.message['payload'] == '{"withdraw_menu":"exit"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"UPDATE acc SET `state` = 'main_menu' WHERE `id` = {user_id}"
            cursor.execute(sql)
            conn.commit()
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'ты в главном меню!<br>твой баланс - ${formatnum(user_data[1])}', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
    else:
        amount = ''
        for i in object.message['text'].lower():
            if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '0':
                amount = amount + i
            elif i == 'к' or i == 'k':
                amount = int(amount) * 1000
            else:
                err = True
                vk.messages.send(user_id=user_id, random_id=get_random_id(),
                                 message='ошибка! не указана сумма')
                break
        if not err:
            if user_data[1] >= int(amount):
                comission = round(amount * 0.03)
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                sql = f"UPDATE acc SET `money` = {user_data[1] - amount}, `state` = 'main_menu' WHERE `id` = {user_id}"
                cursor.execute(sql)
                sql = f"INSERT INTO withdraws(`user_id`,`money`) VALUES ({user_id}, {amount - comission})"
                cursor.execute(sql)
                conn.commit()
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'деньги успешно попали на вывод, как только админ проверит заявку, деньги поступят на твой счёт<br><br>баланс - ${formatnum(user_data[1] - amount)}', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
            else:
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! недостаточно денег')
        err = False

def admin_menu(user_id, user_data, object):
    err = False
    text = object.message['text'].split()
    if 'payload' in object.message:
        if object.message['payload'] == '{"admin_menu":"exit"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"UPDATE acc SET `state` = 'main_menu' WHERE `id` = {user_id}"
            cursor.execute(sql)
            conn.commit()
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'ты в главном меню!<br>твой баланс - ${formatnum(user_data[1])}', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
        elif object.message['payload'] == '{"admin_menu":"random"}':
            res = acc.groups.getMembers(group_id=213708822)
            tmp = random.randint(1, res['count'])
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f"вот рандомный челик: @id{res['items'][tmp-1]}")
        elif object.message['payload'] == '{"admin_menu":"withdraws"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = "SELECT * FROM withdraws"
            cursor.execute(sql)
            tickets = cursor.fetchall()
            conn.commit()
            if len(tickets) == 0:
                mess = 'заявок на вывод нет'
            else:
                mess = 'вот заявки на вывод:<br>'
                for i in tickets:
                    mess = mess + f"<br>{i[0]} | @id{i[1]} | ${formatnum(i[2])}"
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=mess)
    elif text[0] == 'отклонить' or text[0] == 'Отклонить':
        for i in text[1]:
            if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '0':
                continue
            else:
                err = True
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! не указан id заявки')
                break
        if not err:
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"SELECT * FROM withdraws WHERE `id` = {text[1]}"
            cursor.execute(sql)
            temp = cursor.fetchone()
            if temp == None:
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! заявка не найдена')
            else:
                sql = f"DELETE FROM withdraws WHERE `id` = {text[1]}"
                cursor.execute(sql)
                conn.commit()
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='заявка отклонена!')
    elif text[0] == 'Одобрить' or text[0] == 'одобрить':
        for i in text[1]:
            if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '0':
                continue
            else:
                err = True
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! не указан id заявки')
                break
        if not err:
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"SELECT * FROM withdraws WHERE `id` = {text[1]}"
            cursor.execute(sql)
            temp = cursor.fetchone()
            if temp == None:
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! заявка не найдена')
            else:
                sql = f"DELETE FROM withdraws WHERE `id` = {text[1]}"
                cursor.execute(sql)
                conn.commit()
                acc.messages.send(user_id=-166948584, random_id=get_random_id(), message=f"передать @id{temp[1]} {temp[2]}")
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message='заявка одобрена!')
    elif text[0] == '/sql':
        if len(text) > 1:
            command = ' '.join(text)
            command = command.replace('/sql ', '')
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = command.replace('”', '"')
            sql = sql.replace('“', '"')
            sql = sql.replace("’", "'")
            sql = sql.replace('^', '`')
            try:
                cursor.execute(sql)
                res = cursor.fetchall()
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f"вывод: {res}")
            except sqlite3.Error as e:
                vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f"Error: {e}")
            conn.commit()
        else:
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ошибка! нет аргумента')
    else:
        vk.messages.send(user_id=user_id, random_id=get_random_id(), message='используй кнопки!', keyboard=adminkey.get_keyboard())

def main_menu(user_id, user_data, object):
    if 'payload' in object.message:
        if object.message['payload'] == '{"main_menu":"lottery"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"UPDATE acc SET `state` = 'lottery_menu' WHERE `id` = {user_id}"
            cursor.execute(sql)
            sql = f"SELECT * FROM tickets1 WHERE `user_id` = {user_id}"
            cursor.execute(sql)
            tickets1 = len(cursor.fetchall())
            sql = f"SELECT * FROM tickets2 WHERE `user_id` = {user_id}"
            cursor.execute(sql)
            tickets2 = len(cursor.fetchall())
            conn.commit()
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'ты в меню лотереи!<br>твой баланс - ${formatnum(user_data[1])}<br>кол-во твоих билетов "мини босс" - {formatnum(tickets1)}<br>кол-во твоих билетво "босс" - {formatnum(tickets2)}', keyboard=lotterykey.get_keyboard())
        elif object.message['payload'] == '{"main_menu":"deposit"}':
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message='чтобы пополнить баланс, нужно передать на аккаунт @evgphonk сумму для пополнения. пример: "передать @evgphonk 1ккк', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
        elif object.message['payload'] == '{"main_menu":"help"}':
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message='помощь)', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
        elif object.message['payload'] == '{"main_menu":"withdraw"}':
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"UPDATE acc SET `state` = 'withdraw_menu' WHERE `id` = {user_id}"
            cursor.execute(sql)
            conn.commit()
            key = VkKeyboard(False)
            key.add_button('выход', VkKeyboardColor.SECONDARY, '{"withdraw_menu":"exit"}')
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message=f'напиши сколько ты хочешь вывести (от суммы вывода будет взята комиссия в размере 3%)<br><br>баланс - ${formatnum(user_data[1])}', keyboard=key.get_keyboard())
        elif object.message['payload'] == '{"main_menu":"admin_menu"}' and user_data[4] == 1:
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"UPDATE acc SET `state` = 'admin_menu' WHERE `id` = {user_id}"
            cursor.execute(sql)
            conn.commit()
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message='ты в меню админки', keyboard=adminkey.get_keyboard())
        elif object.message['payload'] == '{"main_menu":"sale"}' or object.message['payload'] == '{"main_menu":"pawnshop"}':
            vk.messages.send(user_id=user_id, random_id=get_random_id(), message='в разработке', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
    elif object.message['text'] == 'тест':
        vk.messages.send(user_id=user_id, random_id=get_random_id(), message='test)', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())
    else:
        vk.messages.send(user_id=user_id, random_id=get_random_id(), message='используй кнопки!', keyboard=admmainkey.get_keyboard() if user_data[4] == 1 else mainkey.get_keyboard())

def main():
    print('Main thread started')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.object.message['from_id']
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"SELECT * FROM acc WHERE `id` = {user_id}"
            cursor.execute(sql)
            temp = cursor.fetchall()
            conn.commit()
            if len(temp) == 0:
                conn = sqlite3.connect("bot.db")
                cursor = conn.cursor()
                sql = f"INSERT INTO acc VALUES ({user_id}, 0, 'main_menu', '0', 0)"
                cursor.execute(sql)
                conn.commit()
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"SELECT * FROM acc WHERE `id` = {user_id}"
            cursor.execute(sql)
            user_data = cursor.fetchone()
            conn.commit()
            if user_data[2] == 'main_menu':
                main_menu(user_id, user_data, event.object)
            elif user_data[2] == 'lottery_menu':
                lottery_menu(user_id, user_data, event.object)
            elif user_data[2] == 'lottery_buy1':
                lottery_buy1(user_id, user_data, event.object)
            elif user_data[2] == 'lottery_buy2':
                lottery_buy2(user_id, user_data, event.object)
            elif user_data[2] == 'withdraw_menu':
                withdraw_menu(user_id, user_data, event.object)
            elif user_data[2] == 'admin_menu':
                admin_menu(user_id, user_data, event.object)

def deposit():
    print('Deposit thread started')
    for event in longpoll1.listen():
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
        if time.strftime('%H:%M') == '06:55' and a1 == False:
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            sql = f"SELECT * FROM acc WHERE `id` = 0"
            cursor.execute(sql)
            temp = cursor.fetchone()
            acc.wall.delete(owner_id=-198251975, post_id=temp[3])
            tmp = acc.wall.post(owner_id=-198251975, from_group=1, message='покупка билетов закрывается так как через 5 минут будет выбран счастливый билет!', close_comments=1)
            sql = f"UPDATE acc SET `state` = 'close', `dop` = '{tmp['post_id']}' WHERE `id` = 0"
            cursor.execute(sql)
            conn.commit()
            a1 = True
        elif time.strftime('%H:%M') == '07:00' and a2 == False:
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
                sql = f"UPDATE acc SET `money` = {user_data[1] + prize} WHERE `id` = {user_data[0]}"
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
        elif time.strftime('%H:%M') == '07:01':
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

dep = threading.Thread(target=deposit)
post = threading.Thread(target=posting)
#dep.start()
#post.start()
main()