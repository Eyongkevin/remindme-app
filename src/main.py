from time import strftime
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock

import schedule
from src.layouts import base
from src.scheduler import Scheduler


class MainApp(App):
    sw_started = False

    def update_time(self, nap):
        if self.sw_started:
            self.sw_started += nap
        minutes, seconds = divmod(self.sw_started, 60)
        part_seconds = seconds * 100 % 100
        self.root.children[0].children[
            0
        ].ids.stopwatch.text = f"""{int(minutes):02}:{int(seconds):02}.[size=40]{int(part_seconds):02}[/size]"""

        self.root.children[0].children[0].ids.time.text = strftime("[b]%H[/b]:%M:%S")

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)
        # self.update_time()

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
