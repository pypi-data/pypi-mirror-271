import os
import logging

from sql_unit_test.cli.outputs import report_non_sql_filetype

logger = logging.getLogger(__name__)

def ensure_sql_filetype(i, filename):
    logger.debug(f"Filename {i+1} = {filename}")
    logger.info(f'Checking whether file {i+1} is sql file.')
    if filename[-4:] != '.sql':
        logger.debug(f"File {i+1} extension = {filename[-4:]}")
        logger.info(f'File {i+1} does not have .sql extension.')
        return False
    else: 
        logger.info(f'File {i+1} has .sql extension.')
        return True
    logger.info(f'Finished checking whether file {i+1} is sql file.')




def check_directory(folder_path):
    logger.debug(f"Test folder path = {folder_path}")
    logger.info("Checking files in test directory.")
    file_list = []
    for i, f in enumerate(os.listdir(folder_path)):
        if ensure_sql_filetype(i, f) == True:
            file_list.append(f)
            logger.info("Added a sql file to the file_list.")

        else:
            report_non_sql_filetype(f)
            logger.info("Reported a non sql file type.")

    logger.debug(f"Sql files in test folder path = {file_list}")

    return file_list

