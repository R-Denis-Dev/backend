from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
from django.db.models import Sum
from .models import Transfer, Transaction, Message

@transaction.atomic
@receiver(sender=Transfer, signal=post_save)
def transfer_to(sender,instance, created, **kwargs):
    if created:
        sender = instance.sender
        addressee = instance.addressee
        cash = instance.cash
        
        queryset = Transaction.objects.filter(
            client=sender,status="approved"
        )
        balance = queryset.aggregate(
            balance=Sum(cash)
        )
        print(balance)
        if float(balance['balance']) < cash:
            return None
            
        transaction_sender = Transaction.objects.create(
            client = sender,
            status = "registred",
            cash=cash*-1
        )
        transaction_addressee = Transaction.objects.create(
            client = addressee,
            status = "registred",
            cash=cash
        )
        
        
        transaction_sender.status="approved"
        transaction_addressee.status="approved"
        transaction_sender.save()
        transaction_addressee.save()
        
@receiver(sender=Transaction, signal=post_save)
def transaction_message(sender,instance,created, **kwargs):
    if instance.status != 'approved':
        return None
    message =f"""
Перевод средств {instance.id}:
Сумма: {instance.cash}
Дата транзацкии:{instance.created_at}
Дата подтверждения:{instance.updated_at}
"""
    if Message.objects.filter(message=message).exists():
        return None
    Message.objects.create(
        client=instance.client,
        message=message
    )