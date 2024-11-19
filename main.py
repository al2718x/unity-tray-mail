#!/usr/bin/env python3
import configparser
import os
import subprocess
import gi.repository

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import AppIndicator3


class MyIndicator:
    _ini = os.path.dirname(__file__) + '/menu.ini'
    def __init__(self):
        # noinspection PyArgumentList
        self.ind = AppIndicator3.Indicator.new(
            'Thunderbird Indicator 1.0.3',
            'indicator-messages',
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon('new-messages-red')
        self.menu = Gtk.Menu()
        self.menu_item('Thunderbird', icon_name='thunderbird', args=['thunderbird'])
        for section in self.ini_sections(self._ini):
            self.menu_item(
                self.ini_read(self._ini, section, 'label'),
                icon_name=self.ini_read(self._ini, section, 'icon_name'),
                icon_file = self.ini_read(self._ini, section, 'icon_file'),
                args=self.ini_read(self._ini, section, 'args').split(' ')
            )
        self.menu_item('Compose', icon_name='stock_mail-compose', args=['thunderbird', '-compose'])
        self.menu_item('Address Book', icon_name='stock_addressbook', args=['thunderbird', '-addressbook'])
        self.menu_item('Calendar', icon_name='org.gnome.Calendar', args=['gnome-calendar'])
        self.menu_item('Quit', icon_name='application-exit', action=self.quit)
        self.menu.show_all()
        self.ind.set_menu(self.menu)

    @staticmethod
    def ini_sections(file):
        try:
            config = configparser.ConfigParser()
            config.read(file)
            return config.sections()
        except:
            pass
        return []

    @staticmethod
    def ini_read(file, section, option, default=None):
        try:
            config = configparser.ConfigParser()
            config.read(file)
            return config[section][option]
        except:
            pass
        return default

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

    @staticmethod
    def quit(widget):
        Gtk.main_quit()

    @staticmethod
    def main():
        Gtk.main()


if __name__ == '__main__':
    indicator = MyIndicator()
    indicator.main()
