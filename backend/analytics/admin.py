from django.contrib import admin
from .models import SiteConfiguration

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tracking_trigger')

    def has_add_permission(self, request):
        # Singleton Logic: Only allow adding if none exists
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
