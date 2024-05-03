import logging
import os
import glob

from sql_unit_test.core.config import locate_root_dir

logger = logging.getLogger(__name__)

def parse_filename(filename):
    
    logger.debug(f'Passed filename: {filename}')
    logger.info("Parsing filename")
    parsed_filename = filename.split('.')[0]

    logger.debug(f'Parsed filename: {parsed_filename}')
    logger.info(f'Successfully parsed filename.')  

    return parsed_filename

def clean_run_dir():
    root = locate_root_dir()
    os.chdir(root)
    failure_files = glob.glob(f'./.sql-unit-test/runs/*')

    for path in failure_files:
        normal_path = os.path.normpath(path)
        print(normal_path)
        os.remove(normal_path)

    return failure_files