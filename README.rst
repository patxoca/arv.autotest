.. -*- ispell-local-dictionary: "british" -*-

Introduction
============

Simple application that monitors file changes (events) and triggers
the execution of a program in response. It is being developed with CI
in mind but may be useful for other purposes as well.

Te program is in pre-alpha state but it's functional enough to test
itself.


Installation
============

.. image:: https://travis-ci.org/patxoca/arv.autotest.svg?branch=master
   :target: https://travis-ci.org/patxoca/arv.autotest

This program has been tested with python 2.6, 2.7, 3.3 i 3.4.

::

  pip install arv.autotest


Internals overview
==================

- monitor sets files/directories for changes (``pynotify``)

- decide what events are processed (``event_filters.py``). The filters
  can drop events by type, because the events are coming to fast etc.
  Throtling is implemented here.

- execute a command in response (``runner.py``)

- process the output from the command (``reporters``).

  - display the output on screen

  - display a notification on completion

  - there exist a proof of concept preprocessor that can modify the
    output (ignore and highlight lines).

  - adjust throtling dynamically


Configuration file
==================

The following example is the configuration file used by ``autotest``
to test itself::

  {
      "command": "nosetests --verbosity=2",
      "global_ignore": ["\\..*"],
      "watch"  : [
          {
              "path"    : "arv",
              "include" : [".*\\.py"]
          },
          {
              "path"    : "tests",
              "include" : ["test_.*\\.py"]
          }
      ]
  }

The command specified in the ``command`` key will be executed whenever
a change is detected in any of the watched files (the files matching
``*.py`` within the ``arv`` directory and those matching
``test_*.py`` in the ``tests`` directory). Files matching any of the
``global_ignore`` patterns (hidden files in the example) will be
ignored.

In order to determine if an event is processed or ignored:

#. if the file name matches any of the ``global_ignore`` regexes the
   event is ignored. Use this option to ignore temporary files, VCS
   files etc.

#. the most specific watch is looked for (the one with the longest
   matching path):

   #. if the file name matches any of the corresponding ``exclude``
      patterns the event is ignored.

   #. if the file matches any of the ``include`` patterns the event is
      processed.

   #. otherwise it is ignored.


Configuration options
---------------------

Top level options:

:command: string, required. Command to be executed on every file
          change.

:watch: a list of watches. See below.

:global_ignore: a list of regexes (strings), optional. If a file name
                (not path) matches any regex the events related to
                that file are ignored.

:throttling: See below.

:peprocessor: A list of directives. See below.

Watch options:

:path: string, required. Path of the directory.

:recurse: boolean, default ``true``. If ``true`` sub-directories will
          be monitored recursively.

:auto_add: boolean, default ``true``. If ``true`` newly created
           sub-directories will be automatically monitored.

:include: list of regexes (strings). Regexes matching included files.

:exclude: list of regexes (strings). Regexes matching excluded files.

Preprocessor options:

:regex: regular expression. If the regex matches the **whole** line
        the corresponding action i executed.

:action: action identifier. Currently two actions are defined:

         - ``ignore``: remove the line from the output

         - ``failure``: highlight the line in red

Throttling options:

:max_events_second: limit the maximum number of events that will be
                    processed per second.


Notes on regexes
----------------

Regexes are ``re`` regular expressions, not shell globs. Use ``.*``
not ``*``.

Regular expressions are matched against the file name, not the path.

A ``$`` is added to the end of the regexes so ``test_.*\\.py`` will
match ``test_foo.py`` but not ``test_foo.py.bak``. Use
``test_.*\\.py.*`` to match both.

Be careful with the slashes, the json loader requires them to be
escaped (doubled).


Contact information
===================

Alexis Roda, alexis.roda.villalonga@gmail.com

If you find a bug of have some improvement feel free to drop em an
e-mail.


..  LocalWords:  autotest json regex regexes
