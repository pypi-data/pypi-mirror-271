from dotenv import load_dotenv
import os
import logging
import yaml
import time

from sql_unit_test.cli.outputs import report_missing_uri

logger = logging.getLogger(__name__)

def config_check(uri, target_dir, filepath):
    logger.info('Checking config environment variables.')
    if not uri:
        logging.info("URI object does not exist.")
        raise SystemExit(report_missing_uri())
    
    if not target_dir:
        logger.info(f"Option --target_dir was omitted; defaulting to TARGET_DIR environment variable value.")

    if not filepath:
        logger.info("Option --filepath was omitted; defaulting to TARGET_DIR environment variable value.")

def locate_root_dir():
    cwd = os.getcwd()
    logger.debug(f'Start directory: {cwd}')

    timeout = time.time() + 1
    while True:
        logger.info(f'Checking if cwd is root directory')
        logger.debug(f'cwd: {os.getcwd()}')

        if 'sql-unit-test.yaml' in os.listdir('.'):
            logger.info(f'Successfully located root directory.')
            root = os.getcwd()
            logger.debug(f'Root directory: {root}')

            logger.info(f'Changing cwd back to {cwd}')
            os.chdir(cwd)
            logger.info(f'Successfully changed cwd back to {cwd}')

            
            return root
            break

        if time.time() > timeout:
            logger.info(f'Search for root dir timed out.')
            logger.info(f'Changing cwd back to {cwd}')
            os.chdir(cwd)
            logger.info(f'Successfully changed cwd back to {cwd}')

            break

        else:
            logger.info(f'Cwd is not root directory. Going up one level.')
            os.chdir('..')
            logger.info(f'Successfully went up one directory level.')
    
def parse_config_yaml(path):
    with open(path) as stream:
            try:
                logger.info(f'Attempting to load data from yaml file.')
                data = yaml.safe_load(stream)
                logger.info(f'Successfully loaded data from yaml file.')

            except yaml.YAMLError as exc:
                logger.warning(exc)
    
    logger.info(f'Loading app_env variable from yaml data.')
    app_env = data['app_env']
    logger.debug(f'app_env: {app_env}')
    logger.info(f'Successfully loaded app_env variable from yaml data.')

    logger.info(f'Loading uri variable from yaml data.')
    uri = data['uri']
    logger.debug(f'uri: {uri}')
    logger.info(f'Successfully loaded uri variable from yaml data.')

    logger.info(f'Loading target_dir variable from yaml data.')
    target_dir = data['target_dir']
    logger.debug(f'target_dir: {target_dir}')
    logger.info(f'Successfully loaded target_dir variable from yaml data.')

    logger.info(f'Loading log_level variable from yaml data.')
    log_level = data['log_level']
    logger.debug(f'log_level: {log_level}')
    logger.info(f'Successfully loaded log_level variable from yaml data.')


    return app_env, uri, target_dir, log_level




