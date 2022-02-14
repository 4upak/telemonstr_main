
    function add_toast(name, title, message, delay){
        var toast_data
        toast_data = '<div id="liveToast" class="toast '+name+' hide" role="alert" aria-live="assertive" aria-atomic="true" data-delay="'+delay+'">'
            toast_data += '<div class="toast-header">'
                toast_data += '<img src="/static/images/notification.svg" width="30" class="rounded mr-2" alt="...">'
                toast_data += '<strong class="mr-auto">'+title+'</strong>'
                toast_data += '<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">'
                    toast_data += '<span aria-hidden="true">&times;</span>'
                toast_data += '</button>'
            toast_data += '</div>'
            toast_data += '<div class="toast-body">'
                toast_data += message
            toast_data += '</div>'
        toast_data += '</div>'
        $('.notifications .toasts_stack').append(toast_data)
        var audio = new Audio('/static/sound/mixkit-sci-fi-reject-notification-896.wav');
        audio.play();
    }
