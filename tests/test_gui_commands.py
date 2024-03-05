import pytest
from unittest.mock import MagicMock, patch
from mixmancer.gui.commands import stop_sfx_sounds, set_music_volume


@pytest.fixture
def pygame_mixer_mock():
    return MagicMock()


def test_stop_sfx_sounds(pygame_mixer_mock: MagicMock):
    with patch("pygame.mixer") as mock_pygame_mixer:
        # Mock pygame.mixer.stop to raise AttributeError
        mock_pygame_mixer.stop = MagicMock(side_effect=AttributeError)

        # Check if stop_sfx_sounds raises AttributeError
        with pytest.raises(AttributeError):
            stop_sfx_sounds()


@patch("pygame.mixer")
def test_set_music_volume(mock_pygame_mixer: MagicMock):
    with patch("pygame.mixer.music", MagicMock()) as mock_music:
        set_music_volume("0.5")
        mock_music.set_volume.assert_called_once_with(0.5)
