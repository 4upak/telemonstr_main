from django.shortcuts import render
from django.http import HttpResponse
from os import walk
import os
import json
import shutil
from .functions import *
# Create your views here.
from .models import Telegram_account
from django.http import JsonResponse
import glob
from django.core import serializers
from .models import Telegram_account
from proxy.models import Proxy
from funnels.models import Funnel
import re


def accounts_main_page(request):
    file_qty = len(glob.glob('accounts/sessions/import/*.session'))
    active_account_qty = Telegram_account.objects.count()
    active_proxy_qty = Proxy.objects.count()
    active_funnels_qty = Funnel.objects.count()

    data = {
        'title': "Аккаунты заголовок",
        'file_qty': file_qty,
        'active_account_qty': active_account_qty,
        'active_proxy_qty': active_proxy_qty,
        'active_funnels_qty': active_funnels_qty
    }

    return render(request, 'accounts/index.html', data)

def accounts_import_page(request):

    if request.method == 'POST':
        account_data = get_account_info(request.POST['session'])
        try:
            account_session_file = f'accounts/sessions/import/{request.POST["session"]}.session'
            account_json_file = f'accounts/sessions/import/{request.POST["session"]}.json'
            shutil.copy(account_session_file, 'accounts/sessions/active/')
            shutil.copy(account_json_file, 'accounts/sessions/active/')
        except Exception as ex:
            return JsonResponse({'status': 'error', 'error_message': f"{ex} - copy file error",'index': request.POST['index']})

        try:
            os.remove(f'accounts/sessions/import/{request.POST["session"]}.session')
            os.remove(f'accounts/sessions/import/{request.POST["session"]}.json')
        except Exception as ex:
            return JsonResponse({'status': 'error', 'error_message': f"{ex} - deleting files from import dir error", 'index': request.POST['index']})



        try:
            account = Telegram_account(
                session_file=request.POST["session"]
            )
            if 'last_name' in account_data:
                account.last_name = account_data['last_name']
            if 'first_name' in account_data:
                account.first_name = account_data['first_name']
            if 'username' in account_data:
                account.username = account_data['username']
            if 'twoFA' in account_data:
                account.twoFA = account_data['twoFA']
            if 'password' in account_data:
                account.twoFA_password = account_data['password']
            account.save()
        except Exception as ex:
            return JsonResponse({'status': 'error', 'error_message': f"{ex} - data saving error", 'index': request.POST['index']})
        return JsonResponse({'status':'ok', 'imported_session':request.POST['session'], 'created_index':account.id, 'index': request.POST['index']})

    else:
        return JsonResponse({'status': 'error', 'error_message': "unknown_error"})

def active_accounts_api_page(request):
    return HttpResponse(serializers.serialize("json", Telegram_account.objects.all()))

def accounts_api_page(request):
    dir_name = 'accounts/sessions/import'
    sessions = []
    for (dirpath, dirnames, filenames) in walk(dir_name):
        for file in filenames:
            file_data = file.split('.')
            if file_data[1] == 'session':
                sessions.append(file_data[0])
    data = []
    for session in sessions:
        try:
            f = open(f"accounts/sessions/import/{session}.json", "r")
            with f as read_file:
                data.append(json.load(read_file))
        except Exception as ex:
            data.append(ex)
    return HttpResponse(json.dumps(data))



def accounts_delete_active_account(request):
    if request.method == 'POST':
        try:
            account = Telegram_account.objects.filter(pk = request.POST['account_id']).get()
            session = account.session_file
        except Exception as ex:
            return JsonResponse({'status': 'error', 'error_message': "Load Telegram account from databese error", 'index': request.POST['index']})
        try:
            shutil.move(f"accounts/sessions/active/{session}.json", f"accounts/sessions/trash/{session}.json")
            shutil.move(f"accounts/sessions/active/{session}.session", f"accounts/sessions/trash/{session}.session")
        except Exception as ex:
            return JsonResponse({'status': 'error', 'error_message': f"{ex} File move error", 'index': request.POST['index']})

        try:
            Telegram_account.objects.filter(pk = request.POST['account_id']).delete()
        except Exception as ex:
            return JsonResponse({'status': 'error', 'error_message': "Database removing error", 'index': request.POST['index']})

        return JsonResponse({'status': 'ok', 'message': f"{session} removed succesfull", 'index': request.POST['index']})

    else:
        return JsonResponse({'status': 'error', 'error_message': "request method error", 'index': request.POST['index']})

