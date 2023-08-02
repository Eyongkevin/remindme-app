from kivy.app import App
from kivy.core.window import Window
from src.layouts import base


class MainApp(App):
    def build(self):
        Window.size = (300, 500)
        return base.BaseWidget()


if __name__ == "__main__":
    MainApp().run()
