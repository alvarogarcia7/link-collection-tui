from __future__ import annotations

import abc
import sys
from pathlib import Path
from typing import TYPE_CHECKING, cast

from rich.console import ConsoleRenderable
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.css.query import DOMQuery
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget, AwaitMount
from textual.widgets import Button, Footer, Label, Markdown, Static, DataTable

if TYPE_CHECKING:
    from typing_extensions import Final


class Register:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link


class Repository:
    @abc.abstractmethod
    def find_all(self) -> list[Register]:
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._values = [
            Register("Hacker News", "https://news.ycombinator.com/news"),
            Register("Hacker News", "https://news.ycombinator.com/news")
        ]

    def find_all(self) -> list[Register]:
        return self._values

    def append(self, register: Register) -> None:
        self._values.append(register)


# class Help(Screen):
#     """The help screen for the application."""
#
#     BINDINGS = [("escape,space,q,question_mark", "pop_screen", "Close")]
#     """Bindings for the help screen."""
#
#     def compose(self) -> ComposeResult:
#         """Compose the game's help.
#
#         Returns:
#             ComposeResult: The result of composing the help screen.
#         """
#         yield Markdown(Path(__file__).with_suffix(".md").read_text())


class DisplayRegisterRow(Screen):
    BINDINGS = [("escape,space,q,question_mark", "pop_screen", "Close")]
    """Bindings for the help screen."""

    def compose(self) -> ComposeResult:
        """Compose the game's help.

        Returns:
            ComposeResult: The result of composing the help screen.
        """
        yield "aaa"


# class GameHeader(Widget):
#     """Header for the game.
#
#     Comprises of the title (``#app-title``), the number of moves ``#moves``
#     and the count of how many cells are turned on (``#progress``).
#     """
#
#     moves = reactive(0)
#     """int: Keep track of how many moves the player has made."""
#
#     filled = reactive(0)
#     """int: Keep track of how many cells are filled."""
#
#     def compose(self) -> ComposeResult:
#         """Compose the game header.
#
#         Returns:
#             ComposeResult: The result of composing the game header.
#         """
#         # with Horizontal():
#         #     yield Label(self.app.title, id="app-title")
#         #     yield Label(id="moves")
#         #     yield Label(id="progress")
#
#     def watch_moves(self, moves: int):
#         """Watch the moves reactive and update when it changes.
#
#         Args:
#             moves (int): The number of moves made.
#         """
#         self.query_one("#moves", Label).update(f"Moves: {moves}")
#
#     def watch_filled(self, filled: int):
#         """Watch the on-count reactive and update when it changes.
#
#         Args:
#             filled (int): The number of cells that are currently on.
#         """
#         self.query_one("#progress", Label).update(f"Filled: {filled}")


class GameCell(Button):
    """Individual playable cell in the game."""

    @staticmethod
    def at(row: int) -> str:
        """Get the ID of the cell at the given location.

        Args:
            row (int): The row of the cell.

        Returns:
            str: A string ID for the cell.
        """
        return f"cell-{row}"

    def __init__(self, index: int, row: Register) -> None:
        """Initialise the game cell.

        Args:
            row (int): The row of the cell.
        """
        super().__init__("", id=self.at(index))
        self.row = row

    def compose(self) -> ComposeResult:
        yield "a"
        return super().compose()


class GameGrid(Widget):
    """The main playable grid of game cells."""

    def __init__(self, repository: Repository, *children: Widget):
        super().__init__(*children)
        self._repository = repository
        table = DataTable()
        table.add_column("Link", width=10)
        table.add_column("Name", width=40)
        table.zebra_stripes = True
        self._table = table

    def compose(self) -> ComposeResult:
        self._rows = self._repository.find_all()
        for index, row in enumerate(self._rows):
            self._table.add_row(*[row.link, row.title], key=f"cell-{index}")
        # self._table.update_cell("cell-0", "Link", "NEW VALUE")
        yield self._table


class Game(Screen):
    BINDINGS = [
        Binding("a", "add", "Add"),
        # Binding("n", "new_game", "New Game"),
        # Binding("question_mark", "push_screen('help')", "Help", key_display="?"),
        Binding("q", "quit", "Quit"),
        Binding("up,w,k", "navigate(-1)", "Move Up", False),
        Binding("down,s,j", "navigate(1)", "Move Down", False),
        # Binding("space", "move", "Toggle", False),
    ]

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self._repository = InMemoryRepository()

    def cell(self, row: int) -> GameCell:
        """Get the cell at a given location.

        Args:
            row (int): The row of the cell to get.

        Returns:
            GameCell: The cell at that location.
        """
        return self.query_one(f"#{GameCell.at(row)}", GameCell)

    def compose(self) -> ComposeResult:
        """Compose the game screen.

        Returns:
            ComposeResult: The result of composing the game screen.
        """
        # yield GameHeader()
        game_grid = GameGrid(self._repository)
        game_grid.focus()
        self._game_grid = game_grid
        yield game_grid
        yield Footer()

    def add(self) -> None:
        a = 8 // 0
        print(a)
        self._repository.append(Register("Added", "Added"))
        self._game_grid.compose()
        self._game_grid.notify_style_update()
        self.compose()

    # def on_button_pressed(self, event: GameCell.Pressed) -> None:
    #     """React to a press of a button on the game grid.
    #
    #     Args:
    #         event (GameCell.Pressed): The event to react to.
    #     """
    #     # self.make_move_on(cast(GameCell, event.button))

    def action_new_game(self) -> None:
        """Start a new game."""
        self._repository = InMemoryRepository()
        # start_point = self.cell(0)
        # self.set_focus(start_point)

    def navigate(self, x: int) -> None:
        print(f"x: {x}")
        sys.exit(1)

    def action_navigate(self, row: int) -> None:
        """Navigate to a new cell by the given offsets.

        Args:
            row (int): The row of the cell to navigate to.
        """
        # if isinstance(self.focused, GameCell):
        #     self.set_focus(
        #         self.cell(
        #             (self.focused.row + row)
        #         )
        #     )

    # def action_move(self) -> None:
    #     """Make a move on the current cell."""
    #     if isinstance(self.focused, GameCell):
    #         self.focused.press()

    def on_mount(self) -> None:
        """Get the game started when we first mount."""


class FiveByFive(App[None]):
    """Main 5x5 application class."""

    CSS_PATH = "five_by_five.tcss"
    """The name of the stylesheet for the app."""

    # SCREENS = {"help": Help}
    # """The pre-loaded screens for the application."""

    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle Dark Mode")]
    """App-level bindings."""

    TITLE = "Link Collection Visualizer"
    """The title of the application."""

    def on_mount(self) -> None:
        """Set up the application on startup."""
        self.push_screen(Game())


if __name__ == "__main__":
    FiveByFive().run()
