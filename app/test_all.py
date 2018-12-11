"""All tests that are available are in here"""
import os
import json
import pytest


MAP_PATH = os.path.join(os.path.dirname(__file__), 'envar_mapping.json')
with open(MAP_PATH, 'r') as open_file:
    MAP_DICT = json.loads(open_file.read())
PATH_CONFIG = 'server.cfg'
PATH_BASIC = 'basic.cfg'
PATH_PROFILE = 'server.armaprofile'

CONFIG_STRING_VARIABLES = MAP_DICT['config']['string_variables']
CONFIG_BOOL_INT_VARIABLES = MAP_DICT['config']['bool_int_variables']
CONFIG_STRING_ARRAY_VARIABLES = MAP_DICT['config']['string_array_variables']
CONFIG_NUMBER_OR_BOOL_ARRAY_VARIABLES = MAP_DICT['config']['number_bool_array_variables']
BASIC_INT_VARIABLES = MAP_DICT['basic']['int_variables']
BASIC_CLASS_INT_VARIABLES = MAP_DICT['basic']['class_int_variable']
PROFILE_OPTIONS_VARIABLES = MAP_DICT['profile']['option_variables']
PROFILE_VARIABLES = MAP_DICT['profile']['custom_difficulty_variables']
PROFILES_CUSTOM_AI_LEVEL = MAP_DICT['profile']['custom_ai_level_variables']

def test_config_single_variables(tmp_path):
    """Tests that each single (non array) variable is written correctly to the config file"""
    from configuration import render_server_cfg

    test_value = '123'
    global_variables = dict(CONFIG_BOOL_INT_VARIABLES, **CONFIG_STRING_VARIABLES)
    for global_var in global_variables:
        os.environ[global_var] = test_value

    render_server_cfg(tmp_path / PATH_CONFIG)

    with open(tmp_path / PATH_CONFIG, 'r') as f:
        text = f.read()
        for variable in global_variables.values():
            error = f'{variable} not defined correctly!'
            if variable in CONFIG_STRING_VARIABLES.values():
                assert f'{variable} = "{test_value}";' in text, error
            elif variable in CONFIG_BOOL_INT_VARIABLES.values():
                assert f'{variable} = {test_value};' in text, error

def test_basic_single_variables(tmp_path):
    """Tests that each variable is written correctly to the basic file"""
    from configuration import render_basic_cfg

    test_value = '123'
    global_variables = BASIC_INT_VARIABLES
    for global_var in global_variables:
        os.environ[global_var] = test_value

    render_basic_cfg(tmp_path / PATH_BASIC)

    with open(tmp_path / PATH_BASIC, 'r') as f:
        text = f.read()
        for variable in global_variables.values():
            assert f'{variable} = {test_value};' in text, f'{variable} not defined correctly!'

def test_profile_option_variables(tmp_path):
    """Tests that each variable for the Options class is written correctly to the profile file"""
    from configuration import render_armaprofile

    test_value = '1'
    global_variables = PROFILE_OPTIONS_VARIABLES
    for global_var in global_variables:
        os.environ[global_var] = test_value

    render_armaprofile(tmp_path / PATH_PROFILE)

    with open(tmp_path / PATH_PROFILE, 'r') as f:
        text = f.read()
        for variable in global_variables.values():
            assert f'{variable} = {test_value};' in text, f'{variable} not defined correctly!'

def test_profile_custom_difficulty(tmp_path):
    """Tests that the variable in the CustomDifficulty class in the profile file is written correctly."""
    from configuration import render_armaprofile

    test_value = '1'
    os.environ['PROFILE_AI_LEVEL_PRESET'] = test_value
    variable = PROFILE_VARIABLES['PROFILE_AI_LEVEL_PRESET']

    render_armaprofile(tmp_path / PATH_PROFILE)

    with open(tmp_path / PATH_PROFILE, 'r') as f:
        text = f.read()
        test_text = '};\n    %s = %s;\n    };' % (variable, test_value)
        assert test_text in text, f'{variable} not defined correctly!'

def test_profile_custom_ai_level(tmp_path):
    """Tests that the variables in the CustomAILevel class in the profile file is written correctly."""
    from configuration import render_armaprofile

    test_value = '0.5'
    os.environ['PROFILE_CUSTOM_AI_LEVEL_SKILL_AI'] = test_value
    variable1 = PROFILES_CUSTOM_AI_LEVEL['PROFILE_CUSTOM_AI_LEVEL_SKILL_AI']
    os.environ['PROFILE_CUSTOM_AI_LEVEL_PRECISION_AI'] = test_value
    variable2 = PROFILES_CUSTOM_AI_LEVEL['PROFILE_CUSTOM_AI_LEVEL_PRECISION_AI']

    render_armaprofile(tmp_path / PATH_PROFILE)

    with open(tmp_path / PATH_PROFILE, 'r') as f:
        text = f.read()
        test_text = 'class CustomAILevel\n    {\n        %s = %s;\n        %s = %s;\n        };' % (variable1, test_value, variable2, test_value)
        assert test_text in text, 'CustomAILevel is not defined correctly!'

def test_basic_class_sockets(tmp_path):
    """Tests that the sockets class variable is written correctly to the basic file"""
    from configuration import render_basic_cfg

    test_value = '123'
    os.environ['BASIC_MAX_PACKET_SIZE'] = test_value
    variable = BASIC_CLASS_INT_VARIABLES['BASIC_MAX_PACKET_SIZE']

    render_basic_cfg(tmp_path / PATH_BASIC)

    with open(tmp_path / PATH_BASIC, 'r') as f:
        text = f.read()
        test_text = 'class sockets{%s = %s;};' % (variable, test_value)
        assert test_text in text, f'{variable} not defined correctly!'

def test_config_arrays(tmp_path):
    """Tests if string or number arrays are created correctly to the config file"""
    from configuration import render_server_cfg

    global_variables = dict(CONFIG_STRING_ARRAY_VARIABLES, **CONFIG_NUMBER_OR_BOOL_ARRAY_VARIABLES)

    def assign_globals(value):
        for global_var in global_variables:
            os.environ[global_var] = value

    for variable in global_variables.values():
        # One line
        assign_globals('123')
        render_server_cfg(tmp_path / PATH_CONFIG)
        if variable in CONFIG_STRING_ARRAY_VARIABLES.values():
            array = '%s[]= {\n    "123"\n}' % variable
        elif variable in CONFIG_NUMBER_OR_BOOL_ARRAY_VARIABLES.values():
            array = '%s[]= {\n    123\n}' % variable
        with open(tmp_path / PATH_CONFIG, 'r') as f:
            assert array in f.read(), 'Array text does not match!'

        # Multi line
        assign_globals('123:456:789')
        render_server_cfg(tmp_path / PATH_CONFIG)
        if variable in CONFIG_STRING_ARRAY_VARIABLES.values():
            array = '%s[]= {\n    "123",\n    "456",\n    "789"\n};' % variable
        elif variable in CONFIG_NUMBER_OR_BOOL_ARRAY_VARIABLES.values():
            array = '%s[]= {\n    123,\n    456,\n    789\n};' % variable
        with open(tmp_path / PATH_CONFIG, 'r') as f:
            assert array in f.read(), 'Array text does not match!'

        # Multi line with blank lines
        assign_globals(':123:456::789:')
        render_server_cfg(tmp_path / PATH_CONFIG)
        if variable in CONFIG_STRING_ARRAY_VARIABLES.values():
            array = '%s[]= {\n    "",\n    "123",\n    "456",\n    "",\n    "789",\n    ""\n};' % variable
        elif variable in CONFIG_NUMBER_OR_BOOL_ARRAY_VARIABLES.values():
            array = '%s[]= {\n    ,\n    123,\n    456,\n    ,\n    789,\n    \n};' % variable  # TODO: Make better handling of None elements
        with open(tmp_path / PATH_CONFIG, 'r') as f:
            assert array in f.read(), 'Array text does not match!'

def test_config_not_defined(tmp_path):
    """Tests that each string variable is not written if not defined"""
    from configuration import render_server_cfg, render_basic_cfg, render_armaprofile

    def check_file(file_name, variable_names, test_var):
        """Check that the given variable names or test value doesn't exist in the given file"""
        with open(file_name, 'r') as f:
            text = f.read()
            for variable_name in variable_names:
                assert variable_name not in text, f'{variable_name} is defined!'
                assert test_var not in text, f'test value for {variable_name} still somehow defined!'

    all_global_variables = dict(
        CONFIG_STRING_ARRAY_VARIABLES,
        **CONFIG_BOOL_INT_VARIABLES,
        **CONFIG_NUMBER_OR_BOOL_ARRAY_VARIABLES,
        **CONFIG_STRING_ARRAY_VARIABLES,
        **BASIC_INT_VARIABLES,
        **BASIC_CLASS_INT_VARIABLES,
        **PROFILE_OPTIONS_VARIABLES,
        **PROFILE_VARIABLES,
        **PROFILES_CUSTOM_AI_LEVEL
    )

    for global_var in all_global_variables:
        if global_var in os.environ:
            del os.environ[global_var]

    render_server_cfg(tmp_path / PATH_CONFIG)
    render_basic_cfg(tmp_path / PATH_BASIC)
    render_armaprofile(tmp_path / PATH_PROFILE)

    for file_name in (tmp_path / PATH_CONFIG, tmp_path / PATH_BASIC, tmp_path / PATH_PROFILE):
        check_file(file_name, all_global_variables.values(), 'test_var')

def test_mission(tmp_path):
    """Test that the mission rotation mission is added correctly"""
    from configuration import render_server_cfg

    os.environ['CONFIG_MISSION_ROTATION_CLASSNAMES'] = 'Mission1'
    os.environ['CONFIG_MISSION_ROTATION_NAMES'] = 'co@12_opsalamander_v1-2-0.Tanoa.pbo'
    os.environ['CONFIG_MISSION_ROTATION_DIFFICULTIES'] = 'Custom'
    if 'CONFIG_MISSION_ROTATION_PARAMS' in os.environ:
        del os.environ['CONFIG_MISSION_ROTATION_PARAMS']
    render_server_cfg(tmp_path / PATH_CONFIG)
    correct_text = 'class Missions\n{\n\n\tclass Mission1\n\t{\n\t\ttemplate = co@12_opsalamander_v1-2-0.Tanoa.pbo;\n\t\tdifficulty = "Custom";\n\t\tclass Params {  };\n\t};\n\t\n};'
    with open(tmp_path / PATH_CONFIG, 'r') as f:
        assert correct_text in f.read(), 'Text does not match!'

    os.environ['CONFIG_MISSION_ROTATION_CLASSNAMES'] = 'Mission1:Mission2'
    os.environ['CONFIG_MISSION_ROTATION_NAMES'] = 'co@12_opsalamander_v1-2-0.Tanoa.pbo:zat_selection_v2-1-0.Malden.pbo'
    os.environ['CONFIG_MISSION_ROTATION_DIFFICULTIES'] = 'Custom:veteran'
    os.environ['CONFIG_MISSION_ROTATION_PARAMS'] = 'someparam:otherparam'
    render_server_cfg(tmp_path / PATH_CONFIG)
    correct_text = 'class Missions\n{\n\n\tclass Mission1\n\t{\n\t\ttemplate = co@12_opsalamander_v1-2-0.Tanoa.pbo;\n\t\tdifficulty = "Custom";\n\t\tclass Params { someparam };\n\t};\n\tclass Mission2\n\t{\n\t\ttemplate = zat_selection_v2-1-0.Malden.pbo;\n\t\tdifficulty = "veteran";\n\t\tclass Params { otherparam };\n\t};\n\t\n};'
    with open(tmp_path / PATH_CONFIG, 'r') as f:
        assert correct_text in f.read(), 'Text does not match!'

    os.environ['CONFIG_MISSION_ROTATION_CLASSNAMES'] = 'Mission1'
    os.environ['CONFIG_MISSION_ROTATION_NAMES'] = 'co@12_opsalamander_v1-2-0.Tanoa.pbo'
    del os.environ['CONFIG_MISSION_ROTATION_DIFFICULTIES']
    with pytest.raises(AssertionError):
        render_server_cfg(tmp_path / PATH_CONFIG)

    del os.environ['CONFIG_MISSION_ROTATION_CLASSNAMES']
    os.environ['CONFIG_MISSION_ROTATION_DIFFICULTIES'] = 'Custom'
    with pytest.raises(AssertionError):
        render_server_cfg(tmp_path / PATH_CONFIG)

def test_log_filename():
    """Test that a valid logfile name is used"""
    from log_name import make_log_filename
    import datetime

    os.environ['CONFIG_HOSTNAME'] = 'Test Server - Pytest'
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    correct_filename = f'/arma3/logs/[Test Server - Pytest]__{timestamp}.log'

    assert make_log_filename() == correct_filename
