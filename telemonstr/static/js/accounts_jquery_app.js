function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

jQuery( document ).ready(function( $ ) {

    //check_all action
    $(document).on("click", '.check_all', function(){
        var index = $('#accounts_app #check_account').index(this)
        var session_file = $('#accounts_app .account_row:eq('+index+') td:eq(1)').text()
        var import_accounts_qty = $('#accounts_app .account_row').length
        console.log( import_accounts_qty )

        for (i = 0; i < parseInt(import_accounts_qty); i++) {
            if( $('#accounts_app .form-check-input:eq('+i+')').is(':checked') ){
                $('#accounts_app .form-check-input:eq('+i+')').removeAttr("checked")
            }
            else{
                $('#accounts_app .form-check-input:eq('+i+')').attr("checked","checked")
            }
        }
    })

    //import action
    $(document).on("click", '.action_do_it button', function(){
        if(parseInt( $('select#select_account_action option:selected').attr('value') ) == 1){
            var boxes = $('input[name=check_account]:checked')
            console.log('lenght: '+boxes.length)
            if(boxes.length == 0){
                console.log('nothing to import')
            }
            else{

                boxes.each(function (){
                    var checked_index = $('#accounts_app #check_account').index(this)
                    var checked_session_file = $('#accounts_app .account_row:eq('+checked_index+') td:eq(1)').text()
                    var data = {
                        'session':checked_session_file,
                        'index':checked_index,
                        'csrfmiddlewaretoken': $('input[name=csrf]').val()

                    }
                    $.ajax({
                        url: '/accounts/import/',
                        method: "POST",
                        data: data
                    })
                    .done(function(response){
                        if(response['status']=='ok'){
                            console.log(response['status'])
                            $('#accounts_app .account_row:eq('+response['index']+') td:eq(6)').html('<img width=20 src = "/static/images/done.svg" >')
                            $('#accounts_app .account_row:eq('+response['index']+')').toggle(3000)
                        }
                        else{
                            console.log(response['error_message'])
                            $('#accounts_app .account_row:eq('+response['index']+') td:eq(6)').html('<img width=20 src = "/static/images/error.svg" title="'+response['error_message']+'">')
                        }

                    })
                    .fail(function(response){
                        alert("Server is down")
                    })

                })
            }
        }
    })



});