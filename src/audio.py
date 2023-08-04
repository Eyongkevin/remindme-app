from kivy.core.audio import SoundLoader
from src.utils import ROOT_DIR


class Audio:
    def __init__(self, sound=str(ROOT_DIR / "audio" / "sound.wav")):
        self.sound = sound
        self.loader = SoundLoader.load(self.sound)

    def play(self):
        if self.loader:
            self.loader.play()

    def stop(self):
        if self.loader:
            self.loader.stop()
