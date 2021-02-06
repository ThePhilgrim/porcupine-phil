import pathlib
import tkinter
import tkinter.ttk as ttk
from typing import List

from porcupine import get_paned_window, get_tab_manager, tabs


class DirectoryTree(ttk.Treeview):

    def __init__(self, master: tkinter.Misc) -> None:
        super().__init__(master, selectmode='browse')
        self.paths = {'': pathlib.Path('.').resolve()}
        self.process_directory('')
        self.bind('<<TreeviewSelect>>', self.on_click, add=True)

    def process_directory(self, node: str) -> None:
        for child in self.get_children(node):
            self.delete(child)

        files: List[pathlib.Path] = []
        directories: List[pathlib.Path] = []

        for path in sorted(self.paths[node].iterdir()):
            if path.is_dir():
                directories.append(path)
            else:
                files.append(path)

        for d in directories:
            n = self.insert(node, 'end', text=d.name, open=False)
            self.paths[n] = d
            self._insert_dummy(n)

        for f in files:
            n = self.insert(node, 'end', text=f.name, open=False)
            self.paths[n] = f

    def on_click(self, event: tkinter.Event) -> None:
        [selection] = self.selection()
        path = self.paths[selection]
        if path.is_dir():
            self.process_directory(selection)
        else:
            get_tab_manager().add_tab(tabs.FileTab.open_file(get_tab_manager(), path))

    def _insert_dummy(self, node: str) -> None:
        self.insert(node, 'end', text='')


def setup() -> None:
    sidebar = DirectoryTree(get_paned_window())
    get_paned_window().insert(get_tab_manager(), sidebar)   # put sidebar before tab manager