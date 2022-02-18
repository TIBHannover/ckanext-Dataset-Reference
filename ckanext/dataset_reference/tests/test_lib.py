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
    

    def test_call_api(self):
        '''
            test the calling of doi.org api for fetching a reference metadata based on doi id.

            Scenario 1:
                - input: 10.1007/978-3-030-57717-9_36
                - output: the reference metadata
            
            Scenario 1:
                - input: false_id
                - output: None
        '''

        input1 = '10.1007/978-3-030-57717-9_36'
        input2 = 'false_id'
        api_url_base = 'http://dx.doi.org/'
        assert Helper.call_api(api_url_base + input1) != None
        assert Helper.call_api(api_url_base + input2) == None
    


    def test_process_doi_link(self):
        '''
            The process_doi_link function parse the metadata returned by calling the doi.org API.

            Scenario 1:
                - input: 'https://doi.org/10.1007/978-3-030-57717-9_36'
                - output: a dictionary
            
            Scenario 2:
                - input: 'url_with_false_id'
                - output: None
        '''

        input1 = 'https://doi.org/10.1007/978-3-030-57717-9_36'
        input2 = 'url_with_false_id'
        assert Helper.process_doi_link(input1).get('cite') != None
        assert Helper.process_doi_link(input2) == None

    

 
