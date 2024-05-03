
import logging
import colorama

from sql_unit_test.core.config_manager import retrieve_config_values

logger = logging.getLogger(__name__)

URI, TARGET_DIR, LOG_LEVEL = retrieve_config_values()

def configure_logger():
    logger.info('Configuring logger.')
    logging.basicConfig(
        level=LOG_LEVEL,
        format=colorama.Fore.CYAN   + "%(asctime)s [%(levelname)s] %(name)s: %(message)s" + colorama.Fore.WHITE,
        handlers=[
            logging.StreamHandler()
        ]
    )

    logger.info('Successfully configured logger.')
    logger.debug(f'Log level set to {LOG_LEVEL}')





