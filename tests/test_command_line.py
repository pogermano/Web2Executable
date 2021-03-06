from command_line import CommandBase
import utils
import config
import pytest

api = pytest.mark.skipif(
    not pytest.config.getoption("--runapi"),
    reason="need --runapi option to run"
)

@pytest.fixture(scope='module')
def command_base():
    base = CommandBase()
    base._project_name = 'Test'
    return base

def test_get_versions(command_base):
    assert command_base.get_setting('nw_version').values == []
    command_base.get_versions()
    command_base.setup_nw_versions()
    assert '0.13.2' in command_base.get_setting('nw_version').values

def test_get_settings(command_base):
    settings = command_base.get_settings()

    assert 'download_settings' in settings
    assert 'web2exe_settings' in settings
    assert 'window_settings' in settings
    assert 'app_settings' in settings
    assert 'compression' in settings

def test_sub_output_pattern(command_base):
    pattern_setting = command_base.get_setting('output_pattern')
    command_base.get_setting('name').value = 'Test'
    pattern_setting.value = '%(name) 123'

    value = command_base.sub_pattern()

    assert value == 'Test 123'

def test_multiple_sub_output_pattern(command_base):
    pattern_setting = command_base.get_setting('output_pattern')

    command_base.get_setting('name').value = 'Test'
    command_base.get_setting('nw_version').value = '0.14.0'

    pattern_setting.value = '%(name) 123 %(nw_version)'

    value = command_base.sub_pattern()

    assert value == 'Test 123 0.14.0'

def test_valid_get_setting_objects(command_base):
    valid_settings = ['name', 'nw_version', 'windows-x64', 'main']
    for setting_name in valid_settings:
        setting = command_base.get_setting(setting_name)
        assert setting != None

def test_invalid_get_setting_objects(command_base):
    invalid_settings = ['foo', 'bar', 'steve', 'der']
    for setting_name in invalid_settings:
        setting = command_base.get_setting(setting_name)
        assert setting == None

def test_get_default_nwjs_branch(command_base):
    import re
    branch = command_base.get_default_nwjs_branch()

    match = re.match('nw\d+', branch)

    assert match != None

def test_get_versions(command_base):
    import os
    path = utils.get_data_file_path(config.VER_FILE)

    if os.path.exists(path):
        os.remove(path)

    command_base.get_versions()

    with open(path, 'r') as ver_file:
        data = ver_file.read()
        assert len(data) > 0


