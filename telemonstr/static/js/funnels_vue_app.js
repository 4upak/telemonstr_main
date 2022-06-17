var vue_funnel_list = new Vue({
    el: '#active_funnels_app',
    data:{
        active_funnels_list: [],
        new_funnel_name: ""

    },
    created: function(){
        var vm = this;
        axios.get('/funnels/list/?format=json').then(
            function(response){
                vm.active_funnels_list = response.data
                console.log(response.data)
        }).catch(function (error) {
            console.log(error.toJSON());
        });
        var csrf = document.querySelector('input[name="csrf"]').getAttribute('value')
        axios.defaults.xsrfHeaderName = "X-CSRFToken";
        axios.defaults.xsrfCookieName = csrf;
    },
    methods: {
        funnel_edit: function (pk,scrf) {
            var csrf = document.querySelector('input[name="csrf"]').getAttribute('value')

            data = {
                pk: pk,
                funnel_name: 'edited'
            }

            axios({
                method:'put',
                url:' api/funnels_detail/'+pk,
                data:data,
                headers:{
                    'X-CSRFTOKEN': csrf,
                }
            }).then(response=>{
                console.log('then')

            }).catch(err=>{
                console.log(err)
            })
        },

        funnel_delete: function (pk) {
          // `this` inside methods point to the Vue instance
          alert(pk)
          // `event` is the native DOM event
        },


        funnel_add: function (new_funnel_name){
            data = {

                funnel_name: this.new_funnel_name
            }
            var csrf = document.querySelector('input[name="csrf"]').getAttribute('value')
            axios({
                method:'post',
                url:' /funnels/list/',
                data:data,
                headers:{
                    'X-CSRFTOKEN': csrf,
                }
            }).then(response=>{
                this.active_funnels_list.push(response.data)
                console.log(response.data)


            }).catch(err=>{
                console.log(err)
            })
        }


    },
})