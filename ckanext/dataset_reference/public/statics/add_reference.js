$(document).ready(function(){        
    $('#doi_submit_btn').click(function(e){        
        let doi_input = $('#doi').val();
        $.ajax({
            url: $('#doi-validity-url').val(),
            cache:false,   
            data: {'doi_url': doi_input},            
            type: "POST",
            success: function(result){
                if(result != '1'){                               
                    $('#doi_validation_message').text(result);           
                }
                else{
                    $('#doi-form').submit();
                }                        
            }
        }); 
    });

    $('#doi').focusin(function(){
        $('#doi').css("background-color", 'white');
        $('#doi').addClass('link-enabled');
        $('#bibtex').removeClass('link-enabled');
        $('#bibtex').css("background-color", '#EBEBEB');
    });


    $('#bibtex').focusin(function(){
        $('#bibtex').css("background-color", 'white');
        $('#bibtex').addClass('link-enabled');
        $('#doi').css("background-color", '#EBEBEB');
        $('#doi').removeClass('link-enabled');
    });

    
   
});