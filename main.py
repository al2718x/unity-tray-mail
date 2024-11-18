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
        self.menu_item('Thunderbird', icon_name='thunderbird', args='thunderbird')
        self.menu_item(
            'Tuta Mail',
            icon_file='/home/al/.local/share/icons/hicolor/16x16/apps/tutanota-desktop.png',
            args=['/home/al/tutanota/tutanota-desktop-linux.AppImage']
        )
        self.menu_item(
            'Electron Mail',
            icon_name='com.github.vladimiry.ElectronMail',
            args=['flatpak', 'run', 'com.github.vladimiry.ElectronMail']
        )
        self.menu_item(
            'Delta Chat',
            icon_name='chat.delta.desktop',
            args=['flatpak', 'run', 'chat.delta.desktop']
        )
        self.menu_item('Compose', icon_name='stock_mail-compose', args=['thunderbird', '-compose'])
        self.menu_item('Address Book', icon_name='stock_addressbook', args=['thunderbird', '-addressbook'])
        self.menu_item('Calendar', icon_name='org.gnome.Calendar', args=['gnome-calendar'])
        self.menu_item('Quit', icon_name='application-exit', action=self.quit)
        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def menu_item(self, label, *, icon_name=None, icon_file=None, action=None, args=None):
        item = Gtk.ImageMenuItem()
        item.set_label(label)
        if icon_name:
            img = Gtk.Image().new_from_icon_name(icon_name, Gtk.IconSize.MENU)
            item.set_image(img)
            item.set_always_show_image(True)
        elif icon_file:
            img = Gtk.Image.new_from_file(icon_file)
            item.set_image(img)
            item.set_always_show_image(True)
        _action = self.run if None == action else action
        if args:
            item.connect('activate', _action, args)
        else:
            item.connect('activate', _action)
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
