# -*- coding: utf-8 -*-

# $Id$


class Configuration(object):
    pass

def read_config(path):
    # llegir la configuració (possiblement d'un .ini, .yml o .json) i
    # retornar un object Configuration inicialitzat
    cfg = Configuration()
    cfg.include_files = ["*.py"]
    cfg.exclude_files = []
    cfg.command = "echo hello"
    cfg.queue_events = False

    return cfg
