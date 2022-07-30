from mysql.connector import connect, Error

try:
    with connect(
        host="CryPack.mysql.pythonanywhere-services.com",
        user="CryPack",
        password="IamCool123",
        database="CryPack$bot"
    ) as connection:
        print(connection)
except Error as e:
    print(e)