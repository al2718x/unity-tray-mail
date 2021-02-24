#!/usr/bin/env python3

import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import AppIndicator3
# import signal
import subprocess


class MyIndicator:
    # processes = []

    def __init__(self):
        # noinspection PyArgumentList
        self.ind = AppIndicator3.Indicator.new(
            'Thunderbird Indicator 1.0.0',
            'indicator-messages',
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon('new-messages-red')
        # self.ind.set_label('email', 'email')
        self.menu = Gtk.Menu()

        # item = Gtk.MenuItem()
        # item.set_label('Electron Mail')
        # item.connect('activate', self.run, './ElectronMail.sh')
        # self.menu.append(item)
        #
        # item = Gtk.MenuItem()
        # item.set_label('Delta Chat')
        # item.connect('activate', self.run, './DeltaChat.sh')
        # self.menu.append(item)

        self.menu_item('Thunderbird', 'thunderbird', 'thunderbird')
        self.menu_item('Compose', 'stock_mail-compose', ['thunderbird', '-compose'])
        self.menu_item('Address Book', 'stock_addressbook', ['thunderbird', '-addressbook'])
        self.menu_item('Calendar', 'org.gnome.Calendar', 'gnome-calendar')
        self.menu_item('Quit', 'application-exit')

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def menu_item(self, label, icon_name, connect_args=None):
        item = Gtk.ImageMenuItem()
        img = Gtk.Image()
        img.set_from_icon_name(icon_name, 16)
        item.set_image(img)
        item.set_always_show_image(True)
        item.set_label(label)
        if connect_args:
            item.connect('activate', self.run, connect_args)
        else:
            item.connect('activate', self.quit)
        self.menu.append(item)

    def main(self):
        Gtk.main()

    def run(self, widget, param):
        self.ind.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
        # subprocess.run(['thunderbird'])
        subprocess.Popen(param)
        # p = subprocess.Popen(param)
        # self.processes.append(p)
        # print('pid=', p.pid)
        GLib.timeout_add_seconds(1, self.ind.set_status, AppIndicator3.IndicatorStatus.ACTIVE)

    def quit(self, widget):
        # for pid in self.processes:
        #     if isinstance(pid, subprocess.Popen):
        #         pid.send_signal(sig=signal.SIGTERM)
        Gtk.main_quit()


if __name__ == '__main__':
    indicator = MyIndicator()
    indicator.main()
