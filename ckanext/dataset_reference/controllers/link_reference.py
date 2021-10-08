# encoding: utf-8

from flask import redirect, request, render_template
from sqlalchemy.sql.expression import false
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
from ckanext.dataset_reference.models.package_reference_link import PackageReferenceLink
from datetime import datetime as _time
from ckanext.dataset_reference.libs.helper import Helper
from ckanext.dataset_reference.libs.citation_formatter import CitationFromatter
import bibtexparser


class LinkReferenceController():

    '''
        save the reference added via doi or bibtex
    '''
    def save_doi():
        package_id = request.form.get('package_id') 
        entry_type = request.form.get('doi_or_bibtex')     
        doi = request.form.get('doi')       
        bibtex = request.form.get('bibtex')
        if not Helper.check_access_edit_package(package_id):
            toolkit.abort(403, 'You are not authorized to access this function')
        
        reference_object = {}
        reference_object['create_at'] = _time.now()

        try:
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_id})
            reference_object['package_name'] = package['name']

             # set fields for a doi url/id
            if entry_type == 'doi' and doi and Helper.check_doi_validity(doi) == True:
                citation = Helper.process_doi_link(doi)
                if citation:
                    reference_object['doi'] = doi
                    reference_object['citation'] = citation.get('cite')
                    
            # set fields for a bibtex entry
            if  entry_type == 'bibtex' and bibtex:                
                citation = Helper.process_bibtex(bibtex)
                if citation:
                    reference_object['doi'] = ""
                    reference_object['citation'] = citation
            
            record = PackageReferenceLink(reference_object)
            record.save()
            return  redirect(h.url_for('dataset.read', id=str(package_id) ,  _external=True))  

        except:
            return toolkit.abort(403, "bad request")


    '''
        get the references for a dataset to show on the reference table
    '''
    def get_publication(name):        
        Helper.fill_null_citation(name)
        reference_object = {}
        reference_object['package_name'] = name
        res_object = PackageReferenceLink(reference_object)
        package = toolkit.get_action('package_show')({}, {'name_or_id': name})
        result = res_object.get_by_package(name=name)
        return_rows = ""
        if result == false: ## there is no reference for this dataset
            return '0'
        for source in result:
            if not source.citation:
                continue
            meta_data = {}
            meta_data['cite'] = source.citation
            if source.doi != '':
                meta_data['link'] = source.doi
            else:
                meta_data['link'] = source.url
            return_rows += Helper.create_table_row(meta_data, source.id, Helper.check_access_edit_package(package['id']))
        
        if return_rows != "":
            return return_rows
        
        return '0'
    

    '''
        check the doi url/id validity (exist or not)
    '''
    def doi_is_valid():
        doi_url = request.form.get('doi_url')
        response = Helper.check_doi_validity(doi_url)
        if not response:
            return 'There is no information about this DOI URL or ID'
        
        elif response == 'url not vaid':
            return 'Please enter a valid doi url. Ex: https://www.doi.org/DOI_ID'
        
        return '1'
    

    '''
        check the bibtex syntax validity
    '''
    def bibtex_is_valid():
        bibtex = request.form.get('bibtex')
        try:
            parsed_bibtex_object = bibtexparser.loads(bibtex).entries[0]
        except:
            return "Please enter a valid BibTex format."

        return '1'
    

    '''
        delete a reference
    '''
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
    

    '''
        render the add reference manually view
    '''
    def add_publication_manually(package_name):
        package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
        publication_types = Helper.get_publication_types_dropdown_content()
        years = Helper.get_years_list()
        thesis_types = [{'value': 'PhD', 'text': 'PhD'}, {'value': 'Master', 'text': 'Master'}]

        return render_template('add_manually.html', 
            pkg_dict=package, 
            publication_types=publication_types,
            years=years,
            thesis_types=thesis_types,
            )
    
    '''
        save the manually added reference
    '''
    def save_publication_manually():
        try:
            package_name = request.form.get('package')
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
            if request.form.get('cancel'):
                return h.url_for('dataset.read', id=str(package['id']) ,  _external=True)
                
            if package_name:                
                Helper.check_access_edit_package(package['id'])
                reference = Helper.process_publication_manual_metadata(request)
                citation = CitationFromatter.create_citation(reference)
                if citation != "":
                    reference_object = Helper.create_object_for_db(request, citation)
                    record = PackageReferenceLink(reference_object)
                    record.save()                    

                return h.url_for('dataset.read', id=str(package['id']) ,  _external=True)

            else:
                toolkit.abort(403, "package not specefied")
            
        except:
            toolkit.abort(500, "We cannot process your request at this moment")
    

    '''
        render the edit view for a manually added reference
    '''
    def edit_reference(package_name, ref_id):
        try:
            package = toolkit.get_action('package_show')({}, {'name_or_id': package_name})
            if not Helper.check_access_edit_package(package['id']):
                return toolkit.abort(403, 'You are not authorized to access this function')
            reference_object = {}
            reference_object['package_name'] = package_name
            res_object = PackageReferenceLink(reference_object)
            result = res_object.get_by_id(id=ref_id)
            
            
            
            
            
            
            return result.citation

        except:
            return toolkit.abort(403, "bad request")



