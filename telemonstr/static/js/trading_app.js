new Vue({
    el: '#trading_funnels_app',
    data:{
        trading_funnels: []
    },
    created: function(){
        const vm = this;
        axios.get('/trading/binancelist/?format=json').then(
            function(response){
                vm.trading_funnels = response.data
                console.log(response.data)
        }).catch(function (error) {
            console.log(error.toJSON());
        });

        let socket = new ReconnectingWebSocket("ws://46.219.111.133:8000/ws/streaming/all/");


        socket.onopen = function(e) {
          console.log('socket started')

        };

        socket.onmessage = function(event) {
          console.log(event.data)
          data = JSON.parse(event.data)
          price_data = JSON.parse(data['value'].replace(/'/g, '"'))
          console.log(price_data)

           for (let i = 0; i < vm.trading_funnels.length; i++) {
              if (parseInt(vm.trading_funnels[i]["first_pair"]["id"]) == price_data["pk"]){
                vm.trading_funnels[i]["first_pair"]["price"] = price_data["price"]
                vm.trading_funnels[i]["first_pair"]["real_price"] = price_data["price"]

                if(vm.trading_funnels[i]['first_step_symbol'] != vm.trading_funnels[i]["first_pair"]["base_asset"]){
                     vm.trading_funnels[i]["first_pair"]["real_price"] = 1/price_data["price"]
                }
              }

              if (parseInt(vm.trading_funnels[i]["second_pair"]["id"]) == price_data["pk"]){
                  vm.trading_funnels[i]["second_pair"]["price"] = price_data["price"]
                  vm.trading_funnels[i]["second_pair"]["real_price"] = price_data["price"]

                  if(vm.trading_funnels[i]["second_step_symbol"] != vm.trading_funnels[i]["second_pair"]["base_asset"]){
                        vm.trading_funnels[i]["second_pair"]["real_price"] = 1/price_data["price"]
                    }

              }

              if (parseInt(vm.trading_funnels[i]["third_pair"]["id"]) == price_data["pk"]){
                  vm.trading_funnels[i]["third_pair"]["price"] = price_data["price"]
                  vm.trading_funnels[i]["third_pair"]["real_price"] = price_data["price"]
                  if(vm.trading_funnels[i]["start_stop_symbol"] != vm.trading_funnels[i]["third_pair"]["base_asset"]){
                        vm.trading_funnels[i]["third_pair"]["real_price"] = 1/price_data["price"]
                  }
              }

              asset = 10
              first_bill = asset/vm.trading_funnels[i]['first_pair']['real_price']
              vm.trading_funnels[i]['first_bill'] = first_bill.toFixed(5)
              second_bill = first_bill/vm.trading_funnels[i]["second_pair"]["real_price"]
              vm.trading_funnels[i]['second_bill'] = second_bill.toFixed(5)

              third_bill = second_bill/vm.trading_funnels[i]["third_pair"]["real_price"]
              vm.trading_funnels[i]['third_bill'] = third_bill.toFixed(5)

              comittion = 0.00075*asset*3
              price = (third_bill-asset)/asset*100 - comittion

              profit_amount = third_bill-asset
              vm.trading_funnels[i]['profit_amount'] = profit_amount.toFixed(3)
              vm.trading_funnels[i]['comittion'] = comittion
              vm.trading_funnels[i]['total'] = vm.trading_funnels[i]['profit_amount'] - comittion
              profitability = vm.trading_funnels[i]['total']/asset*100
              vm.trading_funnels[i]['profitability'] = profitability.toFixed(3)

           }

        };

        socket.onclose = function(event) {
          if (event.wasClean) {
            console.log('[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}')
          } else {
            console.log('[close] Соединение прервано')
            socket = new WebSocket("ws://46.219.111.133:8000/ws/streaming/all/");
          }
        };

        socket.onerror = function(error) {
          console.log('[error] ${error.message}')
        };


    },
     methods: {
        open_tab: function (event, id) {
            window.open('/trading/bundle/'+id, '_blank').focus();
        }


     }


})