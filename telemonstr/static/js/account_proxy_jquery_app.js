function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

jQuery( document ).ready(function( $ ) {
    function add_next_tr(current_index){
        var next_tr_index = parseInt(current_index)+1
        $('#proxy_tr'+current_index).after('<tr class="proxy_tr" id="proxy_tr'+next_tr_index+'"><td><div class="form-check"><input class="form-check-input" type="checkbox" id="check_account" name="check_account"></div></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="type" placeholder="Type"></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="host" placeholder="host"></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="port" placeholder="Port"></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="login" placeholder="Login"></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="pass" placeholder="Pass"></td><td scope="col"><img src="/static/images/plus.svg" width="20" class="add_proxy_icon"></td></td>')
        $('#proxy_tr'+current_index+' .form-check-input').attr("checked","checked")
        $('#proxy_tr'+current_index+' .add_proxy_icon').toggle(100)
    }
    //Add proxy row
    $(document).on("click", '.add_proxy_icon', function(){
        var last_tr_id = $( this ).parent().parent().attr('id')
        var last_tr_index = parseInt(last_tr_id.replace("proxy_tr",""))
        console.log(last_tr_id)
        var next_tr_index = last_tr_index+1
        $('#'+last_tr_id).after('<tr class="proxy_tr" id="proxy_tr'+next_tr_index+'"><td><div class="form-check"><input class="form-check-input" type="checkbox" id="check_account" name="check_account" checked></div></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="type" placeholder="Type"></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="host" placeholder="host"></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="port" placeholder="Port"></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="login" placeholder="Login"></td><td scope="col"><input type="text" class="form-control" id="exampleFormControlInput1" name="pass" placeholder="Pass"></td><td scope="col"><img src="/static/images/plus.svg" width="20" class="add_proxy_icon"></td></td>')
        $(this).toggle(100)
    })
    //read proxy lines from textarea
     $(document).on("click", '#read_proxy_lines', function(){
         console.log('Клик работает, заходим в цикл')
         var lines = $('.proxy_text_data').val().split('\n')
         console.log(lines.length + 'Строк в тексте')
         for(var i = 0; i < lines.length; i++){
            var proxy_data = lines[i].split(':')
            add_next_tr(i)
            $('#proxy_tr'+i+' td input[name="type"]').val(proxy_data[0])
            $('#proxy_tr'+i+' input[name="host"]').val(proxy_data[1])
            $('#proxy_tr'+i+' input[name=port]').val(proxy_data[2])
            $('#proxy_tr'+i+' input[name=login]').val(proxy_data[3])
            $('#proxy_tr'+i+' input[name=pass]').val(proxy_data[4])

         }
     })

    $(document).on("click", '.save_proxy button', function(){
        console.log("Button clicked")
        var rows = $('.proxy_tr')
        console.log(rows.length + "proxy rows finded")
        for(var i = 0; i < rows.length-1; i++){
            var data = {
                'type': $('#proxy_tr' + i + ' input[name=type]').val(),
                'host': $('#proxy_tr' + i + ' input[name=host]').val(),
                'port': $('#proxy_tr' + i + ' input[name=port]').val(),
                'login': $('#proxy_tr' + i + ' input[name=login]').val(),
                'pass': $('#proxy_tr' + i + ' input[name=pass]').val(),
                'index': i,
                'csrfmiddlewaretoken': $('input[name=csrf]').val(),
            }
            console.log(data)
            $.ajax({
                url: '/accounts/proxy/add/',
                method: "POST",
                data: data
            })
            .done(function(response){
                if(response['status']=='ok'){
                    console.log(response)
                    $('#proxy_tr' + response['index'] + ' .add_proxy_icon').html('<img width="20" src = "/static/images/done.svg" >')
                    $('#proxy_tr' + response['index']).toggle(2000)
                }
                else{
                    $('#proxy_tr' + response['index'] + ' td:eq(6)').html('<img width="20" src = "/static/images/error.svg" title="'+response['error_message']+'">')
                    console.log(response)

                    add_toast('add_proxy_error_'+response['index'], 'Add proxy error', response['error_message'], 2000)
                    $('.add_proxy_error_'+response['index']).toast('show')
                }
            })
            .fail(function(response){
                 console.log("Server error")
            })
        }
    })

    $(document).on("click", '.check_proxy_icon img', function(){
        var current_row = $(this).parent().parent().parent()
        var index = $('#active_proxy_app tr.active_proxy_row').index(current_row)
        console.log(index)

        var proxy_id = $(this).parent().parent().children('.proxy_id').text()
        $(this).replaceWith('<div class="spinner-grow text-secondary" role="status"><span class="sr-only">Loading...</span></div>')

        data = {
            'id':proxy_id,
            'index':index,
            'csrfmiddlewaretoken': $('input[name=csrf]').val()

        }
        $.ajax({
            url: '/accounts/proxy/check/',
            method: "POST",
            data: data
        })
        .done(function(response){
            if(response['status']=='ok'){
                console.log(response)
                if(response['result'] == true){
                    $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+') .check_proxy_icon').html('<img src="/static/images/toggle-on.svg" width="50">')
                    $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+')').css('background-color', '#d4edda')
                    $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+')').css('border-color', '#f5c6cb')
                    var checked_proxy_host =  $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+') td:eq(2)').text()
                    add_toast('check_proxy_'+index, 'Proxy checked', 'Proxy ' +checked_proxy_host + ' checked succesfully and it is active now', 2000)
                    $('.check_proxy_'+index).toast('show')
                }
                else{
                    $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+') .check_proxy_icon').html('<img src="/static/images/toggle-off.svg" width="50">')
                    $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+')').css('background-color', '#f8d7da')
                    $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+')').css('border-color', '#f5c6cb')
                    var checked_proxy_host =  $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+') td:eq(2)').text()
                    add_toast('check_proxy_'+index, 'Proxy checked', 'Proxy ' + checked_proxy_host+ ' is not active now', 2000)
                    $('.check_proxy_'+index).toast('show')
                }
            }

            else{
                console.log(response)
                add_toast('check_proxy_error_'+index, 'Proxy checking error', 'Proxy with index ' +response['error_message'] + ' checked succesfully', 2000)
                $('.check_proxy_error_'+index).toast('show')
            }
        })
        .fail(function(response){
            console.log("Server error")
        })
    })

    $(document).on("click", '.check_all', function(){
        var active_proxy_qty = $('#active_proxy_app .active_proxy_row').length
        console.log( active_proxy_qty )

        for (i = 0; i < parseInt(active_proxy_qty); i++) {
            if( $('#active_proxy_app .form-check-input:eq('+i+')').is(':checked') ){
                $('#active_proxy_app .form-check-input:eq('+i+')').removeAttr("checked")
            }
            else{
                $('#active_proxy_app .form-check-input:eq('+i+')').attr("checked","checked")
            }
        }
    })

    $(document).on("click", '.delete_proxy_icon img', function(){
        var current_row = $(this).parent().parent().parent()
        var index = $('#active_proxy_app tr.active_proxy_row').index(current_row)
        console.log(index)

        var proxy_id = $(this).parent().parent().children('.proxy_id').text()
        $(this).replaceWith('<div class="spinner-grow text-secondary" role="status"><span class="sr-only">Loading...</span></div>')
        data = {
            'id':proxy_id,
            'index':index,
            'csrfmiddlewaretoken': $('input[name=csrf]').val()

        }
        $.ajax({
            url: '/accounts/proxy/delete/',
            method: "POST",
            data: data
        })
        .done(function(response){
            if(response['status']=='ok'){
                console.log(response)

                $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+') .check_proxy_icon').html('<img src="/static/images/toggle-on.svg" width="50">')


                add_toast('check_proxy_'+index, 'Proxy checked', 'Proxy with index ' +response['index'] + ' deleted succesfully', 2000)
                $('.check_proxy_'+index).toast('show')
                $('#active_proxy_app tr.active_proxy_row:eq('+response['index']+')').toggle(500)

            }
            else{
                console.log(response)
            }
        })
        .fail(function(response){
            console.log("Server error")
        })

    })

    $(document).on("click", '.action_do_it button', function(){
        if(parseInt( $('.action_do_it select#select_proxy_action option:selected').attr('value') ) == 1){
            console.log('checking proxy')
            var rows = $('.active_proxy_row')
            console.log(rows.length + "proxy rows finded")
            var checked_count = 0
            for (i = 0; i < rows.length; i++) {
                if($('.active_proxy_row:eq('+i+') #check_active_proxy').is(":checked")){
                    checked_count+=1
                }

            }
            if(checked_count>0){
                for (i = 0; i < rows.length; i++) {
                    if($('.active_proxy_row:eq('+i+') #check_active_proxy').is(":checked"))
                        $('.active_proxy_row:eq('+i+') .check_proxy_icon img').trigger('click')
                }
            }
            else{
                add_toast('proxy_list_to_check', 'Checked proxy list is empty', 'You need to check some proxy to start checking', 2000)
                $('.proxy_list_to_check').toast('show')
            }
        }

        if(parseInt( $('.action_do_it select#select_proxy_action option:selected').attr('value') ) == 2){
            console.log('deleting proxy')
            var rows = $('.active_proxy_row')
            console.log(rows.length + "proxy rows finded")
            var checked_count = 0
            for (i = 0; i < rows.length; i++) {

                if($('.active_proxy_row:eq('+i+') #check_active_proxy').is(":checked")){
                    console.log(i+' index is selected')
                    checked_count+=1
                }

            }
            console.log(checked_count + "proxy checked")
            if(checked_count>0){
                for (i = 0; i < rows.length; i++) {
                    if($('.active_proxy_row:eq('+i+') #check_active_proxy').is(":checked"))
                        $('.active_proxy_row:eq('+i+') .delete_proxy_icon img').trigger('click')
                }
            }
            else{
                add_toast('proxy_list_to_check', 'Deleteing proxy list is empty', 'You need to check some proxy to delete', 2000)
                $('.proxy_list_to_check').toast('show')
            }
        }

    })




})