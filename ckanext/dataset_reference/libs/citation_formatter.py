# encoding: utf-8


class CitationFromatter():

    def create_citation(response):
        citation_text = ""
        
        # ref type is "Journal Paper" (manually)
        if response['ENTRYTYPE'] in ['Journal Paper']: 
            if response.get('author'):
                citation_text += (response.get('author') + '. ')
            if response.get('year'):
                citation_text += ('(' + response.get('year') + '), ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", ')
            if response.get('journal'):
                citation_text += (response.get('journal') + ', ')
            if response.get('volume'):
                citation_text += ('Vol. ' + response.get('volume') + '  ')
            if response.get('issue'):
                citation_text += ('No. ' + response.get('issue') + ', ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + '. ')  
        
         # ref type is article (bibtex)
        if response['ENTRYTYPE'] in ['article']: 
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + '. ')
            if response.get('journal'):
                citation_text += (response.get('journal') + '., ')
            if response.get('volume'):
                citation_text += ('vol. ' + response.get('volume') + ', ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
            if response.get('month'):
                citation_text += (response.get('month') + ' ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
        # ref type is proceeding paper (Manually)
        elif response['ENTRYTYPE'] in ['Conference Paper']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('year'):
                citation_text += ('(' + response.get('year') + '), ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", ')
            if response.get('proceeding'):
                citation_text += (response.get('proceeding') + ', ')
            if response.get('proceeding_date'):
                citation_text += (response.get('proceeding_date') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
        
        # ref type is proceeding paper (bibtex)
        elif response['ENTRYTYPE'] in ['conference', 'inproceedings', 'proceedings']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", ')
            if response.get('booktitle'):
                citation_text += (response.get('booktitle') + ', ')
            if response.get('series'):
                citation_text += (response.get('series') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')

        
        # ref type is book (bibtex)
        elif response['ENTRYTYPE'] in ['book']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
         # ref type is Book (Manually)
        elif response['ENTRYTYPE'] in ['Book']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('year'):
                citation_text += ('(' + response.get('year') + '), ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
        
        # ref type phd thesis (bibtex)
        elif response['ENTRYTYPE'] in ['phdthesis']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", PhD Thesis, ')
            if response.get('school'):
                citation_text += (response.get('school') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('month'):
                citation_text += (response.get('month') + '. ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
        # ref type Ms thesis (bibtex)
        elif response['ENTRYTYPE'] in ['masterthesis']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", Master Thesis, ')
            if response.get('school'):
                citation_text += (response.get('school') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('month'):
                citation_text += (response.get('month') + '. ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')

         # ref type thesis (manually)
        elif response['ENTRYTYPE'] in ['Thesis']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('year'):
                citation_text += ('(' + response.get('year') + '), ')
            if response.get('title'):
                if response.get('thesis-type') == 'PhD':
                    citation_text += ('"' + response.get('title') + '", [PhD Thesis], ')
                else:
                    citation_text += ('"' + response.get('title') + '", [Master Thesis], ')
            if response.get('school'):
                citation_text += (response.get('school') + ', ')

        # ref type report (bibtex)
        elif response['ENTRYTYPE']  in ['techreport']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", Tech.Rep. ')
            if response.get('number'):
                citation_text += (response.get('number') + ', ')
            if response.get('institution'):
                citation_text += (response.get('institution') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('month'):
                citation_text += (response.get('month') + '. ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
        # ref type report (manually)
        elif response['ENTRYTYPE']  in ['Report']:
            if response.get('org'):
                citation_text += (response.get('org') + '/ ')
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('year'):
                citation_text += ('(' + response.get('year') + '), ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", [Tech.Rep], ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + '.')

        # ref type is Electronic Source (manually)
        elif response['ENTRYTYPE'] == 'Electronic Source':
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('year'):
                citation_text += ('(' + response.get('year') + '), ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '". ')
            if response.get('publisher'):
                citation_text += ('[Online] ' + response.get('publisher') + '. ')
            if response.get('url'):
                citation_text += ('Available at:  ' + response.get('url') + '  ')
            if response.get('access'):
                citation_text += ('(accessed ' + response.get('access') + '). ')

        # ref type is inbook (bibtex)
        elif response['ENTRYTYPE'] in ['inbook']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
            if response.get('address'):
                citation_text += (response.get('address') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('year'):
                citation_text += (response.get('year') + '.')
        
         # ref type is incollection (bibtex)
        elif response['ENTRYTYPE'] in ['incollection']:
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '", ')
            if response.get('editor'):
                citation_text += ('In ' + response.get('editor') + ', editors, ')
            if response.get('booktitle'):
                citation_text += (response.get('booktitle') + ', ')
            if response.get('pages'):
                citation_text += ('pp. ' + response.get('pages') + ', ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')            
            if response.get('address'):
                citation_text += (response.get('address') + ', ')            
            if response.get('year'):
                citation_text += (response.get('year') + '.')

         # ref type is misc (bibtex)
        elif response['ENTRYTYPE'] in ['misc']: 
            if response.get('author'):
                citation_text += (response.get('author') + ', ')
            if response.get('title'):
                citation_text += ('"' + response.get('title') + '". ')
            if response.get('publisher'):
                citation_text += (response.get('publisher') + ', ')
            if response.get('year'):
                citation_text += (response.get('year') + ', ')
            if response.get('doi'):
                citation_text += ( 'doi: ' + response.get('doi') + '.')

        citation_text = citation_text.replace('{', '')
        citation_text = citation_text.replace('}', '')
        return citation_text