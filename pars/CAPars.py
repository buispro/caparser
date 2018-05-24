import vk_api
from materials import constants
import time
import threading
from MainDir import Func


class CAPars:

    def __init__(self):
        self.groups = {}
        self.percent = 0
        self.p = True
        try:
            self.vk = vk_api.VkApi(login=constants.login, password=constants.password,
                                   captcha_handler=self.captcha_handler)
            self.vk.auth()
        except Exception as e:
            print(e)
            Func.show_message("Ошибка при авторизации")
            self.p = False

    def captcha_handler(*captcha):
        captcha = captcha[1]
        key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
        return captcha.try_again(key)

    # Запускаем поток парсинга
    def start(self):
        t = threading.Thread(target=self.thr_method)
        t.daemon = True
        t.start()

    # Получаем группы
    def get_groups(self):
        for word in constants.key_words:
            try:
                pars = self.vk.method("groups.search", {'q': word, 'sort': 0})
            except Exception as e:
                print(e)
                Func.show_message("Ошибка при парсинге группы")
                exit(0)
            for group in pars['items']:
                if not group['id'] in self.groups.keys():
                    self.groups[group['id']] = []
                    self.groups[group['id']].append(word)
                else:
                    self.groups[group['id']].append(word)

    # Получаем ца
    def get_ca(self, id):
        try:
            pars = self.vk.method("groups.getMembers", {'group_id': id, 'fields': 'bdate, contacts, city', 'count': 0})
        except Exception as e:
            print(e)
            Func.show_message("Ошибка при парсинге ца")
            exit(0)
        count = pars['count']
        limit = 1000
        packet = 0
        while limit * packet < count:
            try:
                pars = self.vk.method("groups.getMembers",
                                      {'group_id': id, 'fields': 'bdate, contacts, city', 'offset': limit * packet})
            except Exception as e:
                print(e)
                Func.show_message("Ошибка при парсинге ца")
                exit(0)
            for user in pars['items']:
                if user not in constants.users:
                    if 'city' in user.keys() and user['city']['title'] in constants.cities:
                        constants.users.append(user)
                        constants.users_tags[user['id']] = []
                        constants.users_tags[user['id']].append(self.groups[id])
                else:
                    constants.users_tags[user['id']].append(self.groups[id])
            packet += 1

    def sort_tags(self):
        for key in constants.users_tags.keys():
            ans = []
            for list in constants.users_tags[key]:
                for word in list:
                    if not word in ans:
                        ans.append(word)
                        constants.users_tags[key] = ans

    def sort_users(self):
        bmas = []
        tmas = []
        omas = []
        for user in constants.users:
            if 'bdate' in user.keys() and len(user['bdate'].split('.')) == 3:
                tyear = int(user['bdate'].split('.')[2])
                if tyear >= constants.year:
                    bmas.append(user)
            elif 'mobile_phone' in user.keys() and len(user['mobile_phone']) > 2:
                tmas.append(user)
            else:
                omas.append(user)
        return bmas + tmas + omas

    def get_percent(self):
        return self.percent

    def thr_method(self):
        self.get_groups()
        j = 1
        size = len(self.groups)
        for group in self.groups.keys():
            self.get_ca(group)
            self.percent = j / size * 100
            j += 1
            time.sleep(0.6)
            constants.set_users(self.sort_users())
        self.sort_tags()
        Func.save_pars()
