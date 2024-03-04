import pytest
from unittest.mock import MagicMock, patch
from mixmancer.gui.commands import stop_sfx_sounds, set_music_volume

@pytest.fixture
def mock_pygame_mixer():
    with patch('mixmancer.gui.commands.pygame.mixer') as mixer_mock:
        yield mixer_mock

def test_stop_sfx_sounds(mock_pygame_mixer):
    stop_sfx_sounds()
    mock_pygame_mixer.stop.assert_called_once()

def test_set_music_volume(mock_pygame_mixer):
    set_music_volume(0.5)
    mock_pygame_mixer.music.set_volume.assert_called_once_with(0.5)