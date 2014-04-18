# -*- coding: utf-8 -*-

# $Id$

import pyinotify

from autotest import config
from autotest import reactor
from autotest import runner
from autotest import walker


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, callback):
        self._callback = callback

    # useful to understand how pyinotify works. If you uncomment this
    # method you should use a mask 'pyinotify.ALL_EVENTS' in order to
    # catch all events

    # def process_default(self, event):
    #     print str(event)

    def process_IN_CLOSE_WRITE(self, event):
        self._callback()


def main():
    cfg = config.read_config(None)
    files = walker.get_file_list(None)
    def callback():
        code, output = runner.run(cfg.command)
        reactor.react(code, output)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler(callback=callback))
    wm.add_watch(files, pyinotify.IN_CLOSE_WRITE)
    notifier.loop()

main()
