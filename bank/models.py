from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass



class Transaction(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_client")
    status = models.CharField(choices=(
        ['registred','Зарегистрирована'],
        ['denied','Отменена'],
        ['approved','Одобрена'],
    ))
    cash = models.DecimalField(decimal_places=1, max_digits=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    
class Transfer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_client")
    addressee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addressee_client")
    cash = models.DecimalField(decimal_places=1, max_digits=10000)
    
    
class Message(models.Model):
    client = models.ForeignKey(User,on_delete=models.CASCADE,related_name="message_client")
    message = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)