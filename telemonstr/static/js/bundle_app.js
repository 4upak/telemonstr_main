const app = new Vue({
    el: '#bundle_app',
    data:{
        trading_funnel: [],
        asset: 10,
        comittion_val: 0.00075,
        min_profitability: 0,
    },
    created: function(){



        const vm = this;
        var pk = document.location.href.split('/')[5]



        axios.get('/trading/binancelist/'+pk).then(
            function(response){
                vm.trading_funnel = response.data

                var first_bill = 0
                var second_bill = 0
                var third_bill = 0
                var comittion = vm.comittion_val*asset*3
                var asset = vm.asset

                var audio = new Audio('/static/sound/mixkit-sci-fi-reject-notification-896.wav');

                audio.play();

                vm.trading_funnel.first_pair.amount = 0
                vm.trading_funnel.second_pair.amount = 0
                vm.trading_funnel.third_pair.amount = 0

                vm.trading_funnel.first_pair.time_amount = 0
                vm.trading_funnel.second_pair.time_amount = 0
                vm.trading_funnel.third_pair.time_amount = 0

                vm.trading_funnel.first_pair.flag = 0
                vm.trading_funnel.second_pair.flag = 0
                vm.trading_funnel.third_pair.flag = 0

                vm.trading_funnel.first_pair.socket_flag = 0
                vm.trading_funnel.second_pair.socket_flag = 0
                vm.trading_funnel.third_pair.socket_flag = 0

                vm.trading_funnel.first_pair.socket_connection_time = 0
                vm.trading_funnel.second_pair.socket_connection_time = 0
                vm.trading_funnel.third_pair.socket_connection_time = 0

                vm.trading_funnel.first_pair.socket_connection_duration = 0
                vm.trading_funnel.second_pair.socket_connection_duration = 0
                vm.trading_funnel.third_pair.socket_connection_duration = 0

                vm.trading_funnel.first_pair.position_flag = 0
                vm.trading_funnel.second_pair.position_flag = 0
                vm.trading_funnel.third_pair.position_flag = 0

                vm.trading_funnel.first_pair.position_amount = 0
                vm.trading_funnel.second_pair.position_amount = 0
                vm.trading_funnel.third_pair.position_amount = 0

                vm.trading_funnel.first_pair.orders = []
                vm.trading_funnel.second_pair.orders = []
                vm.trading_funnel.third_pair.orders = []

                vm.trading_funnel.in_position = 0

                vm.trading_funnel.success_list = []
                vm.trading_funnel.success_count = 0
                vm.trading_funnel.success_result = 0
                vm.trading_funnel.success_avg_result = 0
                vm.trading_funnel.total_percent_result = 0


                function pair_set_data(pair, data, step_symbol){
                    data = JSON.parse(event.data)
                    pair.price = data['p']
                    pair.amount += parseFloat(data['q'])


                    if (pair.name == data['s']){
                        pair.price = data["p"]
                        pair.real_price = data["p"]

                        if(step_symbol != pair.base_asset){
                             pair.real_price = 1/data["p"]
                        }
                    }
                    return pair

                }

                function null_flags(){
                    vm.trading_funnel.first_pair.flag = 0
                    vm.trading_funnel.second_pair.flag = 0
                    vm.trading_funnel.third_pair.flag = 0
                }




                let socket_first_step = new ReconnectingWebSocket("wss://stream.binance.com:9443/ws/"+vm.trading_funnel.first_pair.name.toLowerCase()+"@aggTrade");
                let socket_second_step = new ReconnectingWebSocket("wss://stream.binance.com:9443/ws/"+vm.trading_funnel.second_pair.name.toLowerCase()+"@aggTrade");
                let socket_third_step = new ReconnectingWebSocket("wss://stream.binance.com:9443/ws/"+vm.trading_funnel.third_pair.name.toLowerCase()+"@aggTrade");


                socket_first_step.onmessage = function(event) {
                    comittion = vm.comittion_val*asset*3
                    asset = vm.asset

                    pair_set_data(vm.trading_funnel.first_pair, event.data, vm.trading_funnel.first_step_symbol)
                    first_bill = asset/vm.trading_funnel.first_pair.real_price
                    vm.trading_funnel.first_bill = first_bill.toFixed(8)
                    profit_amount = third_bill-asset

                    vm.trading_funnel.profit_amount = profit_amount.toFixed(3)
                    vm.trading_funnel.comittion = comittion
                    vm.trading_funnel.total = vm.trading_funnel.profit_amount - comittion
                    profitability = vm.trading_funnel.total/asset*100
                    vm.trading_funnel.profitability = profitability.toFixed(3)

                    if(profitability>vm.min_profitability && vm.trading_funnel.in_position == 0){
                        console.log("first step bill profitability = " + profitability)
                        vm.trading_funnel.second_pair.position_amount = first_bill - first_bill*vm.comittion_val
                        vm.trading_funnel.second_pair.position_flag = 1
                        vm.trading_funnel.first_pair.orders.push(vm.trading_funnel.second_pair.position_amount)
                        vm.trading_funnel.in_position = 1
                    }
                    if(profitability<0)
                        null_flags()
                };


                //////////////////////////////////////////////




                //////////////////////////////////////////////
                socket_second_step.onmessage = function(event) {
                    comittion = vm.comittion_val*asset*3
                    asset = vm.asset
                    pair_set_data(vm.trading_funnel.second_pair, event.data, vm.trading_funnel.second_step_symbol)

                    second_bill = first_bill/vm.trading_funnel.second_pair.real_price
                    vm.trading_funnel.second_bill = second_bill.toFixed(8)

                    profit_amount = third_bill-asset
                    vm.trading_funnel.profit_amount = profit_amount.toFixed(3)
                    vm.trading_funnel.comittion = comittion
                    vm.trading_funnel.total = vm.trading_funnel.profit_amount - comittion
                    profitability = vm.trading_funnel.total/asset*100
                    vm.trading_funnel.profitability = profitability.toFixed(3)
                    if(vm.trading_funnel.second_pair.position_flag == 1){
                        console.log("second step bill")

                        vm.trading_funnel.third_pair.position_flag = 1
                        vm.trading_funnel.third_pair.position_amount = vm.trading_funnel.second_pair.position_amount/vm.trading_funnel.second_pair.real_price - vm.trading_funnel.second_pair.position_amount/vm.trading_funnel.second_pair.real_price*vm.comittion_val
                        vm.trading_funnel.second_pair.orders.push(vm.trading_funnel.third_pair.position_amount)

                        vm.trading_funnel.second_pair.position_flag = 0
                        vm.trading_funnel.second_pair.position_amount = 0

                    }

                };
                //////////////////////////////////////////////




                //////////////////////////////////////////////

                socket_third_step.onmessage = function(event) {
                    comittion = vm.comittion_val*asset*3
                    asset = vm.asset
                    pair_set_data(vm.trading_funnel.third_pair, event.data, vm.trading_funnel.start_stop_symbol)

                    third_bill = second_bill/vm.trading_funnel.third_pair.real_price
                    vm.trading_funnel.third_bill = third_bill.toFixed(8)

                    profit_amount = third_bill-asset
                    vm.trading_funnel.profit_amount = profit_amount.toFixed(3)
                    vm.trading_funnel.comittion = comittion
                    vm.trading_funnel.total = vm.trading_funnel.profit_amount - comittion
                    profitability = vm.trading_funnel.total/asset*100
                    vm.trading_funnel.profitability = profitability.toFixed(3)
                    if(vm.trading_funnel.third_pair.position_flag == 1){

                        last_bill = vm.trading_funnel.third_pair.position_amount/vm.trading_funnel.third_pair.real_price - vm.trading_funnel.third_pair.position_amount/vm.trading_funnel.third_pair.real_price*vm.comittion_val

                        vm.trading_funnel.third_pair.orders.push(last_bill)
                        vm.trading_funnel.success_list.push((last_bill-asset)/asset*100)
                        setTimeout (5000)
                        vm.trading_funnel.third_pair.position_flag = 0
                        vm.trading_funnel.first_pair.position_amount = 0
                        vm.trading_funnel.in_position = 0

                        vm.trading_funnel.success_count += 1
                        vm.trading_funnel.success_result += last_bill - asset
                        vm.trading_funnel.success_avg_result = vm.trading_funnel.success_result/vm.trading_funnel.success_count
                        vm.trading_funnel.total_percent_result = vm.trading_funnel.success_result/asset


                        audio.play();

                    }
                };


                socket_first_step.onopen = function(e) {
                  console.log('socket started')
                  vm.trading_funnel.first_pair.socket_flag = 1
                  vm.trading_funnel.first_pair.socket_connection_time = Date.now()
                };

                socket_third_step.onopen = function(e) {
                  console.log('socket started')
                  vm.trading_funnel.third_pair.socket_flag = 1
                  vm.trading_funnel.third_pair.socket_connection_time = Date.now()
                };

                socket_second_step.onopen = function(e) {
                  console.log('socket started')
                  vm.trading_funnel.second_pair.socket_flag = 1
                  vm.trading_funnel.second_pair.socket_connection_time = Date.now()

                };




                }).catch(function (error) {
                    console.log(error.toJSON());
                });




    }
})

let timerId = setInterval(function(){

    if(app.trading_funnel.first_pair.socket_flag == 1)
       app.trading_funnel.first_pair.socket_connection_duration = parseInt( (Date.now() - app.trading_funnel.first_pair.socket_connection_time)/1000)
       app.trading_funnel.first_pair.time_amount = app.trading_funnel.first_pair.amount/ app.trading_funnel.first_pair.socket_connection_duration

    if(app.trading_funnel.second_pair.socket_flag == 1)
       app.trading_funnel.second_pair.socket_connection_duration = parseInt( (Date.now() - app.trading_funnel.second_pair.socket_connection_time)/1000)
       app.trading_funnel.second_pair.time_amount = app.trading_funnel.second_pair.amount/ app.trading_funnel.second_pair.socket_connection_duration

    if(app.trading_funnel.third_pair.socket_flag == 1)
       app.trading_funnel.third_pair.socket_connection_duration = parseInt( (Date.now() - app.trading_funnel.third_pair.socket_connection_time)/1000)
       app.trading_funnel.third_pair.time_amount = app.trading_funnel.third_pair.amount/ app.trading_funnel.third_pair.socket_connection_duration

}, 1000);

