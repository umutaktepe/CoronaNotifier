#!/usr/bin/python3

import notify2
from bs4 import BeautifulSoup
import requests
import time


class CoronaTrack:

    def __init__(self):

        self.country = input("Which Country to Track: ").capitalize()
        self.notif_duration = int(input("Notification Duration in Seconds: "))
        self.refresh_notif = int(input("Notification Interval in Minutes: "))
        self.url = "https://www.worldometers.info/coronavirus/"
        self.data_check = []
        self.getdata()

    def getdata(self):

        global message, data_check, data

        while True:

            try:
                html_page = requests.get(self.url)
            except requests.exceptions.RequestException as e:
                print(e)
                continue

            bs = BeautifulSoup(html_page.content, 'html.parser')

            search = bs.select("div tbody tr td")
            start = -1

            for i in range(len(search)):
                if search[i].get_text().find(self.country) != -1:
                    start = i
                    break

            data = []

            for i in range(1, 8):
                try:
                    data = data + [search[start+i].get_text()]
                except:
                    data = data + ["0"]

            message = "Total Infected = {}\nNew Case = {}\nTotal Deaths = {}\nNew Deaths = {}\nRecovered = {}\nActive Case = {}\nSerious Critical = {}".format(*data)

            self.notify()

    def notify(self):

        ICON_PATH = "icon/coronavirus.png"

        notify2.init("Coronavirus Notifier")

        n = notify2.Notification("Coronavirus Notifier", icon=ICON_PATH)
        n.set_urgency(notify2.URGENCY_NORMAL)
        n.set_timeout(self.notif_duration * 1000)
        n.update(summary="CORONAVIRUS NOTIFIER FOR {}\n".format(self.country.upper()), message=message, icon=ICON_PATH)
        n.show()
        time.sleep(self.refresh_notif * 60)

        if self.data_check != data:                     # Show notification if data have changed

            notify2.init("Coronavirus Notifier")

            n = notify2.Notification("Coronavirus Notifier", icon=ICON_PATH)
            n.set_urgency(notify2.URGENCY_NORMAL)
            n.set_timeout(self.notif_duration*1000)
            n.update(summary="CORONAVIRUS NOTIFIER FOR {}\n".format(self.country.upper()), message=message, icon=ICON_PATH)
            n.show()
            time.sleep(self.refresh_notif * 60)

        else:
            time.sleep(self.refresh_notif*60)


if __name__ == "__main__":
    CoronaTrack()





