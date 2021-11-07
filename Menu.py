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

        self.title = Label(text="RANDOM CHESS")
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

        self.difficulty = Slider(min=0, max=4, value=2, orientation='vertical')
        self.difficulty.size = (100,500)
        self.difficulty.pos = (50, 80)
        self.difficulty.step = 1
        self.difficulty.value_track = 1000
        self.difficulty.value_track_color=[1, 0, 0, 1]
        self.add_widget(self.difficulty)


    def start(self, b1):
        self.clear_widgets()
        self.add_widget(Game())


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
