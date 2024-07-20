from unittest.mock import Mock, patch

import pytest
from kivy.core.audio import SoundLoader

from src.audio import Audio


@pytest.fixture()
def audio_obj(tmp_path):
    sound_file = tmp_path / "sound.wav"
    with patch.object(
        SoundLoader,
        "load",
        new=Mock(
            return_value=Mock(
                play=Mock(return_value=None),
                stop=Mock(return_value=None),
            )
        ),
    ):
        yield Audio(sound_file)
