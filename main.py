#!/usr/bin/env python3

import configparser
import os
import subprocess
import threading
import gi  # type: ignore[import-untyped]
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk  # type: ignore[import-untyped]
from gi.repository import AppIndicator3  # type: ignore[import-untyped]
from gi.repository import GLib  # type: ignore[import-untyped]


class MyIndicator:
    _ini = os.path.dirname(__file__) + '/config.ini'
    # env = os.environ.copy()

    def __init__(self):
        # noinspection PyArgumentList
        self.ind = AppIndicator3.Indicator.new(
            'Unity Tray Mail 1.1.1',
            'indicator-messages',
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon('new-messages-red')
        self.menu = Gtk.Menu()
        # self.menu_item('Thunderbird', icon_name='thunderbird', args=['thunderbird'])
        # if ini file not exists create it
        if not os.path.exists(self._ini):
            with open(self._ini, 'w') as f:
                # thunderbird example
                f.write('[thunderbird]\n')
                f.write('label = Thunderbird\n')
                f.write('icon_name = org.mozilla.thunderbird\n')
                f.write('args = flatpak run org.mozilla.thunderbird\n')
                f.write('\n')
                # calendar example
                f.write('[calendar]\n')
                f.write('label = Calendar\n')
                f.write('icon_name = org.gnome.Calendar\n')
                f.write('args = gnome-calendar\n')
                f.write('\n')
        for section in self.ini_sections(self._ini):
            self.menu_item(
                self.ini_read(self._ini, section, 'label'),
                icon_name = self.ini_read(self._ini, section, 'icon_name'),
                icon_file = self.ini_read(self._ini, section, 'icon_file'),
                args = self.ini_read(self._ini, section, 'args')
            )
        # self.menu_item('Compose', icon_name='stock_mail-compose', args=['thunderbird', '-compose'])
        # self.menu_item('Address Book', icon_name='stock_addressbook', args=['thunderbird', '-addressbook'])
        # self.menu_item('Calendar', icon_name='org.gnome.Calendar', args=['gnome-calendar'])
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu_item('Restart', action=self.restart)
        self.menu_item('Quit', action=self.quit)
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

    def run(self, widget, args):
        self.ind.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
        GLib.timeout_add_seconds(1, self.ind.set_status, AppIndicator3.IndicatorStatus.ACTIVE)
        # os.system(args + " &")
        p = subprocess.Popen(
            args.split(),
            # env=self.env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        # wait for process to finish in background thread
        threading.Thread(target=p.wait, daemon=True).start()

    def restart(self, widget):
        dialog = Gtk.MessageDialog(
            parent=None,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Are you sure?"
        )
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            os.system("./run &")
            Gtk.main_quit()

    def quit(self, widget):
        dialog = Gtk.MessageDialog(
            parent=None,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Are you sure?"
        )
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            Gtk.main_quit()

    @staticmethod
    def main():
        Gtk.main()


if __name__ == '__main__':
    indicator = MyIndicator()
    indicator.main()
