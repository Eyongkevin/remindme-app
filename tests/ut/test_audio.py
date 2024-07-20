from unittest.mock import Mock, patch, sentinel

import pytest
from kivy.core.audio import SoundLoader

from src.audio import Audio


def test_audio_creation(tmp_path):
    sound_file = tmp_path / "sound.wav"
    with patch.object(SoundLoader, "load", new=Mock(return_value=sentinel)):
        audio = Audio(sound_file)
        assert audio is not None
        assert isinstance(audio, Audio)


def test_play(audio_obj):
    output = audio_obj.play()

    assert output is None


def test_stop(audio_obj):
    output = audio_obj.stop()

    assert output is None
