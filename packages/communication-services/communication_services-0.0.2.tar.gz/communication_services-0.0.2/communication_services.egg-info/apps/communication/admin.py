from django.contrib import admin
from yaml import emit

# from .app_models.entity_models.app import app
from .app_models.entity_models.email_notification import emailNotification
from .app_models.entity_models.mobile_notification import mobileNotification
from .app_models.entity_models.sms_notification import smsNotification
# Register your models here.
class BookConfigView(admin.ModelAdmin):
    list_display = ["id", "title", "description", "created"]
class AllConfigView(admin.ModelAdmin):
    def get_list_display(self, request):
        """Return a tuple containing the fields of the model, which are to be displayed in the list."""
        return [field.name for field in self.model._meta.fields]

# admin.site.register(app,AllConfigView)
admin.site.register(emailNotification,AllConfigView)
admin.site.register(smsNotification,AllConfigView)
admin.site.register(mobileNotification,AllConfigView)