from django.contrib import admin
from . import models
# Register your models here.



class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['key' , 'owner']

class CellphoneVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['key' , 'cellphone']


admin.site.register(models.VerificationToken , VerificationTokenAdmin)
admin.site.register(models.CellphoneVerificationToken , CellphoneVerificationTokenAdmin)
