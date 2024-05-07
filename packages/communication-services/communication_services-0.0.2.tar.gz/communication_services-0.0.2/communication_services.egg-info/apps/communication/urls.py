from django.urls import include, path

app_name = "communication"

urlpatterns = [
    path("v1.0/", include("apps.communication.app_views.v1.config.urls")),
]
