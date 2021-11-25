# encoding: utf-8

from flask import redirect, request, render_template
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.operators import all_op
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
from ckanext.dataset_reference.models.package_reference_link import PackageReferenceLink
from datetime import datetime as _time
from ckanext.dataset_reference.libs.helper import Helper
from ckanext.dataset_reference.libs.citation_formatter import CitationFromatter
from bibtexparser.bparser import BibTexParser
import bibtexparser

ADDING_METHOD_DOI = '1'
ADDING_METHOD_BIBTX = '2'
ADDING_METHOD_MANUAL = '3'


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
                    reference_object['adding_method'] = ADDING_METHOD_DOI
                    reference_object['citation'] = citation.get('cite')
                    
            # set fields for a bibtex entry
            if  entry_type == 'bibtex' and bibtex:                
                citation = Helper.process_bibtex(bibtex)
                if citation:
                    reference_object['doi'] = ""
                    reference_object['adding_method'] = ADDING_METHOD_BIBTX
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
            meta_data['package'] = source.package_name
            meta_data['id'] = source.id
            meta_data['adding_method'] = source.adding_method
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
        parser = BibTexParser(common_strings=True)
        try:
            parsed_bibtex_object =  bibtexparser.loads(bibtex, parser).entries[0]
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
            edit_mode="False",
            edit_object = Helper.create_empty_ref_object(),
            selected_ref_type = '',
            selected_year = '',
            selected_thesis = ''
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
                    reference_object['adding_method'] = ADDING_METHOD_MANUAL
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
            if result.adding_method == ADDING_METHOD_MANUAL: 
                publication_types = Helper.get_publication_types_dropdown_content()
                years = Helper.get_years_list()
                thesis_types = [{'value': '0', 'text': 'PhD'}, {'value': '1', 'text': 'Master'}]
                selected_ref_type = Helper.find_selected(result.ref_type, publication_types)
                selected_year = Helper.find_selected(result.year, years)
                selected_thesis = Helper.find_selected(result.thesis_type, thesis_types)
                return render_template('add_manually.html', 
                    pkg_dict=package, 
                    publication_types=publication_types,
                    years=years,
                    thesis_types=thesis_types,
                    edit_mode="True",
                    edit_object = result,
                    selected_ref_type = selected_ref_type,
                    selected_year = selected_year,
                    selected_thesis = selected_thesis
                    )
                
            return toolkit.abort(404, "Function is not available")

        except:
            return toolkit.abort(403, "bad request")
    

    '''
        Save the reference edit
    '''
    def save_edit_ref():
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
                    record = PackageReferenceLink({}).get_by_id(id=request.form.get('ref_id'))
                    record = Helper.update_ref_record(request, record, citation)
                    record.commit()                    

                return h.url_for('dataset.read', id=str(package['id']) ,  _external=True)

            else:
                toolkit.abort(403, "package not specefied")
            
        except:
            toolkit.abort(500, "We cannot process your request at this moment")
    

    '''
        replace and with ; for the edit mode for authors name field
    '''
    def format_authors_name_for_edit(authors_string):
        result = authors_string.replace(' and ', ';')
        return result

    
    def check_authors_format():
        authors_string = request.form.get('authors_string')
        authors_string = authors_string.replace(';' , '')
        authors_string = authors_string.replace(',' , '')
        authors_string = authors_string.replace(' ' , '')
        if not authors_string.isalpha():
            return '0'
            
        return '1'



