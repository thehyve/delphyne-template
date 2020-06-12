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
import yaml
from omop_etl_wrapper import Database, setup_logging # TODO: check correct dependency names and locations
from src.main.python.wrapper import Wrapper

__version__ = '0.1.0'

logger = logging.getLogger(__name__)

@click.command()
@click.option('--config', '-c', required=True, metavar='<config_file_path>',
              help='Configuration file path in yaml format (./config/config.yml)',
              type=click.Path(file_okay=False, exists=True, readable=True))
def main(config_file_path):

    setup_logging(debug)

    # load configuration file
    with open(config_file_path) as ymlfile:
       config = yaml.load(ymlfile)

    # Test database connection
    uri = f'postgresql://{username}:{password}@{hostname}:{port}/{database}'
    if not Database.can_connect(uri):
        return

    db = Database(uri)

    etl = Wrapper(db, source, cfg)
    if skipvocab:
        etl.do_skip_vocabulary_loading()

    logger.info('ETL version {}'.format(__version__))
    # if etl.is_git_repo():
    #     logger.info('Git HEAD at ' + etl.get_git_tag_or_branch())

    # Run ETL
    try:
        etl.run()
    except Exception as err:
        logger.error('##### FATAL ERROR. TRACEBACK: #####')
        logger.error(traceback.format_exc())
        raise err


if __name__ == "__main__":
    sys.exit(main(auto_envvar_prefix='ETL'))
