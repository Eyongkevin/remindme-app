from kivy.core.audio import Sound, SoundLoader

from src.utils import ROOT_DIR


class Audio:
    def __init__(self, sound: str = str(ROOT_DIR / "audio" / "sound.wav")) -> None:
        self.sound = sound
        self.loader: Sound | None = SoundLoader.load(self.sound)  # type: ignore

    def play(self) -> None:
        if self.loader:
            self.loader.play()

    def stop(self) -> None:
        if self.loader:
            self.loader.stop()
