from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.layout import Layout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from main import Game


class Menu(Layout):
    def __init__(self):
        Layout.__init__(self)
        self.setup_menu()

    def start(self, b1):
        self.clear_widgets()
        self.add_widget(Game())

    def setup_menu(self):
        self.title = Label(text="Check, Mate")
        self.title.font_size = 80
        self.title.pos = (360, 680)
        self.title.color = [0, 0, 0, 1]
        self.add_widget(self.title)

        self.startB = Button(text="START")
        self.startB.size = (360, 180)
        self.startB.pos = (370, 80)
        self.startB.background_color = [0, 1, 0, 1]
        self.startB.bind(on_press=self.start)
        self.add_widget(self.startB)

        # difficulty bar

        self.difficulty = Slider(min=0, max=3, value=2, orientation='vertical')
        self.difficulty.size = (100,500)
        self.difficulty.pos = (50, 80)
        self.difficulty.step = 1
        self.difficulty.value_track = 1000
        self.difficulty.value_track_color=[1, 0, 0, 1]
        self.add_widget(self.difficulty)

        self.depth = Label(text="MAX DEPTH")
        self.depth.font_size = 27
        self.depth.pos = (55, 570)
        self.depth.color = [0, 0, 0, 1]
        self.add_widget(self.depth)

        self.mark3 = Label(text="- Quantum computer")
        self.mark3.font_size = 27
        self.mark3.pos = (200, 517)
        self.mark3.color = [0, 0, 0, 1]
        self.add_widget(self.mark3)

        self.mark2 = Label(text="- PC")
        self.mark2.font_size = 27
        self.mark2.pos = (100, 360)
        self.mark2.color = [0, 0, 0, 1]
        self.add_widget(self.mark2)

        self.mark1 = Label(text="- calculator")
        self.mark1.font_size = 27
        self.mark1.pos = (140, 204)
        self.mark1.color = [0, 0, 0, 1]
        self.add_widget(self.mark1)

        self.mark0 = Label(text="- microwave")
        self.mark0.font_size = 27
        self.mark0.pos = (145, 50)
        self.mark0.color = [0, 0, 0, 1]
        self.add_widget(self.mark0)



Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '820')
Config.set('graphics', 'height', '820')
Config.write()


class MenuApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.title = "Random Chess"
        return Menu()


MenuApp().run()
