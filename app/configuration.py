"""Generate config files from environmental variables and launch Arma 3 server with them"""
import os
import json
from jinja2 import Environment, FileSystemLoader


ENV = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
MAP_PATH = os.path.join(os.path.dirname(__file__), 'envar_mapping.json')

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
    with open(MAP_PATH, 'r') as open_file:
        global_variable_map = json.loads(open_file.read())['config']

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

    with open(path_config, 'w') as open_file:
        rendered = template_cfg.render(**parameters)
        open_file.write(rendered)
        print(f'Written server config to {path_config}')

def render_basic_cfg(path_basic):
    """Render basic.cfg
    https://community.bistudio.com/wiki/basic.cfg
    """
    template_cfg = ENV.get_template('basic.cfg.jinja')
    with open(MAP_PATH, 'r') as open_file:
        global_variable_map = json.loads(open_file.read())['basic']

    parameters = {}

    for parameter_type in ('int_variables', 'class_int_variable'):
        parameters[parameter_type] = load_singular_variables(global_variable_map[parameter_type])

    with open(path_basic, 'w') as open_file:
        rendered = template_cfg.render(**parameters)
        open_file.write(rendered)
        print(f'Written basic config to {path_basic}')

def render_armaprofile(path_profile):
    """Render basic.cfg
    https://community.bistudio.com/wiki/server.armaprofile
    """
    template_cfg = ENV.get_template('server.armaprofile.jinja')
    with open(MAP_PATH, 'r') as open_file:
        global_variable_map = json.loads(open_file.read())['profile']

    parameters = {}

    for parameter_type in ('option_variables', 'custom_difficulty_variables', 'custom_ai_level_variables'):
        parameters[parameter_type] = load_singular_variables(global_variable_map[parameter_type])

    with open(path_profile, 'w') as open_file:
        rendered = template_cfg.render(**parameters)
        open_file.write(rendered)
        print(f'Written profile to {path_profile}')
