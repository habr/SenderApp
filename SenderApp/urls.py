from django.urls import include, path
from rest_framework import routers
from .views import ClientViewSet, MailingViewSet, MessageViewSet
from .views import send_message_to_subscriber

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'mailings', MailingViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    # Other URL patterns
    path('send/<int:msg_id>/', send_message_to_subscriber, name='send_message'),
]