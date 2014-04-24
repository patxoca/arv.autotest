# -*- coding: utf-8 -*-

# $Id$

import pyinotify

from autotest import cmdline
from autotest import config
from autotest import reporters
from autotest import runner
from autotest import event_filters


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
    react = reporters.make_reporter()
    def callback():
        runner.run(cfg.command, react)
    wm = pyinotify.WatchManager()
    handler = EventHandler(
        callback=callback,
        filter=event_filters.and_(
            event_filters.not_(event_filters.is_delete_dir_event),
            event_filters.simple_event_filter_factory(cfg.watch, cfg.global_ignore),
            event_filters.throttler_factory(cfg.throttling),
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
