from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock

import schedule
from src.layouts import base
from src.scheduler import Scheduler


class MainApp(App):
    def build(self):
        Window.size = (300, 500)
        sch = Scheduler()
        sch.schedule_all()
        Clock.schedule_interval(self.schedule_run_pending, 1)
        return base.BaseWidget()

    def schedule_run_pending(self, e):
        schedule.run_pending()


if __name__ == "__main__":
    MainApp().run()
