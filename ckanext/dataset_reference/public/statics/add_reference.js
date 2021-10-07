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
   
});