import os
from pathlib import Path
import pytest


PATH_CONFIG = 'server.cfg'
PATH_BASIC = 'basic.cfg'
PATH_PROFILE = 'server.armaprofile'

CONFIG_STRING_VARIABLES = {
    'CONFIG_PASSWORD_ADMIN': 'passwordAdmin',
    'CONFIG_PASSWORD': 'password',
    'CONFIG_SERVER_COMMAND_PASSWORD': 'serverCommandPassword',
    'CONFIG_HOSTNAME': 'hostname',
    'CONFIG_LOG_FILE': 'logFile',
    'CONFIG_DOUBLE_ID_DETECTED': 'doubleIdDetected',
    'CONFIG_ON_USER_CONNECTED': 'onUserConnected',
    'CONFIG_ON_USER_DISCONNECTED': 'onUserDisconnected',
    'CONFIG_ON_HACKED_DATA': 'onHackedData',
    'CONFIG_ON_DIFFERENT_DATA': 'onDifferentData',
    'CONFIG_ON_UNSIGNED_DATA': 'onUnsignedData',
    'CONFIG_REGULAR_CHECK': 'regularCheck',
    'CONFIG_TIME_STAMP_FORMAT': 'timeStampFormat',
    'CONFIG_FORCED_DIFFICULTY': 'forcedDifficulty'
}
CONFIG_BOOL_INT_VARIABLES = {
    'CONFIG_MAX_PLAYERS': 'maxPlayers',
    'CONFIG_VOTE_THRESHOLD': 'voteThreshold',
    'CONFIG_VOTE_MISSION_PLAYERS': 'voteMissionPlayers',
    'CONFIG_KICK_DUPLICATE': 'kickduplicate',
    'CONFIG_UPNP': 'upnp',
    'CONFIG_ALLOWED_FILE_PATCHING': 'allowedFilePatching',
    'CONFIG_DISCONNECT_TIMEOUT': 'disconnectTimeout',
    'CONFIG_MAX_DESYNC': 'maxdesync',
    'CONFIG_MAX_PING': 'maxping',
    'CONFIG_MAX_PACKETLOSS': 'maxpacketloss',
    'CONFIG_VERIFY_SIGNATURES': 'verifySignatures',
    'CONFIG_DRAWING_IN_MAP': 'drawingInMap',
    'CONFIG_DISABLE_VON': 'disableVoN',
    'CONFIG_VON_CODEC_QUALITY': 'vonCodecQuality',
    'CONFIG_VON_CODEC': 'vonCodec',
    'CONFIG_BATTLEEYE': 'BattlEye',
    'CONFIG_FORCE_ROTORLIB_SIMULATION': 'forceRotorLibSimulation',
    'CONFIG_PERSISTENT': 'persistent',
    'CONFIG_REQUIRED_BUILD': 'requiredBuild'
}
CONFIG_STRING_ARRAY_VARIABLES = {
    'CONFIG_MOTD': 'motd',
    'CONFIG_ADMINS': 'admins',
    'CONFIG_HEADLESS_CLIENTS': 'headlessClients',
    'CONFIG_LOCAL_CLIENTS': 'localClient',
    'CONFIG_MISSION_WHITELIST': 'missionWhitelist'
}
CONFIG_NUMBER_OR_BOOL_ARRAY_VARIABLES = {
    'CONFIG_KICK_CLIENTS_ON_SLOW_NETWORK': 'kickClientsOnSlowNetwork'
}
BASIC_INT_VARIABLES = {
    'BASIC_MAX_MSG_SEND': 'MaxMsgSend',
    'BASIC_SIZE_GUARANTEED': 'MaxSizeGuaranteed',
    'BASIC_MAX_SIZE_NONGUARANTEED': 'MaxSizeNonguaranteed',
    'BASIC_MIN_BANDWIDTH': 'MinBandwidth',
    'BASIC_MAX_BANDWIDTH': 'MaxBandwidth',
    'BASIC_MIN_ERROR_TO_SEND': 'MinErrorToSend',
    'BASIC_MIN_ERROR_TO_SEND_NEAR': 'MinErrorToSendNear',
    'BASIC_MAX_CUSTOM_FILE_SIZE': 'MaxCustomFileSize'
}
BASIC_CLASS_INT_VARIABLES = {
    'BASIC_MAX_PACKET_SIZE': 'maxPacketSize'
}
PROFILE_OPTIONS_VARIABLES = {
    'PROFILE_REDUCED_DAMAGE': 'reducedDamage',
    'PROFILE_GROUP_INDICATORS': 'groupIndicators',
    'PROFILE_FRIENDLY_TAGS': 'friendlyTags',
    'PROFILE_ENEMY_TAGS': 'enemyTags',
    'PROFILE_DETECTED_MINES': 'detectedMines',
    'PROFILE_COMMANDS': 'commands',
    'PROFILE_WAYPOINTS': 'waypoints',
    'PROFILE_TACTICAL_PING': 'tacticalPing',
    'PROFILE_WEAPON_INFO': 'weaponInfo',
    'PROFILE_STANCE_INDICATOR': 'stanceIndicator',
    'PROFILE_STAMINA_BAR': 'staminaBar',
    'PROFILE_WEAPON_CROSSHAIR': 'weaponCrosshair',
    'PROFILE_VISION_AID': 'visionAid',
    'PROFILE_THIRD_PERSON_AID': 'thirdPersonView',
    'PROFILE_CAMERA_SHAKE': 'cameraShake',
    'PROFILE_SCORE_TABLE': 'scoreTable',
    'PROFILE_DEATH_MESSAGE': 'deathMessages',
    'PROFILE_VON_ID': 'vonID',
    'PROFILE_MAP_CONTENT': 'mapContent',
    'PROFILE_AUTO_REPORT': 'autoReport',
    'PROFILE_MULTIPLE_SAVES': 'multipleSaves'
}
PROFILE_VARIABLES = {
    'PROFILE_AI_LEVEL_PRESET': 'aiLevelPreset'
}
PROFILES_CUSTOM_AI_LEVEL = {
    'PROFILE_CUSTOM_AI_LEVEL_SKILL_AI': 'skillAI',
    'PROFILE_CUSTOM_AI_LEVEL_PRECISION_AI': 'precisionAI'
}

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
