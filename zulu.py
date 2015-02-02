#!/usr/bin/env python

# Copyright (C) 2015 by Kyle Hornberg, Stefano Palazzo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Much of the base code is from https://github.com/sfstpala/World-Clock-AppIndicator/blob/master/world-clock
# thus his name is on the copyright as well.

import gtk
import appindicator
import gobject
import datetime
import tempfile

class AppIndicator (appindicator.Indicator):

    fmt = "%H:%M"
    items = []

    def __init__(self, name, category):

        # Blank icon from https://github.com/fossfreedom/indicator-sysmonitor/blob/master/indicator-sysmonitor#L72
        fn, self.tindicator = tempfile.mkstemp(suffix=".svg")

        with open(self.tindicator, "w") as f:
           svg = '<?xml version="1.0" encoding="UTF-8" \
                       standalone="no"?><svg id="empty" xmlns="http://www.w3.org/2000/svg" \
                       height="22" width="1" version="1.0" \
                       xmlns:xlink="http://www.w3.org/1999/xlink"></svg>'
           f.write(svg)
           f.close()

        self.ai = appindicator.Indicator.__init__(self, name, self.tindicator, category)
        self.set_status(appindicator.STATUS_ACTIVE)
        self.menu = gtk.Menu()
        self.set_menu(self.menu)
        self.menu_setup()
        self.menu.show_all()
        self.update()
        gtk.main()

    def menu_setup(self):
        # Just add a quit option
        self.quit_item = gtk.MenuItem("Quit")
        self.menu.append(self.quit_item)
        self.quit_item.connect("activate", self.quit)

    def update(self):
        self.set_label(datetime.datetime.utcnow().strftime(self.fmt))
        gobject.timeout_add(100, self.update)

    def quit(self, *data):
        gtk.main_quit()


AppIndicator('zulu', 0)