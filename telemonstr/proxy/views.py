from django.shortcuts import render

from accounts.models import *

from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import Telegram_account
from django.http import JsonResponse
from proxy.models import Proxy
from funnels.models import Funnel
from django.core import serializers

# Create your views here.
def proxy_page(request):

    active_account_qty = Telegram_account.objects.count()
    active_proxy_qty = Proxy.objects.count()
    active_funnels_qty = Funnel.objects.count()
    data = {
        'title': "Аккаунты заголовок",
        'active_account_qty': active_account_qty,
        'active_proxy_qty': active_proxy_qty,
        'active_funnels_qty': active_funnels_qty
    }

    return render(request, 'proxy.html',data)

def proxy_add(request):
    if request.method == 'POST':
        try:
            proxy = Proxy(
                type = request.POST['type'],
                host = request.POST['host'],
                port = int(request.POST['port']),
                login = request.POST['login'],
                password = request.POST['pass']
            )
            proxy.save()
            return JsonResponse({'status': 'ok', 'error_message': "Proxy created!", 'index': request.POST['index']})
        except Exception as ex:
            return JsonResponse({'status': 'error', 'error_message': f"{ex} - data saving error", 'index': request.POST['index']})
    else:
        return JsonResponse({'status': 'error', 'error_message': "request method error"})

def proxy_list(request):
    return HttpResponse(serializers.serialize("json", Proxy.objects.all()))

def proxy_delete(request):
    if request.method == 'POST':
        try:
            Proxy.objects.filter(pk = request.POST['id']).delete()
            return JsonResponse({'status': 'ok', 'message': f"Proxy id:{request.POST['id']} deleted", 'index':request.POST['index']})
        except Exception as ex:
            return JsonResponse(
                {'status': 'error', 'message': f"{ex} - Proxy id:{request.POST['id']} deleteting error", 'index': request.POST['index']})
    else:
        return JsonResponse({'status': 'error', 'error_message': "request method error"})


def proxy_check(request):
    if request.method == 'POST':
        import requests
        result = False
        proxy = Proxy.objects.filter(pk = request.POST['id']).get()
        if proxy.type == 'socks5':
            try:
                requests.get('https://google.com', proxies=dict(
                    https=f'{proxy.type}://{proxy.login}:{proxy.password}@{proxy.host}:{proxy.port}',
                    http=f'{proxy.type}://{proxy.login}:{proxy.password}@{proxy.host}:{proxy.port}'
                ), verify=True, timeout=20)
                result = True
            except Exception as ex:
                print(ex)
                result = False
        else:
            return JsonResponse({'status': 'error', 'error_message': "proxy type error", 'index': request.POST['index']})

        return JsonResponse({'status': 'ok', 'error_message': "proxy checked", 'result':result, 'index': request.POST['index']})

    else:
        return JsonResponse({'status': 'error', 'error_message': "request method error", 'index': request.POST['index']})
