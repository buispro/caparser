import sys
import threading

from PyQt5.QtWidgets import *
from MainDir import Func
from gui import design
from materials.constants import *
import time


class UI:

    def __init__(self):
        app = QApplication(sys.argv)  # Новый экземпляр QApplication
        window = self.ExampleApp()  # Создаём объект класса ExampleApp
        window.fill_lists()
        window.show()  # Показываем окно
        Func.set_window(window)
        app.exec_()  # и запускаем приложение

    class ExampleApp(QMainWindow, design.Ui_MainWindow):

        def __init__(self):
            # Это здесь нужно для доступа к переменным, методам
            # и т.д. в файле design.py
            super().__init__()
            self.setupUi(self)  # Это нужно для инициализации нашего дизайна
            self.startButton.clicked.connect(self.save_and_start)
            self.addButton1.clicked.connect(self.addTag1)
            self.delButton1.clicked.connect(self.delTag1)
            self.addButton2.clicked.connect(self.addTag2)
            self.delButton2.clicked.connect(self.delTag2)

        def save_and_start(self):
            set_year(int(self.yearBox.text()))
            save()
            Func.start_pars()
            self.progressBar.setValue(0)
            t = threading.Thread(target=self.thr_method)
            t.daemon = True
            t.start()

        def thr_method(self):
            perc = Func.say_perc()
            while perc <= 100:
                perc = Func.say_perc()
                self.setProgress(perc)
                if perc == 100:
                    break
                time.sleep(1)

        def setProgress(self, perc):
            self.progressBar.setValue(perc)

        def addTag1(self):
            tag = self.editText1.toPlainText()
            if tag:
                key_words.append(tag)
                self.keyTags.addItem(QListWidgetItem(tag))

        def addTag2(self):
            city = self.editText2.toPlainText()
            if city:
                cities.append(city)
                self.cityTags.addItem(QListWidgetItem(city))

        def delTag1(self):
            tag = self.keyTags.takeItem(self.keyTags.currentRow())
            del_key(tag.text())
            del tag

        def delTag2(self):
            city = self.cityTags.takeItem(self.cityTags.currentRow())
            del_city(city.text())
            del city

        def show_message(self, text):
            QMessageBox.critical(self, "Ошибка :(", text)

        def fill_lists(self):
            for key in key_words:
                self.keyTags.addItem(QListWidgetItem(key))
            for city in cities:
                self.cityTags.addItem(QListWidgetItem(city))
