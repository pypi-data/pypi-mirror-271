import os
import csv
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import Footer, Header, ListView, Label, ListItem, DataTable, Static
from textual.logging import TextualHandler
from rich.text import Text
import logging
import shutil
import importlib.resources as pkg_resources

logging.basicConfig(level=logging.INFO, handlers=[TextualHandler()])


class ABOUT(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]
    BORDER_TITLE = "Duckcuts About"

    def on_mount(self):
        self.border_subtitle = "Press ESC to close"

    def compose(self) -> ComposeResult:
        yield Static("Duckcuts", id="title")
        yield Static("https://duckcuts.app", id="url")


class ShortcutsTUI(App):
    TITLE = "Duckcuts"
    SUB_TITLE = ""
    CSS_PATH = "main.css"
    BINDINGS = [
        ("up arrow", "something", "Up"),
        ("down arrow", "else", "Down"),
        ("f", "toggle_files", "Toggle tools"),
        ("k", "scroll_up", "Scroll up"),
        ("j", "scroll_down", "Scroll down"),
        ("q", "quit", "Quit"),
        ("a", "push_screen('about')", "About"),
    ]
    SCREENS = {"about": ABOUT()}

    show_tree = var(True)
    global_data_object = {}
    available_tools = []
    active_list = ""
    remote_tools_data = []

    def watch_show_tree(self, show_tree: bool) -> None:
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        self.load_shortcuts_data()
        items = []
        for x in self.global_data_object.keys():
            items.append(
                ListItem(
                    Label(x, classes="itemLabel"), name=x, id=x, classes="listItem"
                )
            )
        yield Header()
        with Container():
            yield ListView(*items, id="tree-view")
            with VerticalScroll(id="shortcuts-view"):
                yield DataTable(id="shortcuts", zebra_stripes=True, show_cursor=None)
        yield Footer()

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.item is None:
            return
        self.generate_shortcut_names(
            self.global_data_object.get(str(event.item.name)), event.item.name
        )

    def generate_shortcut_names(self, json_object, name) -> None:
        obj1 = self.query_one("#shortcuts")
        vals = [tuple(d.values()) for d in json_object]
        obj1.clear(columns=True)
        obj1.add_columns(*("action", "shortcut"))
        self.sub_title = " " + name
        for row in vals:
            styled_row = []
            styled_row.append(Text(str(row[0]), style="white", justify="left"))
            styled_row.append(Text(str(row[1]), style="bold", justify="left"))
            obj1.add_row(*styled_row)

    def on_mount(self, event: events.Mount) -> None:
        self.load_shortcuts_data()
        self.query_one(ListView).focus()

    def action_toggle_files(self) -> None:
        self.show_tree = not self.show_tree
        if self.show_tree:
            self.query_one("#tree-view").focus()

    def action_scroll_up(self) -> None:
        self.query_one("#shortcuts").scroll_up()

    def action_scroll_down(self) -> None:
        self.query_one("#shortcuts").scroll_down()

    def action_focus_tools(self) -> None:
        self.query_one("#tree-view").focus()

    def action_focus_shortcuts(self) -> None:
        self.query_one("#shortcuts-view").focus()

    def get_home_folder(self):
        return os.path.expanduser("~")

    def load_shortcuts_data(self):
        data_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
        for filename in os.listdir(data_folder):
            toolname = filename.split(".")[0]
            extension = filename.split(".")[1]
            if extension != "csv":
                continue
            self.available_tools.append(toolname)
            self.global_data_object[toolname] = []
            data_file = os.path.join(data_folder, filename)
            if os.path.exists(data_file):
                with open(data_file, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        self.global_data_object[toolname].append(
                            {
                                "action": row[0],
                                "shortcut": row[1],
                            }
                        )


if __name__ == "__main__":
    app = ShortcutsTUI()
    app.run()
