#!/usr/bin/env python3

import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appIndicator
import signal
import subprocess


class MyIndicator:
    processes = []

    def __init__(self):
        self.ind = appIndicator.Indicator.new(
            'Test',
            'indicator-messages',
            # 'application-x-addon',
            appIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.ind.set_status(appIndicator.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon('new-messages-red')
        self.menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label('Thunderbird')
        item.connect('activate', self.run, 'thunderbird')
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label('Thunderbird / Compose')
        item.connect('activate', self.run, ['thunderbird', '-compose'])
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label('Calendar')
        item.connect('activate', self.run, 'gnome-calendar')
        self.menu.append(item)

        # item = Gtk.MenuItem()
        # item.set_label('Electron Mail')
        # item.connect('activate', self.run, './ElectronMail.sh')
        # self.menu.append(item)
        #
        # item = Gtk.MenuItem()
        # item.set_label('Delta Chat')
        # item.connect('activate', self.run, './DeltaChat.sh')
        # self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label('Quit')
        item.connect('activate', self.quit)
        self.menu.append(item)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    @staticmethod
    def main():
        Gtk.main()

    def run(self, widget, param):
        self.ind.set_status(appIndicator.IndicatorStatus.ATTENTION)
        # subprocess.run(['thunderbird'])
        p = subprocess.Popen(param)
        self.processes.append(p)
        print('pid=', p.pid)
        GLib.timeout_add_seconds(1, self.restore_ind)

    def restore_ind(self):
        print(self.processes)
        self.ind.set_status(appIndicator.IndicatorStatus.ACTIVE)

    def quit(self, widget):
        # for pid in self.processes:
        #     if isinstance(pid, subprocess.Popen):
        #         pid.send_signal(sig=signal.SIGTERM)
        Gtk.main_quit()


if __name__ == '__main__':
    indicator = MyIndicator()
    indicator.main()
