import pytest
from unittest.mock import MagicMock, patch
from mixmancer.display.image import ImageProjector

@pytest.fixture
def mock_pygame():
    with patch('mixmancer.display.image.pygame.display.set_mode'), \
         patch('mixmancer.display.image.pygame.image.load') as mock_load, \
         patch('mixmancer.display.image.pygame.transform.scale') as mock_scale, \
         patch('mixmancer.display.image.pygame.display.update'):
        mock_surface = MagicMock()
        mock_surface.get_width.return_value = 100
        mock_surface.get_height.return_value = 100
        mock_load.return_value = mock_surface
        yield

def test_image_projector_init(mock_pygame):
    resolution = (800, 600)
    display = 1
    projector = ImageProjector(resolution, display)
    assert projector.resolution == resolution

def test_image_projector_load_image(mock_pygame):
    resolution = (800, 600)
    display = 1
    projector = ImageProjector(resolution, display)
    image = "assets/tests/test.jpg"
    result = projector.load_image(image)
    assert result == True

def test_image_projector_blit(mock_pygame):
    resolution = (800, 600)
    display = 1
    projector = ImageProjector(resolution, display)
    image = "assets/tests/test.jpg"
    projector.load_image(image)
