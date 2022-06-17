from django.shortcuts import render


from django.shortcuts import render
from django.http import HttpResponse
from os import walk
import os
import json
import shutil

# Create your views here.
from accounts.models import Telegram_account
from django.http import JsonResponse
import glob
from django.core import serializers

from accounts.models import Proxy
from .models import Funnel, Funnel_message
from django.core.files.storage import FileSystemStorage
import re
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FunnelSerializer, FunnelMessageSerializer

from rest_framework.viewsets import ModelViewSet

class FunnelViewSet(ModelViewSet):
    queryset = Funnel.objects.all()
    serializer_class = FunnelSerializer

class FunnelMessagemessageViewSet(ModelViewSet):
    queryset = Funnel.objects.all()
    serializer_class = FunnelMessageSerializer

# Create your views here.
def funnels_page(request):
    active_account_qty = Telegram_account.objects.count()
    active_proxy_qty = Proxy.objects.count()
    active_funnels_qty = Funnel.objects.count()
    data = {
        'title': "Аккаунты заголовок",
        'active_account_qty': active_account_qty,
        'active_proxy_qty': active_proxy_qty,
        'active_funnels_qty': active_funnels_qty
    }


    return render(request, 'funnels.html', data)

def funnels_add(request):
    if request.method == 'POST':
        funnels_name_qty = Funnel.objects.filter(funnel_name = request.POST['funnel_name']).count()
        if funnels_name_qty == 0:
            try:
                pat = re.compile(r"[A-Za-z0-9\s]+")
                if re.fullmatch(pat, request.POST['funnel_name']):
                    funnel = Funnel(
                        funnel_name = request.POST['funnel_name']
                    )
                    funnel.save()
                    return JsonResponse({'status': 'ok', 'error_message': f"Funnel {request.POST['funnel_name']} created!"})
                else:
                    return JsonResponse({'status': 'error', 'error_message': f"Value in not alphanumeric"})
            except Exception as ex:
                return JsonResponse({'status': 'error', 'error_message': f"{ex} - data saving error"})
        else:
            return JsonResponse({'status': 'error', 'error_message': f"Funnel {request.POST['funnel_name']} already exist"})
    else:
        return JsonResponse({'status': 'error', 'error_message': 'Method error'})

def funnels_list(request):
    funnels = Funnel.objects.all().order_by('pk')
    return HttpResponse(serializers.serialize("json", funnels))


@api_view(['GET','POST'])
def funnels_list_api(request):
    if request.method == 'GET':
        funnels = Funnel.objects.all().order_by('pk')
        serializer = FunnelSerializer(funnels, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FunnelSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def funnels_message_list_api(request):
    if request.method == 'GET':
        funnels_messages = Funnel_message.objects.all().order_by('pk')
        serializer = FunnelMessageSerializer(funnels_messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FunnelMessageSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def funnels_detail(request,pk):
    try:
        funnel = Funnel.objects.get(pk = pk)
    except Funnel.DoesNotExist:
        return Response( status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FunnelSerializer(funnel)
        return Response(serializer.data)

    elif request.method == 'PUT':
        print(request.data)
        serializer = FunnelSerializer(funnel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        funnel.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def funnels_message_detail(request, pk):
    try:
        funnel_message = Funnel_message.objects.get(pk = pk)
    except funnel_message.DoesNotExist:
        return Response( status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FunnelMessageSerializer(funnel)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FunnelMessageSerializer(funnel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        funnel_message.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



def funnels_delete(request):
    if request.method == 'POST':
        try:
            Funnel.objects.filter(pk = request.POST['funnel_id']).delete()
            return JsonResponse({'status': 'ok', 'message': f"Funnel id:{request.POST['funnel_id']} deleted", 'funnel_index':request.POST['index']})
        except Exception as ex:
            return JsonResponse(
                {'status': 'error', 'message': f"{ex} - Proxy id:{request.POST['funnel_id']} deleteting error", 'funnel_index': request.POST['index']})
    else:
        return JsonResponse({'status': 'error', 'error_message': "request method error"})

def funnels_edit(request,funnel_id):
    active_account_qty = Telegram_account.objects.count()
    active_proxy_qty = Proxy.objects.count()
    active_funnels_qty = Funnel.objects.count()
    funnel_name = Funnel.objects.filter(pk = funnel_id).first().funnel_name
    data = {
        'title': "Аккаунты заголовок",
        'active_account_qty': active_account_qty,
        'active_proxy_qty': active_proxy_qty,
        'active_funnels_qty': active_funnels_qty,
        'funnel_id':funnel_id,
        'funnel_name':funnel_name

    }

    return render(request, 'funnels_edit.html', data)

def funnels_item_add(request):
    file = request.FILES.get("funnel_image")
    fss = FileSystemStorage()
    file.name="funnel_image.png"
    filename = fss.save(f"funnels_images/{file.name}", file)
    url = fss.url(filename)
    current_funnel = Funnel.objects.filter(pk = request.POST['funnel_id']).first()
    funnel_message = Funnel_message(
        text_message = request.POST['text_message'],
        json_data = "",
        answer_to = 0,
        user_id = request.POST['user_id'],
        delay_before= request.POST['delay_before'],
        delay_after = request.POST['delay_after'],
        message_photo = url,
        funnel = current_funnel
    )
    funnel_message.save()

    return JsonResponse({
        'status': 'ok',
        'message': "image uploaded",
        "added_item": serializers.serialize("json",[funnel_message])
    })