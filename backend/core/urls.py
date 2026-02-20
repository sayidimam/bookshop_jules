from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/integrations/", include("integrations.urls")),
    # Add other app URLs here
]
