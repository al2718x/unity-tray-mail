#!/usr/bin/env python3

import subprocess
import gi.repository

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import AppIndicator3


class MyIndicator:
    def __init__(self):
        # noinspection PyArgumentList
        self.ind = AppIndicator3.Indicator.new(
            'Thunderbird Indicator 1.0.2',
            'indicator-messages',
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon('new-messages-red')
        self.menu = Gtk.Menu()
        self.menu_item('Thunderbird', 'thunderbird', self.run, 'thunderbird')
        self.menu_item_f(
            'Tuta Mail',
            '/home/al/.local/share/icons/hicolor/16x16/apps/tutanota-desktop.png',
            self.run,
            '/home/al/tutanota/tutanota-desktop-linux.AppImage'
        )
        self.menu_item('Compose', 'stock_mail-compose', self.run, ['thunderbird', '-compose'])
        self.menu_item('Address Book', 'stock_addressbook', self.run, ['thunderbird', '-addressbook'])
        self.menu_item('Calendar', 'org.gnome.Calendar', self.run, 'gnome-calendar')
        self.menu_item('Quit', 'application-exit', self.quit)
        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def menu_item_f(self, label, icon_file, action, args=None):
        img = Gtk.Image.new_from_file(icon_file)
        item = Gtk.ImageMenuItem()
        item.set_image(img)
        item.set_always_show_image(True)
        item.set_label(label)
        if args:
            item.connect('activate', action, args)
        else:
            item.connect('activate', action)
        self.menu.append(item)

    def menu_item(self, label, icon_name, action, args=None):
        img = Gtk.Image().new_from_icon_name(icon_name, Gtk.IconSize.MENU)
        item = Gtk.ImageMenuItem()
        item.set_image(img)
        item.set_always_show_image(True)
        item.set_label(label)
        if args:
            item.connect('activate', action, args)
        else:
            item.connect('activate', action)
        self.menu.append(item)

    def run(self, widget, param):
        self.ind.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
        subprocess.Popen(param)
        GLib.timeout_add_seconds(1, self.ind.set_status, AppIndicator3.IndicatorStatus.ACTIVE)

    def quit(self, widget):
        Gtk.main_quit()

    def main(self):
        Gtk.main()


if __name__ == '__main__':
    indicator = MyIndicator()
    indicator.main()
