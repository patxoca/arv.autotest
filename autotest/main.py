# -*- coding: utf-8 -*-

# $Id$

import pyinotify

from autotest import cmdline
from autotest import config
from autotest import reactor
from autotest import runner
from autotest import filters


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, callback, filter):
        self._callback = callback
        self._filter = filter

    # useful to understand how pyinotify works. If you uncomment this
    # method you should use a mask 'pyinotify.ALL_EVENTS' in order to
    # catch all events

    # def process_default(self, event):
    #     print str(event)

    def process_IN_DELETE(self, event):
        if not self._filter(event):
            return
        self._callback()

    def process_IN_CLOSE_WRITE(self, event):
        if not self._filter(event):
            return
        self._callback()


def main():
    opts = cmdline.parse()
    cfg = config.read_config(opts.config_file)
    def callback():
        code, output = runner.run(cfg.command)
        reactor.react(code, output)
    wm = pyinotify.WatchManager()
    handler = EventHandler(
        callback=callback,
        filter=filters.and_(
            filters.not_(filters.is_delete_dir_event),
            filters.simple_event_filter_factory(cfg.watch, cfg.global_ignore)
        )
    )
    notifier = pyinotify.Notifier(wm, handler)
    for watch in cfg.watch:
        wm.add_watch(
            watch.path,
            pyinotify.IN_CLOSE_WRITE|pyinotify.IN_DELETE,
            rec=watch.recurse,
            auto_add=watch.auto_add
        )
    notifier.loop()

main()
