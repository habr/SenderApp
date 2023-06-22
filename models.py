from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        app_label = 'SenderApp'


class Mailing(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    mailing_message = models.TextField()

    class Meta:
        app_label = 'SenderApp'


class Message(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    sent = models.BooleanField(default=False)

    class Meta:
        app_label = 'SenderApp'
