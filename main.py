from image_to_braille import image_to_braille, get_styles

from textual import events
from textual import log
from textual.app import App, ComposeResult
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Select,
    Static,
    Switch,
)
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widget import Widget

STYLES = get_styles()

class Message(Static):
    pass
    
class Sidebar(Container):
    # Arguments for the CLI
    image_path = reactive("images/sample-image.png") # Default image to use if none is specified
    width_in_chars = reactive(-1)
    current_style = reactive(0)
    to_invert = reactive(False)
    to_output = reactive("")
    
    def compose(self) -> ComposeResult:
        yield Message("Options")
        yield Message("Image Path (including the extension):")
        yield Input(placeholder="Enter a full or relative path...", id="path_input")
        yield Message("Resize to Width (optional, minimum 2):")
        yield Input(placeholder="Enter output width in number of characters...", id="width_input")
        yield Message("Use Style:")
        yield Select(((line, i) for i, line in enumerate(STYLES)), allow_blank=False, value=0)
        yield Horizontal(
            Static("Invert: ", classes="label"),
            Switch(animate=False),
            classes="container",
        )
        yield Message("Save as Text File (leave blank to skip):")
        yield Input(placeholder="Enter file name, without the extension...", id="save_input")
        yield Button("Generate", id="start", variant="success")
        
    def on_input_changed(self, event: Input.Changed) -> None: 
        "Update CLI arguments on input change"
        event.stop() # Don't propagate event to parent widget
        if event.input.id == "path_input":
            self.image_path = event.value
        elif event.input.id == "width_input":
            if event.value and event.value.isdigit():
                self.width_in_chars = int(event.value)
        elif event.input.id == "save_input":
            self.to_output = event.value
    
    def on_switch_changed(self, event: Switch.Changed) -> None:
        "Update to_invert on switch change"
        event.stop()  
        self.to_invert = event.value
    
    def on_select_changed(self, event: Select.Changed) -> None:
        "Update current_style on select change"
        event.stop()  
        self.current_style = event.value
        
class Canvas(Widget):
    # Canvas will resize when braille_image changes when layout=True
    braille_image = reactive("Generated ASCII image goes here.", layout=True)

    def render(self) -> str:
        return self.braille_image

class ImageToBrailleApp(App):
    "A textual app that runs image_to_braille"
    CSS_PATH = "main.tcss"
    TITLE = "Image to Braille ASCII Art Generator"
    
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("o", "toggle_sidebar", "Options"),
                Binding("escape", "app.quit", "Quit", show=True)
    ]    
    
    def compose(self) -> ComposeResult:
        "Create child widgets for the app."
        yield Header(show_clock=False)
        yield ScrollableContainer(Canvas(id="canvas"))
        yield Sidebar()
        yield Footer()
        
    # For debugging purposes
    def on_key(self, event: events.Key) -> None:
        self.log(event)
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        "Event handler called when a button is pressed."
        if event.button.id == "start":
            self.action_toggle_sidebar()
            canvas = self.query_one(Canvas)
            sidebar = self.query_one(Sidebar)
            canvas.braille_image = image_to_braille(sidebar.image_path, sidebar.width_in_chars, sidebar.current_style, sidebar.to_invert, sidebar.to_output)
            if canvas.braille_image == None:
                canvas.braille_image = "Something went wrong while generating the image. Please check your inputs and try again."
        
    def action_toggle_dark(self) -> None:
        "An action to toggle dark mode."
        self.dark = not self.dark
        
    def action_toggle_sidebar(self) -> None:
        "An action to toggle the sidebar."
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