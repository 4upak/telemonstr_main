new Vue({
    el: '#active_proxy_app',
    data:{
        active_proxy_list: []
    },
    created: function(){
        const vm = this;
        axios.get('/accounts/proxy/list/').then(function(response){
            vm.active_proxy_list = response.data
            console.log(response.data)
        })
    }
})