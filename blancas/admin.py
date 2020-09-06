from django.contrib import admin
from blancas.models import Search, Surname

class SurnamesAdmin(admin.ModelAdmin):
    search_fields = ('surname', )
    ordering = ['surname', ]

# from django import forms
# from django.utils.translation import gettext as _

# Register your models here.
admin.site.register(Search)
admin.site.register(Surname, SurnamesAdmin)
