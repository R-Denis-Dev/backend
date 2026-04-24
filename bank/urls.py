from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthenticationViewSet, TransactionViewSet, TransferView, MyNotification

router = DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='auth')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/transfer/', TransferView.as_view(), name='transfer'),
    path('api/notifications/', MyNotification.as_view(), name='notifications'),
]
