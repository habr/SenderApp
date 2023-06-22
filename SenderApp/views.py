import requests
from datetime import datetime
from rest_framework import viewsets
from models import Client, Mailing, Message
from serializers import ClientSerializer, MailingSerializer, MessageSerializer
from django.http import JsonResponse


def send_message_to_subscriber(request, msg_id):
    # Extract the necessary information from the request
    phone_number = request.POST.get('phone_number')
    message = request.POST.get('message')

    # Perform the logic to send the message to the subscriber
    # ...

    # Example response data
    response_data = {
        'status': 'success',
        'message': 'Message sent successfully.',
    }

    return JsonResponse(response_data)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        mailing = serializer.save()
        if mailing.start_time > datetime.now():
            self.schedule_mailing(mailing)
        else:
            self.send_mailing(mailing)

    def perform_update(self, serializer):
        mailing = serializer.save()
        if 'start_time' in serializer.validated_data and mailing.start_time < datetime.now():
            self.cancel_mailing(mailing)
            self.send_mailing(mailing)
        else:
            self.schedule_mailing(mailing)

    def perform_destroy(self, instance):
        self.cancel_mailing(instance)
        instance.delete()

    def schedule_mailing(self, mailing):
        # Implement mailing scheduling using the chosen technology (e.g., Celery)
        pass

    def send_mailing(self, mailing):
        clients = Client.objects.filter(
            operator_code=mailing.filter_operator_code,
            tag=mailing.filter_tag
        )
        for client in clients:
            message = Message.objects.create(
                mailing=mailing,
                client=client,
                status='Sending'
            )
            self.send_message_to_external_service(client.phone_number, mailing.message, message.id)

    def cancel_mailing(self, mailing):
        # Implement mailing cancellation using the chosen technology
        pass

    def send_message_to_external_service(self, phone_number, message, message_id):
        url = 'https://probe.fbrq.cloud/send'
        headers = {
            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTg4OTU1MTUsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9rdmQxNyJ9.JfbWLWzopgBUCJ73e2wif4e7y-VQDHMH7AaQVvVuLiw',
            'Content-Type': 'application/json'
        }
        data = {
            'phone_number': phone_number,
            'message': message,
            'message_id': message_id
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            message = Message.objects.get(id=message_id)
            message.status = 'Sent'
            message.save()
        else:
            message = Message.objects.get(id=message_id)
            message.status = 'Error'
            message.save()


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer