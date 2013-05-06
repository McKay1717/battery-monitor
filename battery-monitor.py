#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Wil Alvarez (aka satanas)

from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import GObject

try:
    import ctypes
    libc = ctypes.CDLL('libc.so.6')
    libc.prctl(15, 'battery-monitor', 0, 0)
except ImportError:
    pass

Notify.init("battery-monitor")

def check_battery():
    status = None
    remaining = None
    capacity = None

    try:
        state_file = open('/proc/acpi/battery/BAT0/state')
        info_file = open('/proc/acpi/battery/BAT0/info')

        for line in state_file:
            if line.find('remaining') >= 0:
                temp = line.split(':')[2][:-3]
                remaining = int(temp.strip())
            elif line.find('charging') >= 0:
                temp = line.split(':')[2]
                status = temp.strip()

        for line in info_file:
            if line.find('last full') >= 0:
                temp = line.split(':')[2][:-3]
                capacity = int(temp.strip())
    except:
        fd = open('/sys/class/power_supply/BAT0/charge_full')
        capacity = int(fd.readline())
        fd.close()

        fd = open('/sys/class/power_supply/BAT0/charge_now')
        remaining = int(fd.readline())
        fd.close()

        fd = open('/sys/class/power_supply/BAT0/status')
        status = fd.readline().lower()
        fd.close()
    finally:
        print capacity, remaining, status
        percentage = int((remaining * 100) / capacity)

        notification = None
        if percentage <= 5:
            notification = Notify.Notification('Critical battery level',
                'Battery level under 5%, your PC will shutdown shortly', None)
        elif percentage <= 10:
            notification = Notify.Notification('Low battery level',
                'Battery level under 10%, connect the charger', None)

        if notification:
            notification.show()

    GObject.timeout_add(60000, check_battery)


check_battery()
Gtk.main()


