const app = new Vue({
    el: '#bundle_app',
    data:{
        trading_funnel: []
    },
    created: function(){
        const vm = this;
        var pk = document.location.href.split('/')[5]

        axios.get('/trading/binancelist/'+pk).then(
            function(response){
                vm.trading_funnel = response.data
                var asset = 10
                var first_bill = 0
                var second_bill = 0
                var third_bill = 0
                var comittion = 0.00075*asset*3
                var audio = new Audio('/static/sound/mixkit-sci-fi-reject-notification-896.wav');
                audio.play();

                vm.trading_funnel.first_pair.amount = 0
                vm.trading_funnel.second_pair.amount = 0
                vm.trading_funnel.third_pair.amount = 0


                let socket_first_step = new ReconnectingWebSocket("wss://stream.binance.com:9443/ws/"+vm.trading_funnel.first_pair.name.toLowerCase()+"@aggTrade");
                let socket_second_step = new ReconnectingWebSocket("wss://stream.binance.com:9443/ws/"+vm.trading_funnel.second_pair.name.toLowerCase()+"@aggTrade");
                let socket_third_step = new ReconnectingWebSocket("wss://stream.binance.com:9443/ws/"+vm.trading_funnel.third_pair.name.toLowerCase()+"@aggTrade");

                socket_first_step.onopen = function(e) {
                  console.log('socket started')

                };
                socket_first_step.onmessage = function(event) {
                    data = JSON.parse(event.data)
                    console.log(data)
                    vm.trading_funnel.first_pair.price = data['p']
                    vm.trading_funnel.first_pair.amount += parseFloat(data['q'])

                    if (vm.trading_funnel.first_pair.name == data['s']){
                        vm.trading_funnel.first_pair.price = data["p"]
                        vm.trading_funnel.first_pair.real_price = data["p"]

                        if(vm.trading_funnel.first_step_symbol != vm.trading_funnel.first_pair.base_asset){
                             vm.trading_funnel.first_pair.real_price = 1/data["p"]
                        }
                    }

                    first_bill = asset/vm.trading_funnel.first_pair.real_price
                    vm.trading_funnel.first_bill = first_bill.toFixed(8)

                    profit_amount = third_bill-asset
                    vm.trading_funnel.profit_amount = profit_amount.toFixed(3)
                    vm.trading_funnel.comittion = comittion
                    vm.trading_funnel.total = vm.trading_funnel.profit_amount - comittion
                    profitability = vm.trading_funnel.total/asset*100
                    vm.trading_funnel.profitability = profitability.toFixed(3)
                    if (profitability>0){

                        audio.play();
                    }

                };


                //////////////////////////////////////////////




                //////////////////////////////////////////////
                socket_second_step.onopen = function(e) {
                  console.log('socket started')

                };
                socket_second_step.onmessage = function(event) {
                    data = JSON.parse(event.data)
                    vm.trading_funnel.second_pair.price = data['p']
                    vm.trading_funnel.second_pair.amount += parseFloat(data['q'])
                    if (vm.trading_funnel.second_pair.name == data['s']){
                        vm.trading_funnel.second_pair.price = data["p"]
                        vm.trading_funnel.second_pair.real_price = data["p"]

                        if(vm.trading_funnel.second_step_symbol != vm.trading_funnel.second_pair.base_asset){
                             vm.trading_funnel.second_pair.real_price = 1/data["p"]
                        }
                    }

                    second_bill = first_bill/vm.trading_funnel.second_pair.real_price
                    vm.trading_funnel.second_bill = second_bill.toFixed(8)

                    profit_amount = third_bill-asset
                    vm.trading_funnel.profit_amount = profit_amount.toFixed(3)
                    vm.trading_funnel.comittion = comittion
                    vm.trading_funnel.total = vm.trading_funnel.profit_amount - comittion
                    profitability = vm.trading_funnel.total/asset*100
                    vm.trading_funnel.profitability = profitability.toFixed(3)
                };
                //////////////////////////////////////////////
                socket_third_step.onopen = function(e) {
                  console.log('socket started')

                };
                socket_third_step.onmessage = function(event) {
                    data = JSON.parse(event.data)
                    vm.trading_funnel.third_pair.price = data['p']
                    vm.trading_funnel.third_pair.amount += parseFloat(data['q'])

                    if (vm.trading_funnel.third_pair.name == data['s']){
                        vm.trading_funnel.third_pair.price = data["p"]
                        vm.trading_funnel.third_pair.real_price = data["p"]

                        if(vm.trading_funnel.start_stop_symbol != vm.trading_funnel.third_pair.base_asset){
                             vm.trading_funnel.third_pair.real_price = 1/data["p"]
                        }
                    }
                    third_bill = second_bill/vm.trading_funnel.third_pair.real_price
                    vm.trading_funnel.third_bill = third_bill.toFixed(8)

                    profit_amount = third_bill-asset
                    vm.trading_funnel.profit_amount = profit_amount.toFixed(3)
                    vm.trading_funnel.comittion = comittion
                    vm.trading_funnel.total = vm.trading_funnel.profit_amount - comittion
                    profitability = vm.trading_funnel.total/asset*100
                    vm.trading_funnel.profitability = profitability.toFixed(3)
                };


                }).catch(function (error) {
                    console.log(error.toJSON());
                });




    }
})