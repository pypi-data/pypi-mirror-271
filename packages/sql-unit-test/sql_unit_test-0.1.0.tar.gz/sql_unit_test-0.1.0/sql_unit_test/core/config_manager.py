import logging

from sql_unit_test.core.config import locate_root_dir, parse_config_yaml 

logger = logging.getLogger(__name__)

def retrieve_config_values():
    TARGET_DIR = '.'
    LOG_LEVEL = 'WARN'
    URI = ''

    root = locate_root_dir()

    if root is not None:
        
        yaml_path = root + "\sql-unit-test.yaml"

        app_env, uri, target_dir, log_level = parse_config_yaml(yaml_path)

        if app_env == 'dev':
            URI='sqlite:///sample//test_database.db'
            TARGET_DIR='./sample/playlists'

            if log_level:
                LOG_LEVEL = log_level

        else:
            if uri:
                URI = uri

            if target_dir:
                TARGET_DIR = target_dir

            if log_level:
                LOG_LEVEL = log_level
    
    return URI, TARGET_DIR, LOG_LEVEL