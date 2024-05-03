import pandas as pd
import logging
import colorama
import time
import json
import time
import os

from sql_unit_test.cli.outputs import report_failing_test_result, report_passing_test_result, report_test_sql_query_error
from sql_unit_test.core.config import locate_root_dir
from sql_unit_test.core.utils import parse_filename

logger = logging.getLogger(__name__)

def read_sql_file(test_file_path):
    logger.debug(f'Passed test_file_path: {test_file_path}')
    logger.info('Opening sql unit test file.')

    test_file = open(test_file_path, 'r')

    logger.debug(f'Test file object: {test_file}')
    logger.info('Successfully opened sql unit test file.')

    logger.info('Reading sql unit test file to variable.')
    test_sql = test_file.read()
    logger.debug(f'Test file contents: \n{colorama.Fore.WHITE}{test_sql}{colorama.Fore.CYAN}')
    logger.info('Successfully Read sql unit test file to variable.')



    return test_sql, test_file_path

def run_sql_unit_test(test_sql, con):
    logger.info('Running sql test query.')
    start_time = time.time()
    try:

        test_result = pd.read_sql(test_sql, con)
        test_duration = round(time.time() - start_time, 2) 

    
    except Exception as E:
        raise SystemExit(report_test_sql_query_error(E))

    logger.debug(f'Test result: \n{colorama.Fore.WHITE}{test_result}{colorama.Fore.CYAN}')
    logger.info('Successfully ran sql test query.')

    return test_result, test_duration

def create_failure_file(test_results, test_duration, test_filename):
    logger.debug(f'Passed test_result: {test_results}')
    logger.debug(f'Passed test_duration: {test_duration}')
    logger.debug(f'Passed test_filename: {test_filename}')

    logger.info(f'Creating failure file.')

    root = locate_root_dir()

    parsed_filename = parse_filename(test_filename)

    failure_file_path = str(f'{root}/.sql-unit-test/runs/{parsed_filename}-failure_report-{time.strftime("%Y_%m_%d_%H_%M_%S")}.json').replace(' ', '_')
    logger.debug(f'Failure File Path: {failure_file_path}')

    dict = test_results.to_dict('records')
    logger.debug(f'Test Results Dict: {dict}')

    failure_file_dict = {
        'test_duration' : test_duration,
        'failing_rows' : dict
    }
    logger.debug(f'Failure File Dict: {dict}')

    with open(failure_file_path, "w") as outfile:
        json.dump(failure_file_dict, outfile, indent=4)

    logger.info('Successfully created failure file.')
    return failure_file_path

def handle_test_result(test_result_df, test_duration, test_filename, test_file_path):
    if test_result_df.empty:
        logger.info('Sql unit test PASSED.')
        report_passing_test_result(test_duration=test_duration)
        
    else:
        logger.info('Sql unit test FAILED.')
        failure_file_path = create_failure_file(test_results=test_result_df, test_filename=test_filename, test_duration=test_duration)

        report_failing_test_result(test_file_path=os.path.normpath(test_file_path), failure_file_path=os.path.normpath(failure_file_path), test_duration=test_duration)





