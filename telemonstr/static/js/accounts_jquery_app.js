function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

jQuery( document ).ready(function( $ ) {

    //check_all accounts for import
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

     //check_all active accounts
    $(document).on("click", '.check_all', function(){
        var index = $('#active_accounts_app #check_active_account').index(this)
        var session_file = $('#active_accounts_app .active_account_row:eq('+index+') td:eq(1)').text()
        var import_accounts_qty = $('#active_accounts_app .active_account_row').length
        console.log( import_accounts_qty )

        for (i = 0; i < parseInt(import_accounts_qty); i++) {
            if( $('#active_accounts_app .form-check-input:eq('+i+')').is(':checked') ){
                $('#active_accounts_app .form-check-input:eq('+i+')').removeAttr("checked")
            }
            else{
                $('#active_accounts_app .form-check-input:eq('+i+')').attr("checked","checked")
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
    //deleting active account
    $(document).on("click", '#active_accounts_app .delete_account_icon', function(){
        var account_id = $(this).parent().children('.account_id').text()
        var index = $(this).parent().parent().index('#active_accounts_app .active_account_row')
        console.log(index)

        data = {
            'index':index,
            'account_id':account_id,
            'csrfmiddlewaretoken': $('input[name=csrf]').val()
        }

        $.ajax({
            url: '/accounts/delete/',
            method: "POST",
            data: data
        })
        .done(function(response){
            if(response['status']=='ok'){
                console.log(response)
                $('#active_accounts_app .active_account_row:eq('+response['index']+')').toggle(300)
                add_toast('account_delete_'+index, 'Account deleted', 'account with index ' +response['index'] + ' deleted succesfully', 2000)
                $('.account_delete_'+index).toast('show')
            }
            else{
                console.log(response)
                add_toast('account_delete_error_'+index, 'Account deleting error', 'account with index ' +response['error_message'] + ' deleting error', 2000)
                $('.account_delete_error_'+index).toast('show')
            }
        })
        .fail(function(response){
            console.log("Server error")
        })

    })




});