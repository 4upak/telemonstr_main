function getCookie() {
    // What do I have to add here to look only in the "obligations=" cookie?
    // Because now it searches all the cookies.

    var elements = document.cookie.split('=');
    var obligations= elements[1].split('%');
    for (var i = 0; i < obligations.length - 1; i++) {
        var tmp = obligations[i].split('$');
        addProduct1(tmp[0], tmp[1], tmp[2], tmp[3]);
    }
 }

function rounded(number){
    return +number.toFixed(2);
}
const app = new Vue({
    el: '#dashboard_app',
    data:{
        curr_data: [],
        fiat: '-',
        crypto: '-',
        bank:'-',
        scrf_tocken:'',

        binance_spread:0,
        binance_spread_comittion:0.2,

        binance_huobi_spread:0,
        binance_huobi_spread_comittion:0.2,

        binance_minfin_spread:0,
        minfin_comittion:3,

        minfin_binance_spread:0,
        minfin_binance_spread_comittion:-2,

        binance_whitebit_spread:0,
        binance_whitebit_spread_comittion:0.2,

        binance_mono_whitebit_spread:0,
        binance_mono_whitebit_spread_comittion:0.7,

        binance_privat_whitebit_spread:0,
        binance_privat_whitebit_spread_comittion:1

    },
    created: function(){
        const vm = this;

        url_data = window.location.pathname.split('/')
        vm.fiat = url_data[3]
        vm.crypto = url_data[4]
        vm.bank = url_data[5]
        axios.get('/p2p/dashboard/api/'+url_data[3]+'/'+url_data[4]+'/'+url_data[5]).then(function(response){
            vm.curr_data = response.data
            vm.binance_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[0][1].optimal.avg_price - vm.curr_data[0][0].optimal.avg_price*vm.binance_spread_comittion/100)
            vm.binance_huobi_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[1][1].optimal.avg_price-vm.curr_data[0][0].optimal.avg_price*vm.binance_huobi_spread_comittion/100)
            vm.binance_minfin_spread = rounded(vm.curr_data[2][0].optimal.avg_price - (vm.curr_data[2][0].optimal.avg_price*vm.minfin_comittion/100) - vm.curr_data[0][1].optimal.avg_price)
            vm.minfin_binance_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[2][1].optimal.avg_price-vm.curr_data[0][0].optimal.avg_price*vm.minfin_binance_spread_comittion/100)
            vm.binance_whitebit_spread = rounded(vm.curr_data[3][1].optimal.avg_price - vm.curr_data[0][0].optimal.avg_price-vm.curr_data[3][1].optimal.avg_price*vm.binance_whitebit_spread_comittion/100)
            vm.binance_mono_whitebit_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[3][1].optimal.avg_price - vm.curr_data[0][0].optimal.avg_price*vm.binance_mono_whitebit_spread_comittion/100)
            vm.binance_privat_whitebit_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[3][1].optimal.avg_price- vm.curr_data[0][0].optimal.avg_price*vm.binance_privat_whitebit_spread_comittion/100)
        })

    },
    watch: {
            minfin_comittion: function (value) {
                vm = this
                vm.binance_minfin_spread = rounded(vm.curr_data[2][0].optimal.avg_price - (vm.curr_data[2][0].optimal.avg_price*vm.minfin_comittion/100) - vm.curr_data[0][1].optimal.avg_price)
            },
            binance_spread_comittion: function (value) {
                vm = this
                vm.binance_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[0][1].optimal.avg_price - vm.curr_data[0][0].optimal.avg_price*vm.binance_spread_comittion/100)
            },
            binance_huobi_spread_comittion: function (value) {
                vm = this
                vm.binance_huobi_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[1][1].optimal.avg_price-vm.curr_data[0][0].optimal.avg_price*vm.binance_huobi_spread_comittion/100)
            },
            binance_whitebit_spread_comittion: function (value) {
                vm = this
                vm.binance_whitebit_spread = rounded(vm.curr_data[3][1].optimal.avg_price - vm.curr_data[0][0].optimal.avg_price-vm.curr_data[3][1].optimal.avg_price*vm.binance_whitebit_spread_comittion/100)
            },
            binance_mono_whitebit_spread_comittion: function (value) {
                vm = this
                vm.binance_mono_whitebit_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[3][1].optimal.avg_price - vm.curr_data[0][0].optimal.avg_price*vm.binance_mono_whitebit_spread_comittion/100)
            },
            binance_privat_whitebit_spread_comittion: function (value) {
                vm = this
                vm.binance_privat_whitebit_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[0][0].optimal.avg_price*vm.binance_privat_whitebit_spread_comittion/100 - vm.curr_data[3][1].optimal.avg_price)
            },
            minfin_binance_spread_comittion: function (value) {
                vm = this
                vm.minfin_binance_spread = rounded(vm.curr_data[0][0].optimal.avg_price - vm.curr_data[2][1].optimal.avg_price-vm.curr_data[0][0].optimal.avg_price*vm.minfin_binance_spread_comittion/100)
            },
    }
})

function send_to_telega(bundle, spread, csrftoken){
    var data = {
        'bundle': bundle,
        'bank':app.bank,
        'spread': spread,
        'xstfCookieName': csrftoken,
        'xsrfHeaderName': csrftoken,
        'csrfmiddlewaretoken':app.scrf_tocken,
    }
    $.ajax({
        url: '/p2p/telegram_send/',
        method: "POST",
        data: data
    })
    .done(function(response){
        if(response['status']=='ok'){
            console.log(response)
        }
        else{
            console.log(response)
        }
    })
    .fail(function(response){
         console.log("Server error")
    })

}

let timerId = setInterval(function(){

    axios.get('/p2p/dashboard/api/'+app.fiat+'/'+app.crypto+'/'+app.bank).then(function(response){

            app.scrf_tocken = document.getElementById('csrf_tocken').value
            app.curr_data = response.data

            app.binance_spread = rounded(app.curr_data[0][0].optimal.avg_price - app.curr_data[0][1].optimal.avg_price - app.curr_data[0][0].optimal.avg_price*app.binance_spread_comittion/100)
            if (app.binance_spread > 0.3)
                send_to_telega('binance usdt -> uah -> binance usdt', app.binance_spread, app.scrf_tocken)

            app.binance_huobi_spread = rounded(app.curr_data[0][0].optimal.avg_price - app.curr_data[1][1].optimal.avg_price-app.curr_data[0][0].optimal.avg_price*app.binance_huobi_spread_comittion/100)
            if (app.binance_huobi_spread > 1)
                send_to_telega('binance usdt -> uah -> Huobi usdt', app.binance_huobi_spread, app.scrf_tocken)

            vm.binance_minfin_spread = rounded(vm.curr_data[2][0].optimal.avg_price - (vm.curr_data[2][0].optimal.avg_price*vm.minfin_comittion/100) - vm.curr_data[0][1].optimal.avg_price)
            if (app.binance_minfin_spread > 0.5)
                send_to_telega('binance usdt -> кеш usdt -> кеш uah -> binance usdt', app.binance_minfin_spread, app.scrf_tocken)

            app.minfin_binance_spread = rounded(app.curr_data[0][0].optimal.avg_price - app.curr_data[2][1].optimal.avg_price-app.curr_data[0][0].optimal.avg_price*app.minfin_binance_spread_comittion/100)
            if (app.minfin_binance_spread > 0.5)
                send_to_telega('binance usdt -> кеш uah -> кеш usdt -> binance usdt', app.minfin_binance_spread, app.scrf_tocken)

            app.binance_whitebit_spread = rounded(app.curr_data[3][1].optimal.avg_price - app.curr_data[0][0].optimal.avg_price - app.curr_data[3][1].optimal.avg_price*app.binance_whitebit_spread_comittion/100)
            if (app.binance_whitebit_spread > 0.3)
                send_to_telega('whitebit usdt -> whitebit uah -> binance usdt', app.binance_whitebit_spread, app.scrf_tocken)

            app.binance_mono_whitebit_spread = rounded(app.curr_data[0][0].optimal.avg_price - app.curr_data[3][1].optimal.avg_price - app.curr_data[0][0].optimal.avg_price*app.binance_mono_whitebit_spread_comittion/100)
            if (app.binance_mono_whitebit_spread > 0.5)
                send_to_telega('binance usdt -> mono uah -> whitebit usdt', app.binance_mono_whitebit_spread, app.scrf_tocken)

            app.binance_privat_whitebit_spread = rounded(app.curr_data[0][0].optimal.avg_price - app.curr_data[0][0].optimal.avg_price*app.binance_privat_whitebit_spread_comittion/100 - app.curr_data[3][1].optimal.avg_price)
            if (app.binance_privat_whitebit_spread > 0.5)
                send_to_telega('binance usdt -> privat uah -> whitebit usdt', app.binance_privat_whitebit_spread, app.scrf_tocken)

        })
    console.log("Data updated")


}, 60000);
