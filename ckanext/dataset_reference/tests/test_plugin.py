# encoding: utf-8 

'''
    Test Class for the dataset_reference plugin
'''

import pytest

import ckan.tests.factories as factories
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.create_test_data as ctd



@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestDatasetReference(object):




    def test_add_reference_with_doi_when_doi_is_valid(self, app):
        

        pass
