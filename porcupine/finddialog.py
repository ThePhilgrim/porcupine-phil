# Copyright (c) 2017 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""A find dialog."""
# TODO: replace support?

import re
import tkinter as tk


def _parse_geometry(geometry):
    """Convert tkinter geometry string to (x, y, width, height) tuple."""
    match = re.search(r'^(\d+)x(\d+)\+(\d+)\+(\d+)$', geometry)
    return tuple(map(int, match.groups()))


class FindDialog(tk.Toplevel):

    def __init__(self, editor, **kwargs):
        super().__init__(editor, **kwargs)
        self.transient(editor)
        self.editor = editor

        topframe = tk.Frame(self)
        topframe.pack(expand=True, anchor='center')
        label = tk.Label(topframe, text="What do you want to search for?")
        label.pack()
        self.entry = tk.Entry(
            topframe, font=editor.settings['font'])
        self.entry.bind('<Return>', lambda event: self.find())
        self.entry.bind('<Escape>', lambda event: self.withdraw())
        self.entry.pack()
        self.notfoundlabel = tk.Label(self, fg='red')
        self.notfoundlabel.pack()
        buttonframe = tk.Frame(self)
        buttonframe.pack(side='bottom', fill='x')

        closebutton = tk.Button(buttonframe, text="Close this dialog",
                                command=self.withdraw)
        closebutton.pack(side='right')
        findbutton = tk.Button(buttonframe, text="Find", command=self.find)
        findbutton.pack(side='right')

        self.entry.focus()
        self.title("Find")
        self.resizable(False, False)
        self.geometry('240x120')
        self.protocol('WM_DELETE_WINDOW', self.withdraw)

    def show(self):
        self.notfoundlabel['text'] = ''
        self.deiconify()

    def find(self, what=None):
        text = self.editor.textwidget
        if what is None:
            what = self.entry.get()
            if not what:
                # the user didnt enter anything
                return

        start = text.search(what, 'insert+1c')
        if start:
            end = start + ('+%dc' % len(what))
            text.tag_remove('sel', '0.0', 'end')
            text.tag_add('sel', start, end)
            text.mark_set('insert', start)
            text.see(start)
            self.notfoundlabel['text'] = ''
        else:
            self.notfoundlabel['text'] = "Cannot find '%s' :(" % what