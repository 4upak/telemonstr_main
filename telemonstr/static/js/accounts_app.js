new Vue({
    el: '#accounts_app',
    data:{
        accounts: []
    },
    created: function(){
        const vm = this;
        axios.get('/accounts/api/import_accounts').then(function(response){
            vm.accounts = response.data
        })
    }
})

new Vue({
    el: '#active_accounts_app',
    data:{
        active_accounts: []
    },
    created: function(){
        const vm = this;
        axios.get('/accounts/api/active_accounts').then(function(response){
            vm.active_accounts = response.data
        })
    }
})


