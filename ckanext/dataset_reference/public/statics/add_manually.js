$(document).ready(function(){
    $("#pub-type").select2();
    $('#years-select').select2();
    $('select.month-select').select2();

    $('#pub-type').change(function(){
        let pubType = $(this).select2('data').text;
        if (pubType == 'article'){
            $('.pub-type-section').hide();
            $('#article-section').fadeIn();
        }
        else if (pubType == 'techreport'){
            $('.pub-type-section').hide();
            $('#section-tech-report').fadeIn();
        }
        else if (['conference', 'inproceedings', 'proceedings'].includes(pubType)){
            $('.pub-type-section').hide();
            $('#conference-section').fadeIn();
        }
        else if (pubType == 'inbook'){
            $('.pub-type-section').hide();
            $('#inbook-section').fadeIn();
        }
        else if (pubType == 'incollection'){
            $('.pub-type-section').hide();
            $('#incollecion-section').fadeIn();
        }
        else if (pubType == 'book'){
            $('.pub-type-section').hide();
            $('#book-section').fadeIn();
        }
        else if (['masterthesis', 'phdthesis'].includes(pubType)){
            $('.pub-type-section').hide();
            $('#thesis-section').fadeIn();
        }
        else{
            $('.pub-type-section').hide();            
        }

    });

    $('#save-btn').click(function(){        
        let form_validity = form_validator();        
        if(form_validity){
            send_data();
        }        
    });

    $('#cancel-btn').click(function(){        
        send_data(true);        
    });

});


function form_validator(){
    let result = true;
    $('.pub-type-select').css('border', '');
    $('#pub-title').css('border', '');
    $('#authors').css('border', '');
    if ($('#pub-type').select2('data') == null){        
        $('.pub-type-select').css('border', '2px solid red');
        result = false;
    }
    if ($('#pub-title').val() == ''){        
        $('#pub-title').css('border', '2px solid red');
        result = false;
    }
    if ($('#authors').val() == ''){        
        $('#authors').css('border', '2px solid red');
        result = false;
    }
    if(!result){
        $('#mandatory-text').css('color', 'red');
    }

    return result;
}


function send_data(is_cancel=false){
    var formdata = new FormData();
    if (is_cancel){
        formdata.set('cancel', '1');
        formdata.set('package', $('#package').val());
        send_request(formdata);
        return 1;
    }
    let pubType = $('#pub-type').select2('data').text;    
    formdata.set('package', $('#package').val());
    formdata.set('type', pubType);
    formdata.set('title', $('#pub-title').val()); 
    formdata.set('author', $('#authors').val());
    formdata.set('year', $('#years-select').select2('data').text);
    formdata.set('publisher', $('#publisher').val());
   
    if (pubType == 'article'){
        formdata.set('journal', $('#article-journal').val());
        formdata.set('volume', $('#article-volume').val());
        formdata.set('page', $('#article-pages').val());
        formdata.set('month', $('#article-month').select2('data').text);
        send_request(formdata);

    }
    else if (pubType == 'techreport'){
        formdata.set('number', $('#report-number').val());
        formdata.set('institutaion', $('#report-number').val());
        formdata.set('month', $('#report-month').select2('data').text);
        formdata.set('address', $('#report-address').val());
        send_request(formdata);

    }
    else if (['conference', 'inproceedings', 'proceedings'].includes(pubType)){
        formdata.set('booktitle', $('#conf-booktitle').val());
        formdata.set('series', $('#conf-series').val());
        formdata.set('address', $('#conf-address').val());
        formdata.set('pages', $('#conf-pages').val());
        send_request(formdata);

    }
    else if (pubType == 'inbook'){
        formdata.set('address', $('#inbook-address').val());
        formdata.set('pages', $('#inbook-pages').val());
        send_request(formdata);

    }
    else if (pubType == 'incollection'){
        formdata.set('editor', $('#incollecion-editor').val());
        formdata.set('address', $('#incollecion-address').val());
        formdata.set('pages', $('#incollecion-pages').val());
        formdata.set('booktitle', $('#incollecion-booktite').val());
        send_request(formdata);

    }
    else if (pubType == 'book'){
        formdata.set('address', $('#book-address').val());
        send_request(formdata);

    }
    else if (['masterthesis', 'phdthesis'].includes(pubType)){
        formdata.set('address', $('#thesis-address').val());
        formdata.set('month', $('#thesis-month').select2('data').text);
        formdata.set('school', $('#thesis-school').val());
        send_request(formdata);

    }
    else{        
        send_request(formdata);
    }
}

function send_request(data){
    let dest_url = $('#dest_url').val();
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == XMLHttpRequest.DONE && req.status === 200) {       
            window.location.replace(this.responseText);                                 
        }
    }
    req.open("POST", dest_url);
    req.send(data);
}