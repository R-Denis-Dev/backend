from rest_framework import (
    status,viewsets,views,permissions
)
from decimal import Decimal
from rest_framework.response import Response
from rest_framework.authentication import (
    authenticate, get_user_model
    )
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.db.models import (
    F, ExpressionWrapper, 
    Sum,Min,Max,
    DecimalField
    )
from .serializers import (
    LoginSerializer,RegisterSerializer,
    TransactionSerializer, TransferSerialzer, TransferPreviewSerialzer,
    MessageSerialzier
    
)
from .models import (
    Transaction,Transfer,Message
    )



class AuthenticationViewsets(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(methods=['post'],detail=False)
    def register(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'detail':"Вы успешно зарегистрировались"
        })
        
    @action(methods=['post'],detail=False)
    def login(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            return Response({
                "detail":"Неверные данные"
            }, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'accessToken':token.key,
            'timestamp':created,
            'user':serializer.data
        })
        
class TransactionViewSet(viewsets.ModelViewSet):
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(client=self.request.user)
    
    @action(methods=['get'],detail=False)
    def balance(self,request):
        queryset = self.queryset.filter(client=request.user,status="approved")
        balance_information = queryset.aggregate(
            balance = Sum('cash'),
        )
        return Response(balance_information)
    

class TransferView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        serializer = TransferSerialzer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(sender=request.user)
        return Response(TransferPreviewSerialzer(transaction).data)
        
        
class MyNotification(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        queryset = Message.objects.filter(client=request.user, is_read=False)
        response = MessageSerialzier(queryset,many=True).data
        queryset.update(is_read=True)
        return Response(response)