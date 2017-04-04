import tkinter as tk

from porcupine import plugins
from porcupine.settings import config


def filetab_hook(filetab):
    statusbar = tk.Label(filetab.content, anchor='w', relief='sunken')

    def update():
        line, column = filetab.textwidget.index('insert').split('.')
        statusbar['text'] = "Line %s, column %s" % (line, column)

    def set_enabled(junk, enabled):
        if enabled:
            # side='bottom' makes this go below the main area
            # TODO: convert the find/replace area into a plugin. the
            # statusbar probably shouldn't be a part of the filetab at
            # all? the find/replace area will not be but it should be
            # above the statusbar.
            statusbar.pack(side='bottom', fill='x')
            filetab.textwidget.on_cursor_move.append(update)
            update()
        else:
            statusbar.pack_forget()
            filetab.textwidget.on_cursor_move.remove(update)

    config.connect('gui:statusbar', set_enabled)
    set_enabled(None, config['gui:statusbar'])
    yield
    if config['gui:statusbar']:
        # try to get things garbage-collected
        set_enabled(None, False)


plugins.add_plugin("Statusbar", filetab_hook=filetab_hook)