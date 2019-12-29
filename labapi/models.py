from django.db import models
from django.conf import settings


class Patients(models.Model):
    code = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=40, null=False, blank=False)
    mname = models.CharField(max_length=40, null=False, blank=False)
    lname = models.CharField(max_length=40, null=False, blank=False)
    birthday = models.DateField(auto_now=False, null=False, blank=False)
    card_number = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=30, null=False, blank=False, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.fname} {self.lname}'


class Transactions(models.Model):
    STATUS_CHOICES = (
        (1, 'Стадия 1'),
        (2, 'Стадия 2'),
        (3, 'Стадия 3'),
        (4, 'Стадия 4'),
    )

    PAYMENT_CHOICES = (
        (1, 'Оплата наличными'),
        (2, 'Оплата картой'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    urgently = models.BooleanField(default=False)
    payment_type = models.IntegerField(choices=PAYMENT_CHOICES, default=1)

    patient = models.ForeignKey(
        Patients,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.status} {self.patient_id}'


class Logger(models.Model):
    request_type = models.CharField(max_length=10, null=False, blank=False)
    request_date = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField(null=False)
    patient_code = models.IntegerField(null=False)
    transaction_id = models.IntegerField(null=True)
    before = models.TextField(max_length=400, null=True, blank=False)
    after = models.TextField(max_length=400, null=True, blank=False)

    def __str__(self):
        return f'{self.request_type} {self.user_id}'
