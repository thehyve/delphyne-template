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
from pathlib import Path

import click
import sys
from omop_etl_wrapper.config.models import MainConfig
from omop_etl_wrapper.log.setup_logging import setup_logging
from omop_etl_wrapper.util.io import read_yaml_file

from src.main.python.cdm import Base
from src.main.python.wrapper import Wrapper

__version__ = '0.1.0'

logger = logging.getLogger(__name__)


@click.command()
@click.option('--config', '-c', required=True, metavar='<config_file_path>',
              help='Path to the yaml configuration file.',
              type=click.Path(file_okay=True, exists=True, readable=True))
def main(config):
    # Setup logging
    setup_logging()

    # Load configuration
    config = MainConfig(**read_yaml_file(Path(config)))

    # Initialize ETL with configuration parameters
    etl = Wrapper(config, Base)

    # TODO: ok to log this here? shall we log it next to wrapper version info?
    logger.info('ETL version {}'.format(__version__))

    # Run ETL
    etl.run()


if __name__ == "__main__":
    sys.exit(main())
