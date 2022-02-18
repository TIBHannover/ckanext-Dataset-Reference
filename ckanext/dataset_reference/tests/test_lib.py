# encoding: utf-8

import pytest
import ckan.tests.factories as factories
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.create_test_data as ctd
from ckanext.dataset_reference.libs.helper import Helper


class TestLibraryFunctions(object):


    def test_parse_doi_id(self):
        '''
            Test the parse_doi_id function. The function parses a doi url to extract the doi id.
            Scenario 1:
                - input: https://example.org/10.1007/978-3-030-57717-9_36
                - output: https://example.org/10.1007/978-3-030-57717-9_36
            
            Scenario 2:
                - input: 10.1007/978-3-030-57717-9_36
                - output: 10.1007/978-3-030-57717-9_36
            
            Scenario 3:
                - input: https://doi.org/10.1007/978-3-030-57717-9_36
                - output: 10.1007/978-3-030-57717-9_36
        '''

        input1 = 'https://example.org/10.1007/978-3-030-57717-9_36'
        input2 = '10.1007/978-3-030-57717-9_36'
        input3 = 'https://doi.org/10.1007/978-3-030-57717-9_36'
        assert Helper.parse_doi_id(input1) == input1
        assert Helper.parse_doi_id(input2) == '10.1007/978-3-030-57717-9_36'
        assert Helper.parse_doi_id(input3) == '10.1007/978-3-030-57717-9_36'
    

    
    

 
