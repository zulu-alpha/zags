"""Generate config files from environmental variables and launch Arma 3 server with them"""
import os
from jinja2 import Environment, FileSystemLoader


ENV = Environment(loader=FileSystemLoader('templates'))

def load_singular_variables(global_map):
    """Load the values from the global variables specified in the global_map
    into the returned dictionary, with it's keys defined in the global_map as well.
    """
    return {
        var_name: os.getenv(global_name) for global_name, var_name in \
        global_map.items() if os.getenv(global_name)
    }

def render_server_cfg(path_config):
    """Render server.cfg
    https://community.bistudio.com/wiki/server.cfg
    """
    template_cfg = ENV.get_template('server.cfg.jinja')

    global_variable_map = {
        'string_variables': {
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
        },
        'bool_int_variables': {
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
        },
        'string_array_variables': {
            'CONFIG_MOTD': 'motd',
            'CONFIG_ADMINS': 'admins',
            'CONFIG_HEADLESS_CLIENTS': 'headlessClients',
            'CONFIG_LOCAL_CLIENTS': 'localClient',
            'CONFIG_MISSION_WHITELIST': 'missionWhitelist'
        },
        'number_bool_array_variables': {
            'CONFIG_KICK_CLIENTS_ON_SLOW_NETWORK': 'kickClientsOnSlowNetwork'
        },
        'mission_rotation_variables': {
            'CONFIG_MISSION_ROTATION_CLASSNAMES': 'mission_classnames',
            'CONFIG_MISSION_ROTATION_NAMES': 'mission_names',
            'CONFIG_MISSION_ROTATION_DIFFICULTIES': 'mission_difficulties',
            'CONFIG_MISSION_ROTATION_PARAMS': 'mission_parameters'
        }
    }

    parameters = {}

    # Parse singlular variables
    for paramater_type in ('string_variables', 'bool_int_variables'):
        parameters[paramater_type] = load_singular_variables(global_variable_map[paramater_type])

    # Parse array variables
    for paramater_type in ('string_array_variables', 'number_bool_array_variables', 'mission_rotation_variables'):
        parameters[paramater_type] = {
            var_name: os.getenv(global_name).split(':') for global_name, var_name in \
            global_variable_map[paramater_type].items() if os.getenv(global_name)
        }

    mission_parameters = set(global_variable_map['mission_rotation_variables'].values()) - {'mission_parameters'}
    provided_mission_parameters = set(parameters['mission_rotation_variables'].keys())
    parameter_intersection = mission_parameters.intersection(provided_mission_parameters)
    if parameter_intersection:
        error = f'{mission_parameters - provided_mission_parameters} mission rotation parameters are still needed!'
        assert parameter_intersection == mission_parameters, error

    with open(path_config, 'w') as f:
        rendered = template_cfg.render(**parameters)
        f.write(rendered)


def render_basic_cfg(path_basic):
    """Render basic.cfg
    https://community.bistudio.com/wiki/basic.cfg
    """
    template_cfg = ENV.get_template('basic.cfg.jinja')

    global_variable_map = {
        'int_variables': {
            'BASIC_MAX_MSG_SEND': 'MaxMsgSend',
            'BASIC_SIZE_GUARANTEED': 'MaxSizeGuaranteed',
            'BASIC_MAX_SIZE_NONGUARANTEED': 'MaxSizeNonguaranteed',
            'BASIC_MIN_BANDWIDTH': 'MinBandwidth',
            'BASIC_MAX_BANDWIDTH': 'MaxBandwidth',
            'BASIC_MIN_ERROR_TO_SEND': 'MinErrorToSend',
            'BASIC_MIN_ERROR_TO_SEND_NEAR': 'MinErrorToSendNear',
            'BASIC_MAX_CUSTOM_FILE_SIZE': 'MaxCustomFileSize'
        },
        'class_int_variable': {
            'BASIC_MAX_PACKET_SIZE': 'maxPacketSize'
        }
    }
    
    parameters = {}

    for parameter_type in ('int_variables', 'class_int_variable'):
        parameters[parameter_type] = load_singular_variables(global_variable_map[parameter_type])

    with open(path_basic, 'w') as f:
        rendered = template_cfg.render(**parameters)
        f.write(rendered)

def render_armaprofile(path_profile):
    """Render basic.cfg
    https://community.bistudio.com/wiki/server.armaprofile
    """
    template_cfg = ENV.get_template('server.armaprofile.jinja')

    global_variable_map = {
        'option_variables': {
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
        },
        'custom_difficulty_variables': {
            'PROFILE_AI_LEVEL_PRESET': 'aiLevelPreset'
        },
        'custom_ai_level_variables': {
            'PROFILE_CUSTOM_AI_LEVEL_SKILL_AI': 'skillAI',
            'PROFILE_CUSTOM_AI_LEVEL_PRECISION_AI': 'precisionAI'
        }
    }

    parameters = {}

    for parameter_type in ('option_variables', 'custom_difficulty_variables', 'custom_ai_level_variables'):
        parameters[parameter_type] = load_singular_variables(global_variable_map[parameter_type])

    with open(path_profile, 'w') as f:
        rendered = template_cfg.render(**parameters)
        f.write(rendered)
