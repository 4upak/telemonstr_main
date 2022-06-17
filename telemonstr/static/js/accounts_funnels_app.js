bootstrapValidate(['#funnel_name'], 'required: Enter funnel name');


/*
jQuery( document ).ready(function( $ ) {
    console.log('funnels javascript works')

    $( ".create_funnel_name_form" ).submit(function( event ) {
        event.preventDefault()
        data = {
            'funnel_name':$('input#funnel_name').val(),
            'csrfmiddlewaretoken': $('input[name=csrf]').val()
        }

        $.ajax({
            url: '/funnels/add/',
            method: "POST",
            data: data
        })
        .done(function(response){
            if(response['status']=='ok'){
                console.log(response['status'])


                $('#funnel_units_form .bd-content-title').text($('input#funnel_name').val())




                add_toast('funnel_add', 'Funnel added', 'Funnel created succesfully', 3000)
                $('.funnel_add').toast('show')
                console.log('reloading list')

                axios.get('list/').then(function(response){
                    vue_funnel_list.active_funnels_list = response.data
                })

            }
            else{
                console.log(response)
                add_toast('funnel_add', 'Funnel vration faled', response['error_message'], 3000)
                $('.funnel_add').toast('show')
                $('input#funnel_name').addClass('is-invalid')
                $('.create_funnel_name_form .form-group').append('<div class="invalid-feedback has-error-required" style="display: inline-block;">'+response['error_message']+'</div>')
            }

        })
        .fail(function(response){
            console.log("Server error")
            add_toast('funnel_add', 'Funnel vration faled', 'server error', 3000)
            $('.funnel_add').toast('show')
        })
    })
    $(document).on("click", '#funnel_units_form button', function(){
        console.log('create funnel unit click')

    })

    $(document).on("click", '.delete_funnel_icon', function(){
        console.log('delete funnel click')
        var index = $(this).parent().parent().index('#active_funnels_app .active_funnel_row')
        data = {
            'index': index,
            'funnel_id':$(this).parent().children('.funnel_id').text(),
            'csrfmiddlewaretoken': $('input[name=csrf]').val()
        }

        $.ajax({
            url: '/funnels/delete/',
            method: "POST",
            data: data
        })
        .done(function(response){
            if(response['status']=='ok'){
                console.log(response)

                add_toast('funnel_delete', 'Funnel deleted', 'Funnel deleted succesfully', 3000)
                $('.funnel_delete').toast('show')
                $('.active_funnel_row:eq(' + index + ')').toggle(300)

            }
            else{
                console.log(response)
                add_toast('funnel_add', 'Funnel vration faled', response['error_message'], 3000)
                $('.funnel_delete').toast('show')
            }
            console.log('funnel deleted')

        })
        .fail(function(response){
            console.log("Server error")
            add_toast('funnel_delete', 'Funnel deleting faled', 'server error', 3000)
            $('.funnel_delete').toast('show')
        })


    })





})*/