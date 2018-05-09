import pathlib

import pytest

from kitovu.gui import confscreen


@pytest.fixture(autouse=True)
def kitovu_yaml(monkeypatch, temppath):
    config = temppath / 'kitovu.yaml'
    config.write_text('root-dir: ~/hsr', encoding='utf-8')
    monkeypatch.setattr(confscreen.settings, 'get_config_file_path',
                        lambda: pathlib.Path(config))
    return config


@pytest.fixture
def screen(qtbot):
    cs = confscreen.ConfScreen()
    qtbot.add_widget(cs)
    return cs


def test_reading_config(screen):
    assert screen._edit.toPlainText() == 'root-dir: ~/hsr'


@pytest.mark.parametrize('close', [True, False])
def test_writing_config(screen, kitovu_yaml, qtbot, close):
    screen._edit.append('global-ignore: ["Thumbs.db"]')

    if close:
        with qtbot.wait_signal(screen.close_requested):
            screen._back_button.click()
    else:
        with qtbot.assert_not_emitted(screen.close_requested):
            screen._save_button.click()

    expected = '\n'.join([
        'root-dir: ~/hsr',
        'global-ignore: ["Thumbs.db"]',
    ])
    assert kitovu_yaml.read_text('utf-8') == expected


def test_cancel(screen, kitovu_yaml, qtbot):
    screen._edit.append('global-ignore: ["Thumbs.db"]')
    with qtbot.wait_signal(screen.close_requested):
        screen._cancel_button.click()

    assert kitovu_yaml.read_text('utf-8') == 'root-dir: ~/hsr'
