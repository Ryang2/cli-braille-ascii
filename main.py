from rich import box
from rich.console import RenderableType

from textual.app import App, ComposeResult
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Footer,
    Header,
    Input,
    RichLog,
    Select,
    Static,
    Switch,
)
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widget import Widget
from textual import events
from textual import log
from image_to_braille import image_to_braille, get_styles

STYLES = get_styles()

class Message(Static):
    pass
    
class Sidebar(Container):
    # Arguments for the CLI
    image_path = reactive("C:/Users/rickr/git/cli-braille-ascii/$example-512px.png")
    width_in_chars = reactive(80)
    current_style = reactive(0)
    to_invert = reactive(False)
    to_output = reactive("")
    
    def compose(self) -> ComposeResult:
        yield Message("Options")
        yield Message("Image Path (including the extension):")
        yield Input(placeholder="Enter a full or relative path...") # Once focused, unable to shift focus unless you click select
                                                                    # This makes the 'O' shortcut ineffective
        yield Message("Resize to Width:")
        yield Input(placeholder="Enter output width in number of characters...") # TODO, validate numbers using reactive
        yield Message("Use Style:")
        yield Select(((line, i) for i, line in enumerate(STYLES)), allow_blank=False, value=0)
        yield Horizontal(
            Static("Invert: ", classes="label"),
            Switch(animate=False),
            classes="container",
        )
        yield Message("Save as Text File (leave blank to skip):")
        yield Input(placeholder="Enter file name, without the extension...")
        yield Button("Generate", id="start", variant="success") # TODO, don't focus on the button
        
class Canvas(Widget):
    # Canvas will resize when braille_image changes when layout=True
    braille_image = reactive("Generated ASCII image goes here.", layout=True)

    def render(self) -> str:
        return self.braille_image

class ImageToBrailleApp(App):
    """A textual app that runs image_to_braille"""
    CSS_PATH = "main.tcss"
    TITLE = "Image to Braille ASCII Art Generator"
    
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("o", "toggle_sidebar", "Options"),
                Binding("escape", "app.quit", "Quit", show=True)
    ]    
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=False)
        yield ScrollableContainer(Canvas(id="canvas"))
        yield Sidebar()
        yield Footer()
        
    # For debugging purposes
    def on_key(self, event: events.Key) -> None:
        self.log(event)
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "start":
            self.action_toggle_sidebar()
            canvas = self.query_one(Canvas)
            canvas.braille_image = image_to_braille(self.image_path, self.width_in_chars, self.current_style, self.to_invert, self.to_output)
        
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
        
    def action_toggle_sidebar(self) -> None:
        """An action to toggle the sidebar."""
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