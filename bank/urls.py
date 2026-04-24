from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet,AuthenticationViewsets, TransferView,
    MyNotification
)

router = DefaultRouter()
router.register(r'auth',AuthenticationViewsets,'auth')
router.register(r'transactions',TransactionViewSet,'transactions')

urlpatterns = [

]