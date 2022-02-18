# encoding: utf-8 

'''
    Test Class for the dataset_reference plugin
'''

import pytest

import ckan.tests.factories as factories
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.create_test_data as ctd




@pytest.mark.ckan_config('ckan.plugins', 'dataset_reference')
@pytest.mark.usefixtures('with_plugins', 'with_request_context')
class TestControllers(object):

    @pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
    def test_add_reference_with_doi_when_doi_is_valid(self, app, migrate_db_for):
        '''
            A user has to be able to add a reference
            with a doi url
        '''
        # ctd.CreateTestData.create()
        migrate_db_for("dataset_reference")
        sysadmin_user = model.User.get("testsysadmin")
        owner_org = factories.Organization(users=[{
            'name': sysadmin_user.id,
            'capacity': 'member'
        }])
        dataset = factories.Dataset(owner_org=owner_org['id'])  
        auth = {u"Authorization": str(sysadmin_user.apikey)}
        data = {
            'package_id': dataset['id'],
            'doi_or_bibtex': 'doi',
            'doi': 'https://doi.org/10.1007/978-3-030-57717-9_36'
        }
        dest_url = h.url_for('dataset_reference.save_doi')
        response = app.post(dest_url, data=data, extra_environ=auth)    
        assert response.status_code == 200
        assert True == True
    


    def test_doi_is_valid_call(self, app):
        '''
            The doi url/id need to be checked via ajax request for sake of form validation 
            on client side.
        '''

        input1 = 'https://doi.org/10.1007/978-3-030-57717-9_36'
        input2 = '10.1007/978-3-030-57717-9_36'
        input3 = 'https://example.org/10.1007/978-3-030-57717-9_36'
        ctd.CreateTestData.create()
        
        sysadmin_user = model.User.get("testsysadmin")
        auth = {u"Authorization": str(sysadmin_user.apikey)}
        dest_url = h.url_for('dataset_reference.doi_is_valid')
        data = {
            'doi_url': input1,
        }
        
        response = app.post(dest_url, data=data, extra_environ=auth)
        assert '1' in response.body
        



        
