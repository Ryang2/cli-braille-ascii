from rich import box
from rich.console import RenderableType

from textual.app import App, ComposeResult
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    RichLog,
    Static,
    Switch,
)
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual import events
from textual import log
from image_to_braille import image_to_braille

MESSAGE = """
Options

Image Path: [...................]

Resize to Width: [...]

Use Style: [Average Threshold V]

Invert: [X]

Save as Text File: [X]

"""

class Message(Static):
    pass
    
class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Message(MESSAGE)
        yield Button("Generate", id="start", variant="success") # TODO, don't focus on the button
        
class Canvas(Static):
    pass

class ImageToBrailleApp(App):
    """A textual app that runs image_to_braille"""
    CSS_PATH = "main.tcss"
    TITLE = "Image to Braille ASCII Art Generator"
    
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("o", "toggle_sidebar", "Options"),
                Binding("escape", "app.quit", "Quit", show=True)
    ]
    
    # TODO: Figure out a way to pull this from image_to_braille.py rather than hardcoding
    STYLES = [("Average Threshold", "avg_thresh"),
              ("Adaptive Threshold", "adapt_thresh")
    ]
    
    # Arguments for the CLI
    image_path = reactive("C:/Users/rickr/git/cli-braille-ascii/example-512px.png")
    width_in_chars = reactive(80)
    current_style = reactive(STYLES[0])
    to_invert = reactive(False)
    to_output = reactive(False)
    braille_image = reactive("")
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Container(
            Sidebar(classes="-hidden"),
            Header(show_clock=False),
            Canvas(id="canvas")
        )
        yield Footer()
        
    # For debugging purposes
    def on_key(self, event: events.Key) -> None:
        self.log(event)
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "start": # disable button after pressing?
            # TODO: try to call a driver function instead? Or change main into something that works with CLI and methods
            self.braille_image = image_to_braille(self.image_path, self.width_in_chars, self.current_style[1], self.to_invert)
            canvas = self.query_one(Canvas)
            #self.action_toggle_sidebar()
            canvas.update(self.braille_image) # May also use reactive to always display what's in braille_image
            # It's overlaying on top of sidebar, we want it underneath!
            # Might also want to resize window to fit image
        
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
        
    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")

if __name__ == "__main__":
    app = ImageToBrailleApp()
    app.run()