# encoding: utf-8

from flask import redirect, request, render_template
from sqlalchemy.sql.expression import false
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
from ckanext.dataset_reference.models.package_reference_link import PackageReferenceLink
from datetime import datetime as _time
from ckanext.dataset_reference.libs.helper import Helper


class LinkReferenceController():

    def save_doi():
        package_id = request.form.get('package_id')       
        doi = request.form.get('doi')       
        if not Helper.check_access_edit_package(package_id):
            toolkit.abort(403, 'You are not authorized to access this function')

        if package_id and doi and Helper.check_doi_validity(doi) == True:
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_id})
            try:
                citation = Helper.process_doi_link(doi)
                if citation:
                    reference_object = {}
                    reference_object['package_name'] = package['name']
                    reference_object['doi'] = doi
                    reference_object['create_at'] = _time.now()
                    reference_object['citation'] = citation.get('cite')
                    record = PackageReferenceLink(reference_object)
                    record.save()
                return  redirect(h.url_for('dataset.read', id=str(package_id) ,  _external=True))   
            except:
                return toolkit.abort(403, "bad request")
            
        else:
            return toolkit.abort(403, "bad request")
    


    def get_publication(name):        
        Helper.fill_null_citation(name)
        reference_object = {}
        reference_object['package_name'] = name
        res_object = PackageReferenceLink(reference_object)
        package = toolkit.get_action('package_show')({}, {'name_or_id': name})
        result = res_object.get_by_package(name=name)
        return_rows = ""
        if result == false:
            return '0'
        for source in result:
            if not source.citation:
                continue
            meta_data = {}
            meta_data['cite'] = source.citation
            if meta_data:
                meta_data['link'] = source.doi
                return_rows += Helper.create_table_row(meta_data, source.id, Helper.check_access_edit_package(package['id']))
        
        if return_rows != "":
            return return_rows
        
        return '0'
    

    def doi_is_valid():
        doi_url = request.form.get('doi_url')
        response = Helper.check_doi_validity(doi_url)
        if not response:
            return 'There is no information about this doi url'
        
        elif response == 'url not vaid':
            return 'Please enter a valid doi url. Ex: https://www.doi.org/DOI_ID'
        
        return '1'
    

    def delete_doi(doi_id):
        res_object = PackageReferenceLink({})
        doi_obj = res_object.get_by_id(id=doi_id)
        package_name = doi_obj.package_name
        package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
        if not Helper.check_access_edit_package(package['id']):
            toolkit.abort(403, 'You are not authorized to access this function')
        try:            
            doi_obj.delete()
            doi_obj.commit()
            return  redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True)) 

        except:
            return toolkit.abort(403, "bad request")
    

    def add_publication_manually(package_name):
        package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
        publication_types = Helper.get_publication_types_dropdown_content()
        years = Helper.get_years_list()

        return render_template('add_manually.html', 
            pkg_dict=package, 
            publication_types=publication_types,
            years=years,
            )
    

    def save_publication_manually():
        try:
            package_name = request.form.get('package')
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
            if request.form.get('cancel'):
                return h.url_for('dataset.read', id=str(package['id']) ,  _external=True)
                
            if package_name:                
                Helper.check_access_edit_package(package['id'])
                reference = Helper.process_publication_manual_metadata(request)
                citation = Helper.create_citation(reference)
                if citation != "":
                    record = PackageReferenceLink(package_name=package_name, doi='', create_at = _time.now(), citation=citation)
                    record.save()                    

                return h.url_for('dataset.read', id=str(package['id']) ,  _external=True)

            else:
                toolkit.abort(403, "package not specefied")
            
        except:
            toolkit.abort(500, "We cannot process your request at this moment")

