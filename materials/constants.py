login = ""
password = ""
year = 2002
dir = ""

cities = []
key_words = []

users = []
users_tags = {}


def set_users(mas):
    global users
    users = mas


def first_method():
    f1 = open('cities.txt', 'r')
    for city in f1.read().split('\n'):
        if city:
            cities.append(city)
    f1.close()

    f2 = open('tags.txt', 'r')
    for key in f2.read().split('\n'):
        if key:
            key_words.append(key)
    f2.close()

    f3 = open('dir.txt', 'r')
    global dir
    dir = f3.read()
    f3.close()

    f4 = open('vk.txt', 'r')
    global login, password
    login, password = f4.read().split("\n")
    f4.close()


def del_city(city):
    cities.remove(city)


def del_key(key):
    key_words.remove(key)


def set_year(a):
    global year
    year = a


def save():
    f1 = open('cities.txt', 'w')
    for city in cities:
        f1.write(city + "\n")
    f1.close()

    f2 = open('tags.txt', 'w')
    for key in key_words:
        f2.write(key + "\n")
    f2.close()
