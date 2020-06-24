# Copyright 2020 The Hyve
#
# Licensed under the GNU General Public License, version 3,
# or (at your option) any later version (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# !/usr/bin/env python3

import logging
import sys
import traceback
import click
import getpass
from pathlib import Path
from omop_etl_wrapper.util.io import read_yaml_file
from omop_etl_wrapper.log.setup_logging import setup_logging
from omop_etl_wrapper import Database
from src.main.python.wrapper import Wrapper


__version__ = '0.1.0'

logger = logging.getLogger(__name__)

@click.command()
@click.option('--config', '-c', required=True, metavar='<config_file_path>',
              help='Path to the yaml configuration file.',
              type=click.Path(file_okay=True, exists=True, readable=True))
def main(config):

    # Load configuration
    config = read_yaml_file(Path(config))

    # Setup logging
    debug: bool = config['run_options']['debug_mode']
    setup_logging(debug)

    # Initialize ETL with configuration parameters
    etl = Wrapper(config)
    if config['run_options']['skip_vocabulary_loading']:
        etl.do_skip_vocabulary_loading()

    # TODO: ok to log this here? shall we log it next to wrapper version info?
    logger.info('ETL version {}'.format(__version__))

    # TODO: any situation where we want to use the following? if so, make sure it is part of wrapper code
    # if etl.is_git_repo():
    #     logger.info('Git HEAD at ' + etl.get_git_tag_or_branch())

    # Run ETL
    # TODO: shouldn't any error be already captured by logger?
    try:
        etl.run()
    except Exception as err:
        logger.error('##### FATAL ERROR. TRACEBACK: #####')
        logger.error(traceback.format_exc())
        raise err

if __name__ == "__main__":
    sys.exit(main())
    # TODO: some projects use main(auto_envvar_prefix='ETL'), even if it's not a click parameter;
    #  understand use and either document or remove
