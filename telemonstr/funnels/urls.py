from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', FunnelViewSet, basename = 'funnel')
router.register('funnel_messages', FunnelMessagemessageViewSet, basename = 'funnel_message')
urlpatterns = router.urls

urlpatterns.append(path('active', funnels_page))
urlpatterns.append(path('edit/<int:funnel_id>', funnels_edit)),




'''urlpatterns = [
    path('', funnels_page),
    path('add/', funnels_add),
    path('list/', funnels_list),

    path('delete/', funnels_delete),
    path('edit/<int:funnel_id>', funnels_edit),
    path('item/add/', funnels_item_add),

    path('api/funnels_list/', funnels_list_api),
    path('api/funnels_messages_list/', funnels_message_list_api),

    path('api/funnels_detail/<int:pk>', funnels_detail),
    path('api/funnels_message_detail/<int:pk>', funnels_message_detail),


]'''
