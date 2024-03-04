from mixmancer.config.settings import Settings

def test_settings_defaults():
    settings = Settings()

    assert settings.projector_width == 1200
    assert settings.projector_height == 900
    assert settings.app_width == 600
    assert settings.app_height == 400
    assert settings.display == 1
    assert settings.color == {
        'white': '#ffffff',
        'black': '#000000',
        'grey': '#36393f',
        'purple': '#7289da',
    }
