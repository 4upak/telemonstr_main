new Vue({
    el: '#trading_funnels_app',
    data:{
        trading_funnels: []
    },
    created: function(){
        const vm = this;

        vm.trading_funnels = []
        url = window.location.href
        var symbol = url.split('/')[5]
        /*
        let socket = new WebSocket("ws://46.219.111.133:8000/ws/trading/"+symbol+"/");


        socket.onopen = function(e) {
          console.log('socket started')
        };

        socket.onmessage = function(event) {
          console.log(event.data)

          var data_list = JSON.parse(event.data)
          console.log(data_list)
          var data_list_clear = JSON.parse(data_list)
          console.log(data_list_clear)

          if(data_list_clear.action == 'new_funnel'){
            vm.trading_funnels.unshift(data_list_clear)
          }
          console.log(vm.trading_funnels)

        };

        socket.onclose = function(event) {
          if (event.wasClean) {
            console.log('[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}')
          } else {
            console.log('[close] Соединение прервано')
          }
        };

        socket.onerror = function(error) {
          console.log('[error] ${error.message}')
        };*/

        axios.get('/trading/binancelist/?format=json').then(
            function(response){
                vm.trading_funnels = response.data
                console.log(response.data)
        }).catch(function (error) {
            console.log(error.toJSON());
        });
        /*
        setInterval(
          () => {
            console.log('reload')
            axios.get('/trading/binancelist/?format=json').then(
            function(response){
                vm.trading_funnels = response.data
                console.log(response.data)
            }).catch(function (error) {
                console.log(error.toJSON());
            });
          },
          5000
        );*/

    }
})