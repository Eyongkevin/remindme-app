from time import strftime
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

import schedule
from src.layouts import base
from src.scheduler import Scheduler
from .utils import load_fonts, seconds_until_midnight
from src.layouts.homeList import RemainderListView


class MainApp(App):
    sw_state = False
    sw_time = 0
    sw_stop_time = False

    def update_time(self, nap):
        self._update_main_clock()
        self._update_date()
        self._update_stop_watch(nap)

    def _update_main_clock(self):
        self.root.children[0].children[0].ids.time.text = strftime("[b]%H[/b]:%M:%S")

    def _update_stop_watch(self, nap):
        if self.sw_state == "start" and self.sw_stop_time:
            self.sw_time += nap
            minutes, seconds = divmod(self.sw_time, 60)
            if int(minutes) >= self.sw_stop_time:
                MainApp.sw_state == "stop"
            else:
                part_seconds = seconds * 100 % 100
                self.root.children[0].children[
                    0
                ].ids.stopwatch.text = f"""{int(minutes):02}:{int(seconds):02}.[size=40]{int(part_seconds):02}[/size]"""
        elif self.sw_state == "pause":
            pass
        elif self.sw_state == "reset":
            self.root.children[0].children[
                0
            ].ids.stopwatch.text = "00:00.[size=40]00[/size]"
            self.sw_time = 0
            self.sw_stop_time = False
            self.sw_state = False
        elif self.sw_state == "stop":
            self.sw_state = False
        elif self.sw_state == "start" and self.sw_stop_time is False:
            self.sw_state = False

    def _update_date(self):
        self.root.children[0].children[0].ids.date.text = strftime("%a, %B %-d")

    def _update_home_list_data(self, dt):
        Scheduler.data_instance.data = RemainderListView.prepare_data()
        self._schedule_once_at_midnight()

    def _schedule_once_at_midnight(self):
        secs = seconds_until_midnight()
        Clock.schedule_once(self._update_home_list_data, secs)

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)
        self._schedule_once_at_midnight()

    def build(self):
        Window.size = (300, 500)
        sch = Scheduler()
        sch.schedule_all()
        Clock.schedule_interval(self.schedule_run_pending, 1)
        return base.BaseWidget()

    def schedule_run_pending(self, e):
        schedule.run_pending()


if __name__ == "__main__":
    Window.clearcolor = get_color_from_hex("#101216")
    load_fonts()
    MainApp().run()
