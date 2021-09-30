$(document).ready(function(){
    $("#pub-type").select2();
    $('#years-select').select2();
    $('select.month-select').select2();
    $("#thesis-type").select2();

    $('#pub-type').change(function(){
        let pubType = $(this).select2('data').text;
        if (pubType == 'Journal Paper'){
            $('.pub-type-section').hide();
            $('#article-section').fadeIn();
        }
        else if (pubType == 'Report'){
            $('.pub-type-section').hide();
            $('#section-tech-report').fadeIn();
        }
        else if (pubType === 'Conference Paper'){
            $('.pub-type-section').hide();
            $('#conference-section').fadeIn();
        }
        else if (pubType == 'Book'){
            $('.pub-type-section').hide();
            $('#book-section').fadeIn();
        }
        else if (pubType === 'Thesis'){
            $('.pub-type-section').hide();
            $('#thesis-section').fadeIn();
        }
        else if (pubType === 'Electronic Source'){
            $('.pub-type-section').hide();
            $('#section-electronic-source').fadeIn();
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
    formdata.set('url', $('#ref-url').val());
   
    if (pubType == 'Journal Paper'){
        formdata.set('journal', $('#article-journal').val());
        formdata.set('volume', $('#article-volume').val());
        formdata.set('page', $('#article-pages').val());
        formdata.set('issue', $('#article-issue').select2('data').text);
        send_request(formdata);

    }
    else if (pubType == 'Report'){
        formdata.set('publisher', $('#report-publisher').val());
        formdata.set('org', $('#report-ins').val());
        formdata.set('address', $('#report-address').val());
        send_request(formdata);

    }
    else if (pubType === 'Conference Paper'){
        formdata.set('proceeding', $('#conf-proceeding').val());
        formdata.set('proceeding_date', $('#conf-proceeding-date').val());
        formdata.set('publisher', $('#conf-publisher').val());
        formdata.set('address', $('#conf-pub-address').val());
        formdata.set('pages', $('#conf-pages').val());
        send_request(formdata);

    }
    else if (pubType == 'Book'){
        formdata.set('address', $('#book-address').val());
        formdata.set('publisher', $('#book-publisher').val());
        send_request(formdata);

    }
    else if (pubType == 'Thesis'){
        formdata.set('thesis-type', $('#thesis-type').select2('data').text);
        formdata.set('school', $('#thesis-school').val());
        send_request(formdata);

    }
    else if (pubType == 'Electronic Source'){
        formdata.set('access', $('#e-accessDate').val());
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