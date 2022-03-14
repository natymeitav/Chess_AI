from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.layout import Layout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
import webbrowser
from main import Game


class Menu(Layout):
    def __init__(self):
        Layout.__init__(self)

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
        self.startB.font_size = 30
        self.add_widget(self.startB)

        self.infoB = Button(text="chess?")
        self.infoB.size = (360, 180)
        self.infoB.pos = (370, 300)
        self.infoB.background_color = [1, 0, 0, 1]
        self.infoB.bind(on_press=self.show_info)
        self.infoB.font_size = 30
        self.add_widget(self.infoB)

        # difficulty bar

        self.difficulty = Slider(min=0, max=3, value=2, orientation='vertical')
        self.difficulty.size = (100, 500)
        self.difficulty.pos = (50, 80)
        self.difficulty.step = 1
        self.difficulty.value_track = 1000
        self.difficulty.value_track_color = [1, 0, 0, 1]
        self.add_widget(self.difficulty)

        self.depthL = Label(text="MAX DEPTH")
        self.depthL.font_size = 27
        self.depthL.pos = (55, 570)
        self.depthL.color = [0, 0, 0, 1]
        self.add_widget(self.depthL)

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

    def start(self, b1):
        self.clear_widgets()
        self.add_widget(Game(self.difficulty.value,self))

    def rebuild_menu(self):
        self.clear_widgets()

        self.add_widget(self.title)
        self.add_widget(self.startB)
        self.add_widget(self.infoB)

        self.difficulty.value = 2
        self.add_widget(self.difficulty)

        self.add_widget(self.depthL)
        self.add_widget(self.mark0)
        self.add_widget(self.mark1)
        self.add_widget(self.mark2)
        self.add_widget(self.mark3)

    def show_info(self,b1):
        webbrowser.open("rules.pdf")


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
