from time import strftime

import schedule
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from src.layouts import base

# from src.layouts.homeList import RemainderListView
from src.scheduler import Scheduler

from .utils import load_fonts  # , seconds_until_midnight


class MainApp(App):
    sw_state: bool | str = False
    sw_time: int = 0
    sw_stop_time: bool = False

    def update_time(self, nap: int) -> None:
        self._update_main_clock()
        self._update_date()
        self._update_stop_watch(nap)

    def _update_main_clock(self) -> None:
        self.root.children[0].children[0].ids.time.text = strftime("[b]%H[/b]:%M:%S")  # type: ignore

    def _update_stop_watch(self, nap: int) -> None:
        if self.sw_state == "start" and self.sw_stop_time:
            self.sw_time += nap
            minutes, seconds = divmod(self.sw_time, 60)
            if int(minutes) >= self.sw_stop_time:
                self.sw_state = "stop"
            else:
                part_seconds: int = seconds * 100 % 100
                self.root.children[0].children[0].ids.stopwatch.text = f"""{int(minutes):02}:{int(seconds):02}.[size=40]{int(part_seconds):02}[/size]"""  # type: ignore
        elif self.sw_state == "pause":
            pass
        elif self.sw_state == "reset":
            self.root.children[0].children[0].ids.stopwatch.text = "00:00.[size=40]00[/size]"  # type: ignore
            self.sw_time = 0
            self.sw_stop_time = False
            self.sw_state = False
        elif self.sw_state == "stop":
            self.sw_state = False
        elif self.sw_state == "start" and self.sw_stop_time is False:
            self.sw_state = False

    def _update_date(self):
        self.root.children[0].children[0].ids.date.text = strftime("%a, %B %-d")  # type: ignore

    # def _update_home_list_data(self, dt):
    #     Scheduler.data_instance.data = RemainderListView.prepare_data()
    #     self._schedule_once_at_midnight()

    # def _schedule_once_at_midnight(self):
    #     secs = seconds_until_midnight()
    #     Clock.schedule_once(self._update_home_list_data, secs)

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)  # type: ignore
        # self._schedule_once_at_midnight()

    def build(self):
        Window.size = (300, 500)
        sch: Scheduler = Scheduler()
        sch.schedule_all()
        Clock.schedule_interval(self.schedule_run_pending, 1)  # type: ignore
        return base.BaseWidget()

    def schedule_run_pending(self, _):
        schedule.run_pending()


if __name__ == "__main__":
    Window.clearcolor = get_color_from_hex("#101216")
    load_fonts()
    MainApp().run()
