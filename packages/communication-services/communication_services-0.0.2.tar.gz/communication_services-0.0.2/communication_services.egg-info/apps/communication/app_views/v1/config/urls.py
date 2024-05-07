from unicodedata import name
from django.urls import path
from rest_framework.routers import SimpleRouter
# from ..book import book_views
from ..main import main_views

# router = SimpleRouter()
# router.register("book/", book_views.BookClassViewSet, basename="book-list")
# urlpatterns = router.urls

urlpatterns = [
    path('send/email', main_views.send_email_view ,name='send_email'),
    path('send/sms', main_views.send_sms_view, name='send_sms'),
    path('send/notify', main_views.send_notification_view, name='send_notify'),
    path('send/verify', main_views.send_verify_view, name='send_verify'),
    path('check/verify', main_views.check_verify_view, name='check_verify'),
]