# encoding: utf-8

from sqlalchemy.sql.expression import false, null
from sqlalchemy.sql.functions import count
import ckan.plugins.toolkit as toolkit
import urllib.request
import ckan.lib.helpers as h
import bibtexparser
from ckanext.dataset_reference.models.package_reference_link import PackageReferenceLink
from datetime import datetime
from ckanext.dataset_reference.libs.citation_formatter import CitationFromatter
from datetime import datetime as _time


Base_doi_api_url = "http://dx.doi.org/"

class Helper():

    '''
        check the user can edit/add a reference or not. The user who can edit the target dataset, also 
        can edit/add reference
    '''
    def check_access_edit_package(package_id):
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':package_id}
        try:
            toolkit.check_access('package_update', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return False
            # toolkit.abort(403, 'You are not authorized to access this function')


    '''
        parse a doi input to get the doi ID
    '''
    def parse_doi_id(url):
        if 'doi.org/' not in url:  # url has to be a doi ID
            return url  

        temp = url.split('doi.org/')
        doi_id = temp[len(temp) - 1]
        return doi_id
    

    '''
        call http://dx.doi.org/ to get the reference metadata
    '''
    def call_api(api_url):
        response = None
        request_header = {'Accept': 'application/x-bibtex'}                
        try:
            req_obj = urllib.request.Request(api_url, headers=request_header)
            with urllib.request.urlopen(req_obj) as url:            
                if url.code == 200:                    
                    response = bibtexparser.load(url).entries[0]
        
            return response
        
        except:
            return None


    '''
        parse the result returned by  http://dx.doi.org/
    '''
    def process_doi_link(doi_link):               
        try:            
            doi_id = Helper.parse_doi_id(doi_link)
            dest_url = Base_doi_api_url + doi_id
            response = Helper.call_api(dest_url)
            if response:                        
                processed_result = {}
                processed_result['cite'] = CitationFromatter.create_citation(response)
                return processed_result            
            else:
                return None        
        except:
            return None
    

    '''
        parse a bibtex input
    '''
    def process_bibtex(bibtex_string):
        parsed_bibtex_object = bibtexparser.loads(bibtex_string).entries[0]
        citation = None
        if parsed_bibtex_object:
            citation = CitationFromatter.create_citation(parsed_bibtex_object)
        return citation


    '''
        fill null citations for a dataset
    '''
    def fill_null_citation(package):
        try:
            res_object = PackageReferenceLink(package_name=package)
            result = res_object.get_by_package(name=package)
            if result == false:
                return False

            for source in result:                        
                if not source.citation or source.citation == null:
                    source.citation = Helper.process_doi_link(source.doi).get('cite')
                    source.commit()
        except:
            return False

        return True


    '''
        check a doi url is valid and exists
    '''
    def check_doi_validity(doi_url):        
        doi = Helper.parse_doi_id(doi_url)
        if not doi:
            return 'url not vaid'
        dest_url = Base_doi_api_url + doi
        response = Helper.call_api(dest_url)
        if response:
            return True

        return None


    '''
        Process the manually added metadata to prepare it the for citation formatter
    '''
    def process_publication_manual_metadata(request):
        reference = {}
        reference['ENTRYTYPE'] = request.form.get('type')
        reference['title'] = request.form.get('title')
        reference['author'] = Helper.format_authors(request.form.get('author'))
        reference['year'] = request.form.get('year')
        reference['url'] = request.form.get('url')

        if reference['ENTRYTYPE'] == 'Journal Paper':
            reference['journal'] = request.form.get('journal')
            reference['volume'] = request.form.get('volume')
            reference['pages'] = request.form.get('page')
            reference['issue'] = request.form.get('issue')

        elif reference['ENTRYTYPE'] == 'Conference Paper':
            reference['proceeding'] = request.form.get('proceeding')
            reference['proceeding_date'] = request.form.get('proceeding_date')
            reference['pages'] = request.form.get('page')
            reference['address'] = request.form.get('address')
            reference['publisher'] = request.form.get('publisher')
        
        elif reference['ENTRYTYPE'] == 'Report':
            reference['publisher'] = request.form.get('publisher')
            reference['org'] = request.form.get('org')
            reference['address'] = request.form.get('address')
        
        elif reference['ENTRYTYPE'] == 'Book':                           
            reference['address'] = request.form.get('address')
            reference['publisher'] = request.form.get('publisher')
        
        elif reference['ENTRYTYPE'] == 'Thesis':
            reference['school'] = request.form.get('school')
            reference['thesis-type'] = request.form.get('thesis-type')
        
        elif reference['ENTRYTYPE'] == 'Electronic Source':
            reference['access'] = request.form.get('access')
            
        else:
            reference['ENTRYTYPE'] = 'misc'
            reference['doi'] = ''

        return reference


    '''
        create the dictaionary of the reference metadata to save in db
    '''
    def create_object_for_db(request, citation):
        reference = {}
        reference['package_name'] = request.form.get('package')
        reference['doi'] = ''
        reference['create_at'] =  _time.now()
        reference['citation'] = citation
        reference['ref_type'] = request.form.get('type')
        reference['title'] = request.form.get('title')
        reference['authors'] = Helper.format_authors(request.form.get('author'))
        reference['year'] = request.form.get('year')
        reference['url'] = request.form.get('url')
        reference['journal'] = request.form.get('journal')
        reference['volume'] = request.form.get('volume')
        reference['page'] = request.form.get('page')
        reference['issue'] = request.form.get('issue')
        reference['proceeding'] = request.form.get('proceeding')
        reference['conference_date'] = request.form.get('proceeding_date')
        reference['place'] = request.form.get('address')
        reference['publisher'] = request.form.get('publisher')
        reference['access_date'] = request.form.get('access')
        reference['thesis_type'] = request.form.get('thesis-type')
        if request.form.get('type') == 'Report':
            reference['organization'] = request.form.get('org')
        else:
            reference['organization'] = request.form.get('school')
            
        return reference
    

    '''
        update an edited ref
    '''
    def update_ref_record(request, record, citation):
        if request.form.get('type') == 'Journal Paper':
            record.citation = citation
            record.ref_type = request.form.get('type')
            record.title = request.form.get('title')
            record.authors = Helper.format_authors(request.form.get('author'))
            record.year = request.form.get('year')
            record.url =  request.form.get('url')
            record.journal = request.form.get('journal')
            record.volume = request.form.get('volume')
            record.issue = request.form.get('issue')
            record.page = request.form.get('page')
            record.proceeding = ''
            record.conference_date = ''
            record.place = ''
            record.publisher = ''
            record.access_date = ''
            record.thesis_type = ''
            record.organization = ''
        
        elif request.form.get('type') == 'Report':
            record.citation = citation
            record.ref_type = request.form.get('type')
            record.title = request.form.get('title')
            record.authors = Helper.format_authors(request.form.get('author'))
            record.year = request.form.get('year')
            record.url =  request.form.get('url')
            record.journal = ''
            record.volume = ''
            record.issue = ''
            record.page = ''
            record.proceeding = ''
            record.conference_date = ''
            record.place = request.form.get('address')
            record.publisher = request.form.get('publisher')
            record.access_date = ''
            record.thesis_type = ''
            record.organization = request.form.get('org')
        
        elif request.form.get('type') == 'Conference Paper':
            record.citation = citation
            record.ref_type = request.form.get('type')
            record.title = request.form.get('title')
            record.authors = Helper.format_authors(request.form.get('author'))
            record.year = request.form.get('year')
            record.url =  request.form.get('url')
            record.journal = ''
            record.volume = ''
            record.issue = ''
            record.page =  request.form.get('page')
            record.proceeding = request.form.get('proceeding')
            record.conference_date = request.form.get('proceeding_date')
            record.place = request.form.get('address')
            record.publisher = request.form.get('publisher')
            record.access_date = ''
            record.thesis_type = ''
            record.organization = ''
        
        elif request.form.get('type') == 'Book':
            record.citation = citation
            record.ref_type = request.form.get('type')
            record.title = request.form.get('title')
            record.authors = Helper.format_authors(request.form.get('author'))
            record.year = request.form.get('year')
            record.url =  request.form.get('url')
            record.journal = ''
            record.volume = ''
            record.issue = ''
            record.page = ''
            record.proceeding = ''
            record.conference_date = ''
            record.place = request.form.get('address')
            record.publisher = request.form.get('publisher')
            record.access_date = ''
            record.thesis_type = ''
            record.organization = ''
        
        elif request.form.get('type') == 'Thesis':
            record.citation = citation
            record.ref_type = request.form.get('type')
            record.title = request.form.get('title')
            record.authors = Helper.format_authors(request.form.get('author'))
            record.year = request.form.get('year')
            record.url =  request.form.get('url')
            record.journal = ''
            record.volume = ''
            record.issue = ''
            record.page = ''
            record.proceeding = ''
            record.conference_date = ''
            record.place = ''
            record.publisher = ''
            record.access_date = ''
            record.thesis_type = request.form.get('thesis-type')
            record.organization = request.form.get('school')
        
        elif request.form.get('type') == 'Electronic Source':
            record.citation = citation
            record.ref_type = request.form.get('type')
            record.title = request.form.get('title')
            record.authors = Helper.format_authors(request.form.get('author'))
            record.year = request.form.get('year')
            record.url =  request.form.get('url')
            record.journal = ''
            record.volume = ''
            record.issue = ''
            record.page = ''
            record.proceeding = ''
            record.conference_date = ''
            record.place = ''
            record.publisher = ''
            record.access_date = request.form.get('access')
            record.thesis_type = ''
            record.organization = ''

        return record


    '''
        create the dictaionary of an empty reference metadata 
    '''
    def create_empty_ref_object():
        reference = {}
        reference['id'] = ''
        reference['doi'] = ''
        reference['ref_type'] = ''
        reference['title'] = ''
        reference['authors'] = ''
        reference['year'] = ''
        reference['url'] = ''
        reference['journal'] = ''
        reference['volume'] = ''
        reference['page'] = ''
        reference['issue'] = ''
        reference['proceeding'] = ''
        reference['conference_date'] = ''
        reference['place'] = ''
        reference['publisher'] = ''
        reference['access_date'] = ''
        reference['thesis_type'] = ''
        reference['organization'] = ''
            
        return reference


    '''
        find the selected item for the dit mode
    '''
    def find_selected(item, target):
        for su in target:
            if su['text'] == item:
                return su['value']
        return ''


    '''
        format the authors list to replace ";" with "and"
    '''
    def format_authors(author_string):
        if author_string:
            if author_string[len(author_string) - 1] == ';':
                author_string = author_string[:len(author_string) - 1]
            return author_string.replace(';', ' and ')

        return author_string

    

    '''
        prepare the reference types for manually adding
    '''
    def get_publication_types_dropdown_content():
        publication_types = []
        Types = ['Not Selected',
            'Book', 
            'Journal Paper', 
            'Conference Paper', 
            'Thesis', 
            'Electronic Source', 
            'Report'
            ]
        counter = 0        
        for t in Types:
            temp = {}
            temp['value'] = str(counter)
            temp['text'] = t
            publication_types.append(temp)
            counter += 1

        return publication_types

    
    '''
        prepare the years list for manually adding
    '''
    def get_years_list():
        years = []        
        current_year = datetime.now().year
        counter = 0
        for i in list(reversed(range(1900, current_year + 1))):
            temp = {}
            temp['value'] = str(counter)
            temp['text'] = str(i)
            years.append(temp)
            counter += 1
        return years

    
    '''
        prepare the months list for manually adding
    '''
    def get_month_list():
        months = []
        texts = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        values = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for i in range(0, 12):
            temp = {}
            temp['value'] = values[i]
            temp['text'] = texts[i]
            months.append(temp)

        return months


    '''
        create the table view for references
    '''
    def create_table_row(meta_data, object_id, is_auth_to_delete):
        row = '<tr>'
        row = row +  '<td>' +  meta_data['cite'] + '</td>'   
        if meta_data['link'] and meta_data['link'] != '':      
            row = row +  '<td><a href="' +  meta_data['link'] + '" target="_blank">Link</a></td>'
        else:
            row = row +  '<td>None</td>'
       
        if is_auth_to_delete:
            row = row +  '<td>' +  Helper.create_delete_modal(object_id) + '<br>'  
            if meta_data['adding_method'] == '3': # manually added
                row = row +  '<a href="' + h.url_for('dataset_reference.edit_reference', package_name=str(meta_data['package']), ref_id=str(meta_data['id']))  + '"><i class="fa fa-edit"></i></a>'  
        row = row +  '</td>'
        row = row +  '</tr>'
        return row
    

    '''
        create the modal view for deleteing a reference
    '''
    def create_delete_modal(object_id):
        delete_url = h.url_for('dataset_reference.delete_doi', doi_id=str(object_id) ,  _external=True)
        modal = '<a href="#" type="button" data-toggle="modal" data-target="#deleteModal' + str(object_id) +  '"><i class="fa fa-trash-o"></i></a>'
        modal += '<div id="deleteModal' + str(object_id)  + '" class="modal fade" role="dialog">'
        modal += '<div class="modal-dialog">'
        modal += '<div class="modal-content">'
        modal += '<div class="modal-header">'
        modal += '<button type="button" class="close" data-dismiss="modal">&times;</button>'
        modal += '</div>'
        modal += '<div class="modal-body">'
        modal += '<p><h3>Are you sure about deleting this material?</h3></p>'
        modal += '</div>'
        modal += '<div class="modal-footer">'
        modal += '<a href="' + delete_url + '" type="button" class="btn btn-danger">Delete</a>'
        modal += '<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>'
        modal += '</div>'
        modal += '</div>'
        modal += '</div>'
        modal += '</div>'
                
        return modal