import os
import xlwt
import xlrd
from materials import constants
import datetime


class Mxl:
    def __init__(self):
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 2
        font0.height = 400
        font0.bold = True

        self.font0 = font0

        style0 = xlwt.XFStyle()
        style0.font = font0

        self.style0 = style0

        font1 = xlwt.Font()
        font1.name = 'Times New Roman'
        font1.height = 300

        self.font1 = font1

        style1 = xlwt.XFStyle()
        style1.font = font1

        self.style1 = style1

        self.date = datetime.date.today().strftime("%d.%m.%Y")

        # Если таблица была до этого
        if os.path.exists(constants.dir):
            self.users = []
            self.tags = []
            self.ids = []

            rb = xlrd.open_workbook(constants.dir, formatting_info=True)
            sheet = rb.sheet_by_index(0)

            for tag in sheet.row_values(0):
                self.tags.append(tag)
            # Считываем данные из таблицы
            lis = self.tags
            for i in range(1, sheet.nrows):
                self.ids.append(int(sheet.row_values(i)[1]))
                j = 0
                user = {}
                for col in sheet.row_values(i):
                    l = lis[j]
                    user[l] = col
                    j += 1
                self.users.append(user)

            # Преобразование тегов
            self.tags = self.tags[7:-1]
            for tag in constants.key_words:
                if not tag in self.tags:
                    self.tags.append(tag)

        self.wb = xlwt.Workbook()

        ws = self.wb.add_sheet('Users', cell_overwrite_ok=True)

        ws.write(0, 0, "Дата", style0)
        ws.write(0, 1, "ID", style0)
        ws.write(0, 2, "Имя", style0)
        ws.write(0, 3, "Фамилия", style0)
        ws.write(0, 4, "Телефон", style0)
        ws.write(0, 5, "Дата рождения", style0)
        ws.write(0, 6, "Город", style0)

        i = 7
        if os.path.exists(constants.dir):
            for tag in self.tags:
                ws.write(0, i, tag, style0)
                i += 1
        else:
            for tag in constants.key_words:
                ws.write(0, i, tag, style0)
                i += 1

        ws.write(0, i, "Статус 1 или 0", style0)

        self.ws = ws

    def sort_pars(self):
        ans = []
        for user in constants.users:
            if not user['id'] in self.ids:
                ans.append(user)
            else:
                for i in range(0, len(self.ids) - 1):
                    if user['id'] == self.ids[i]:
                        for tag in constants.users_tags[self.ids[i]]:
                            self.users[i][tag] = tag
                        break
        constants.users = ans

    def write_start_info(self, pers, i):
        self.ws.write(i, 0, self.date, self.style1)
        self.ws.write(i, 1, str(pers['id']), self.style1)
        self.ws.write(i, 2, pers['first_name'], self.style1)
        self.ws.write(i, 3, pers['last_name'], self.style1)
        if 'mobile_phone' in pers.keys():
            self.ws.write(i, 4, pers['mobile_phone'], self.style1)
        else:
            self.ws.write(i, 4, "-", self.style1)

        if 'bdate' in pers.keys():
            self.ws.write(i, 5, pers['bdate'], self.style1)
        else:
            self.ws.write(i, 5, "-")

        self.ws.write(i, 6, pers['city']['title'], self.style1)

    def addUsers(self):
        if not os.path.exists(constants.dir):
            i = 1
            style1 = self.style1
            for pers in constants.users:
                self.write_start_info(pers, i)
                j = 7
                for tag in constants.key_words:
                    if tag in constants.users_tags[pers['id']]:
                        self.ws.write(i, j, tag, style1)
                    else:
                        self.ws.write(i, j, "-", style1)
                    j += 1

                self.ws.write(i, j, "0", style1)
                i += 1

        else:
            self.sort_pars()
            i = 1
            style1 = self.style1
            for user in constants.users:
                self.write_start_info(user, i)
                j = 7
                for tag in self.tags:
                    if tag in constants.users_tags[user['id']]:
                        self.ws.write(i, j, tag, style1)
                    else:
                        self.ws.write(i, j, "-", style1)
                    j += 1
                self.ws.write(i, j, "0", style1)
                i += 1
            for user in self.users:
                self.ws.write(i, 0, user['Дата'], self.style1)
                self.ws.write(i, 1, user['ID'], self.style1)
                self.ws.write(i, 2, user['Имя'], self.style1)
                self.ws.write(i, 3, user['Фамилия'], self.style1)
                self.ws.write(i, 4, user['Телефон'], self.style1)
                self.ws.write(i, 5, user['Дата рождения'], self.style1)
                self.ws.write(i, 6, user['Город'], self.style1)
                j = 7
                for tag in self.tags:
                    if tag in user.keys():
                        self.ws.write(i, j, user[tag], style1)
                    else:
                        self.ws.write(i, j, "-", style1)
                    j += 1
                self.ws.write(i, j, user['Статус 1 или 0'], style1)
                i += 1

    def write(self):
        self.wb.save(constants.dir)
