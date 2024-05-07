from typing import Union

import h5py
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.widget import Widget
from textual.widgets import Static

import h5tui.h5
from h5tui import HDF5ItemViewer


class HexView(VerticalScroll, can_focus=True):

    BINDINGS = [
        Binding('b', 'bold', "Put text in bold"),
        Binding('u', 'underline', "Put text in underline"),
    ]

    def __init__(self, item, *children: Widget):
        super().__init__(*children)
        self.item = item
        self.text = f"The widget returned by HexViewer for {self.item.name}."

    def compose(self) -> ComposeResult:
        yield Static(self.text)

    def action_bold(self):
        w = self.query_one(Static)
        w.update(f"[b]{self.text}[/]")

    def action_underline(self):
        w = self.query_one(Static)
        w.update(Text(self.text, style="underline"))


class HexViewer(HDF5ItemViewer):
    def __init__(self):
        self._id = 'hex-view'

    @staticmethod
    def can_handle(item: Union[h5py.File, h5py.Group, h5py.Dataset]) -> bool:
        if h5tui.h5.is_dataset(item):
            return True
        return False

    @staticmethod
    def get_widget(item: Union[h5py.File, h5py.Group, h5py.Dataset]) -> Widget:
        return HexView(item)

    def get_id(self) -> str:
        return self._id
