from typing import Any

import pytermgui as ptg
from pytermgui import Widget
from pytermgui.pretty import pprint

OUTPUT = {}


class EditorWidget(Widget):

    def handle_key(self, key: str) -> bool:
        print(f"Received key: {key}")

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)
        with ptg.WindowManager() as manager:
            window = (ptg.Window(
                "",
                ptg.InputField("Balazs", prompt="Name: "),
                ptg.InputField("Some street", prompt="Address: "),
                ptg.InputField("+11 0 123 456", prompt="Phone number: "),
                "",
                ptg.Container(
                    "Additional notes:",
                    ptg.InputField(
                        "A whole bunch of\nMeaningful notes\nand stuff", multiline=True,
                    ),
                    box="EMPTY_VERTICAL",
                ),
                "",
                ["Submit", lambda *_: self.submit(manager, window)],
                width=60,
                box="DOUBLE",
            )
                      .set_title("[210 bold]New contact")
                      .center()
                      )

            # For the screenshot's sake
            window.select(0)

            manager.add(window)

    def submit(self, manager: ptg.WindowManager, window: ptg.Window) -> None:
        for widget in window:
            if isinstance(widget, ptg.InputField):
                OUTPUT[widget.prompt] = widget.value
                continue

            if isinstance(widget, ptg.Container):
                label, field = iter(widget)
                OUTPUT[label.value] = field.value

        manager.stop()


CONFIG = """
config:
    InputField:
        styles:
            prompt: dim italic
            cursor: '@72'
    Label:
        styles:
            value: dim bold

    Window:
        styles:
            border: '60'
            corner: '60'

    Container:
        styles:
            border: '96'
            corner: '96'
"""

with ptg.YamlLoader() as loader:
    loader.load(CONFIG)

EditorWidget()

pprint(OUTPUT)
