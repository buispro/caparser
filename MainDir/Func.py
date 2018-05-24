from pars.CAPars import CAPars
from pars.Mxl import Mxl

ca = 0
window = 0


def start_pars():
    global ca
    if type(ca) is int:
        ca = CAPars()
        if ca.p:
            ca.start()
        else:
            ca = 0


def save_pars():
    global ca
    ca = 100
    mxl = Mxl()
    mxl.addUsers()
    mxl.write()


def set_window(wind):
    global window
    window = wind


def show_message(text):
    window.show_message(text)


def say_perc():
    global ca
    if not type(ca) is int:
        return ca.get_percent()
    else:
        return ca
