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

from pathlib import Path
import logging
import pandas as pd
from omop_etl_wrapper import Wrapper as BaseWrapper
from src.main.python.transformation import *
from src.main.python.model.sourcedata import SourceData # TODO: use local version for the moment, will be made general (for data files & database)
from src.main.python.util import VariableConceptMapper # TODO: add to package?
from src.main.python.util import OntologyConceptMapper # TODO: add to package?
from src.main.python.util import RegimenExposureMapper # TODO: add to package?

# NOTE: select the desired target CDM version below
from omop_etl_wrapper.cdm import hybrid as cdm
# from omop_etl_wrapper.cdm import cdm531 as cdm
# from omop_etl_wrapper.cdm import cdm600 as cdm


logger = logging.getLogger(__name__)


class Wrapper(BaseWrapper):
    cdm = cdm

    def __init__(self, config):
        super().__init__(config)
        # Load config settings
        self.source_folder = Path(config['run_options']['source_data_folder'])
        self.path_mapping_tables = Path('./resources/mapping_tables')
        self.path_custom_vocabularies = Path('./resources/custom_vocabularies')
        self.path_sql_transformations = Path('./src/main/sql')
        self.skip_vocabulary_loading: bool = config['run_options']['skip_vocabulary_loading']
        # Load data to objects
        # self.variable_concept_mapper = VariableConceptMapper(self.path_mapping_tables)
        # self.ontology_concept_mapper = OntologyConceptMapper(self.path_mapping_tables)
        # self.regimen_exposure_mapper = RegimenExposureMapper(self.path_mapping_tables)
        # NOTE: replace the following with project-specific source table names!
        self.sample_source_table = None

    def transform(self):

        # NOTE: replace the following with project-specific transformations from python/transformations/ or sql/ folder!
        # make sure execution follows order of table dependencies (see cdm model)
        self.execute_transformation(dm_to_person)
        self.execute_transformation(sample_source_table_to_person)
        # self.execute_sql_file(self.path_sql_transformations / 'sample_script.sql')

    def run(self):

        # self.start_timing()

        logger.info('{:-^100}'.format(' Source Counts '))
        # self.log_tables_rowcounts(self.source_folder)

        logger.info('{:-^100}'.format(' Setup '))

        # Prepare source
        self.create_schemas()
        self.drop_cdm()
        self.create_cdm()

        # Load custom concepts
        if not self.skip_vocabulary_loading:
            logger.info('Loading custom vocabularies')
            self.load_custom_vocabulary_tables()

        # Load source to concept mappings
        self.truncate_stcm_table()
        self.load_stcm()

        # Load source data

        logger.info('{:-^100}'.format(' ETL '))

        # These queries are cdm6 specific
        # self.stem_table_to_domains()

        self.transform()

        self.etl_stats.write_summary_files()
        self.etl_stats.log_summary()

        # self.log_summary()
        # self.log_runtime()

    # TODO: change the following to load these programmatically from a source data folder?
    # NOTE: replace the following with project-specific source tables and function names!
    def get_sample_source_table(self):
        if not self.sample_source_table:
            self.sample_source_table = SourceData(self.source_folder / 'sample_source_table.csv')
        return self.sample_source_table

    def load_custom_vocabulary_tables(self):

        # patterns
        VOCAB_FILE_PATTERN = '*_vocabulary.tsv'
        CLASS_FILE_PATTERN = '*_concept_class.tsv'
        CONCEPT_FILE_PATTERN = '*_concept.tsv'

        # TODO: quality checks: mandatory fields, dependencies
        # self.check_custom_vocabularies_format()

        vocab_ids, vocab_files = self.get_custom_vocabulary_ids_and_files(VOCAB_FILE_PATTERN)
        class_ids, class_files = self.get_custom_class_ids_and_files(CLASS_FILE_PATTERN)

        # drop older versions
        self.drop_custom_concepts(vocab_ids)
        self.drop_custom_vocabularies(vocab_ids)
        self.drop_custom_classes(class_ids)
        # load new versions
        self.load_custom_classes(class_ids, class_files)
        self.load_custom_vocabularies(vocab_ids, vocab_files)
        self.load_custom_concepts(vocab_ids, CONCEPT_FILE_PATTERN)
        # TODO: remove obsolete versions (i.e. cleanup in case of renaming of vocabs/classes);
        #  if the name has been changed, the previous drop won't find them;
        #  NOTE: for this to work, you need to keep a list of valid Athena vocabulary ids
        #  and check that no unknown vocabulary is present (not in Athena or custom vocab files);
        #  the cleanup could be rather time-consuming and should not be executed every time
        valid_vocabs = self.get_list_of_valid_vocabularies()
        self.drop_unused_custom_concepts(valid_vocabs)
        self.drop_unused_custom_vocabularies(valid_vocabs)
        valid_classes = self.get_list_of_valid_classes()
        self.drop_unused_custom_classes(valid_classes)

    def get_custom_vocabulary_ids_and_files(self, file_pattern):

        vocab_ids = set()
        vocab_files = set()

        for vocab_file in self.path_custom_vocabularies.glob(file_pattern):

            df = pd.read_csv(vocab_file, sep='\t')
            for _,row in df.iterrows():
                vocab_id = df['vocabulary_id']
                vocab_version =  df['vocabulary_version']

                if self.check_if_existing_vocab_version(vocab_id, vocab_version):
                    continue

                vocab_ids.add(vocab_id)
                vocab_files.add(vocab_file.name)

        return list(vocab_ids), list(vocab_files)

    def check_if_existing_vocab_version(self, vocab_id, vocab_version):

        with self.db.session_scope() as session:
            existing_record = \
                session.query(cdm.Vocabulary) \
                .filter(cdm.Vocabulary.vocabulary_id == vocab_id) \
                .filter(cdm.Vocabulary.vocabulary_version == vocab_version) \
                .one_or_none()
            return False if not existing_record else True

    def get_custom_class_ids_and_files(self, file_pattern):

        class_ids = set()
        class_files = set()

        for class_file in self.path_custom_vocabularies.glob(file_pattern):
            df = pd.read_csv(class_file, sep='\t')
            for _, row in df.iterrows():
                class_id = df['concept_class_id']
                class_name = df['concept_class_name']
                class_concept_id = df['concept_class_concept_id']

                if self.check_if_existing_custom_class(class_id, class_name, class_concept_id):
                    continue

                class_ids.add(class_id)
                class_files.add(class_file)

        return list(class_ids), list(class_files)

    def check_if_existing_custom_class(self, class_id, class_name, class_concept_id):

        with self.db.session_scope() as session:
            existing_record = \
                session.query(cdm.ConceptClass) \
                .filter(cdm.ConceptClass.concept_class_id == class_id) \
                .filter(cdm.ConceptClass.concept_class_name == class_name) \
                .filter(cdm.ConceptClass.concept_class_concept_id == class_concept_id) \
                .one_or_none()
            return False if not existing_record else True

    def drop_custom_concepts(self, vocab_ids):

        if vocab_ids:
            with self.db.session_scope() as session:
                session.query(cdm.Concept) \
                    .filter(cdm.Concept.vocabulary_id._in(vocab_ids)) \
                    .delete()

    def drop_custom_vocabularies(self, vocab_ids):

        if vocab_ids:
            with self.db.session_scope() as session:
                session.query(cdm.Vocabulary) \
                    .filter(cdm.Vocabulary.vocabulary_id._in(vocab_ids)) \
                    .delete()

    def drop_custom_classes(self, class_ids):

        if class_ids:
            with self.db.session_scope() as session:
                session.query(cdm.ConceptClass) \
                    .filter(cdm.ConceptClass.concept_class_id._in(class_ids)) \
                    .delete()

    def load_custom_classes(self, class_ids, class_files):

        if class_ids:

            with self.db.session_scope() as session:

                for class_file in class_files:
                    df = pd.read_csv(self.path_custom_vocabularies / class_file, sep='\t')
                    df = df[df['concept_class_id'].isin(class_ids)]

                    records = []
                    for _,row in df.iterrows():
                        records.append(cdm.ConceptClass(
                            concept_class_id=row['concept_class_id'],
                            concept_class_name=row['concept_class_id'],
                            concept_class_concept_id=row['concept_class_concept_id']
                        ))
                    session.add_all(records)

    def load_custom_vocabularies(self, vocab_ids, vocab_files):

        if vocab_ids:

            with self.db.session_scope() as session:

                for vocab_file in vocab_files:
                    df = pd.read_csv(self.path_custom_vocabularies / vocab_file, sep='\t')
                    df = df[df['vocabulary_id'].isin(vocab_ids)]

                    records = []
                    for _, row in df.iterrows():
                        records.append(cdm.Vocabulary(
                            vocabulary_id=row['vocabulary_id'],
                            vocabulary_name=row['vocabulary_name'],
                            vocabulary_reference=row['vocabulary_reference'],
                            vocabulary_version=row['vocabulary_version'],
                            vocabulary_concept_id=row['vocabulary_concept_id']
                        ))
                    session.add_all(records)

    def load_custom_concepts(self, vocab_ids, concept_file_pattern):

        if vocab_ids:

            with self.db.session_scope() as session:

                for concept_file in self.path_custom_vocabularies.glob(concept_file_pattern):
                    df = pd.read_csv(concept_file, sep='\t')
                    df = df[df['vocabulary_id'].isin(vocab_ids)]

                    records = []
                    for _, row in df.iterrows():
                        records.append(cdm.Concept(
                            concept_id=row['concept_id'],
                            concept_name=row['concept_name'],
                            domain_id=row['domain_id'],
                            vocabulary_id=row['vocabulary_id'],
                            concept_class_id=row['concept_class_id'],
                            standard_concept=row['standard_concept'],
                            concept_code=row['concept_code'],
                            valid_start_date=row['valid_start_date'],
                            valid_end_date=row['valid_end_date'],
                            invalid_reason=row['invalid_reason']
                        ))
                    session.add_all(records)

    def get_list_of_valid_vocabularies(self):
        pass

    def get_list_of_valid_classes(self):
        pass

    def drop_unused_custom_concepts(self, vocab_ids):
        pass

    def drop_unused_custom_vocabularies(self, vocab_ids):
        pass

    def drop_unused_custom_classes(self, class_ids):
        pass

